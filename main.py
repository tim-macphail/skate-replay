import cv2

import pyaudio
import numpy as np
import time

# Configuration
CLAP_THRESHOLD = 2000  # Adjust this threshold according to your environment
CLAP_DEBOUNCE_TIME = 0.5  # Debounce time in seconds
STREAM_DELAY = 0  # seconds

# Constants for audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Variables for debounce
clap_detected_time = 0

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)


# Initialize the webcam
print("initializing webcam...")
cap = cv2.VideoCapture(0)
print("webcam initialized")

max_fps = cap.get(cv2.CAP_PROP_FPS)

frame_buffer = []
buffer_size_cap = int(max_fps * STREAM_DELAY)
slow_mo = False
show_frame = True

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)
    frame_buffer.append(frame)

    if show_frame and len(frame_buffer) > buffer_size_cap:
        cv2.imshow("Webcam", frame_buffer.pop(0))

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("quitting...")
        cap.release()
        cv2.destroyAllWindows()
        # Close PyAudio stream and terminate PyAudio
        stream.stop_stream()
        stream.close()
        audio.terminate()
        exit(0)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        if not slow_mo:
            print("okay slow mo now")
            slow_mo = True
        else:
            print("back to regs")
            slow_mo = False
            frame_buffer = frame_buffer[:buffer_size_cap]  # truncate the buffer
            show_frame = True

    if slow_mo:
        show_frame = (
            not show_frame
        )  # toggle if we're showing a new frame each loop. TODO: develop a better mechanism for this

    # Read audio data from the stream
    # !this probably takes some time
    data = stream.read(CHUNK)

    # Convert binary data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Check if the amplitude exceeds the threshold
    if np.max(np.abs(audio_data)) > CLAP_THRESHOLD:
        # If a potential clap is detected, check debounce time
        current_time = time.time()
        if current_time - clap_detected_time > CLAP_DEBOUNCE_TIME:
            print("Clap detected!")
            slow_mo = True
            clap_detected_time = current_time
