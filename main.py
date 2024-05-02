import cv2
import pyaudio
import numpy as np

# configuration constants
EVENT_AMPLITUDE_THRESHOLD = 10000  # Adjust this threshold according to your environment
RECOLLECTION = 2  # seconds
CONTINUATION = 1  # seconds
REPLAY_PLAYBACK_RATE = 0.25

# pyaudio constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# initialize audio capture
print("initializing audio stream 👂...")
audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)
print("audio stream initialized.")

# initialize the webcam
print("initializing webcam 📹...")
cap = cv2.VideoCapture(0)
print("webcam initialized.")

# computed constants
FRAME_RATE = cap.get(cv2.CAP_PROP_FPS)
MEMORY_CAP = int(FRAME_RATE * RECOLLECTION)
REPLAY_FRAME_INTERVAL = int(1 / REPLAY_PLAYBACK_RATE)
REPLAY_FRAME_COUNT = int(FRAME_RATE * (RECOLLECTION + CONTINUATION))

# global control variables
memory = []
playback_control = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    audio_data = stream.read(CHUNK)

    memory.append(frame)

    if not playback_control:
        cv2.imshow("Webcam", frame)
        while len(memory) > MEMORY_CAP:
            memory.pop(0)

        audio_data = np.frombuffer(audio_data, dtype=np.int16)
        if np.max(np.abs(audio_data)) > EVENT_AMPLITUDE_THRESHOLD:
            print(f"event with amplitude {np.max(np.abs(audio_data))} detected!")
            playback_control = REPLAY_FRAME_COUNT * REPLAY_FRAME_INTERVAL
    else:
        if playback_control % REPLAY_FRAME_INTERVAL == 0:
            cv2.imshow("Webcam", memory.pop(0))
        playback_control -= 1
        if playback_control == 0:
            print("resume live stream.")

    if cv2.waitKey(1) & 0xFF == ord("s"):
        playback_control = 0

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("quitting...")
        cap.release()
        cv2.destroyAllWindows()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        exit(0)
