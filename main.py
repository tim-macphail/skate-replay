import cv2
import pyaudio
import numpy as np
import time

# Configuration
CLAP_THRESHOLD = 2000  # Adjust this threshold according to your environment
EVENT_DEBOUNCE_TIME = 0.5  # Debounce time in seconds
RECOLLECTION = 2  # seconds
CONTINUATION = 1  # seconds
PLAYBACK_RATE = 0.25
FRAME_INTERVAL = int(1 / PLAYBACK_RATE)

# pyaudio constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

clap_detected_time = 0

print("initializing audio stream 👂...")
# Initialize PyAudio
audio = pyaudio.PyAudio()
# Open audio stream
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)
print("audio stream initialized")

# Initialize the webcam
print("initializing webcam 📹...")
cap = cv2.VideoCapture(0)
print("webcam initialized")

FRAME_RATE = cap.get(cv2.CAP_PROP_FPS)

memory = []
buffer_size_cap = int(FRAME_RATE * RECOLLECTION)
slow_mo = False

slowmo_control = 0

REPLAY_FRAME_COUNT = FRAME_RATE * (RECOLLECTION + CONTINUATION) * FRAME_INTERVAL
# capture loop (FRAME_RATE iterations / sec)
while True:
    # Capture and flip the frame
    ret, frame = cap.read()
    # frame = cv2.flip(frame, 1)

    memory.append(frame)

    if not slow_mo:
        cv2.imshow("Webcam", frame)  # read from the back of the queue
        if len(memory) > buffer_size_cap:
            memory.pop(0)
    else:
        if not slowmo_control:
            slow_mo = False
        elif slowmo_control % FRAME_INTERVAL == 0:  # show every 2nd frame
            cv2.imshow("Webcam", memory.pop(0))
        slowmo_control -= 1

    # # Exit the loop if 'q' is pressed
    # if cv2.waitKey(1) & 0xFF == ord("q"):
    #     print("quitting...")
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     # Close PyAudio stream and terminate PyAudio
    #     stream.stop_stream()
    #     stream.close()
    #     audio.terminate()
    #     exit(0)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        slow_mo = not slow_mo
        memory = memory[:buffer_size_cap]  # truncate the buffer
        slowmo_control = REPLAY_FRAME_COUNT
        # else:
        #     print("back to regs")
        #     slow_mo = False
        #     memory = memory[:buffer_size_cap]  # truncate the buffer

        # Read audio data from the stream
        # data = stream.read(CHUNK)

        # # Convert binary data to numpy array
        # audio_data = np.frombuffer(data, dtype=np.int16)

        # # Check if the amplitude exceeds the threshold
    # if np.max(np.abs(audio_data)) > CLAP_THRESHOLD:
    # If a potential clap is detected, check debounce time
    # current_time = time.time()
    # if current_time - clap_detected_time > CLAP_DEBOUNCE_TIME:
    #     print("Clap detected!")
    #     slow_mo = True  # TODO: make this trigger some function or something
    #     clap_detected_time = current_time
