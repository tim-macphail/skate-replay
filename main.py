import cv2
import pyaudio
import numpy as np
import argparse

from persistence import save_replay
from logger import log

parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--sound", help="threshold for audio event detection", default=10000
)
parser.add_argument(
    "-r",
    "--recollection",
    help="playback duration after event detection (seconds)",
    default=1,
)
parser.add_argument(
    "-c",
    "--continuation",
    help="playback duration after event detection (seconds)",
    default=1,
)
parser.add_argument("-p", "--playback", help="event playback rate", default=0.5)
args = parser.parse_args()

log.debug(args)

EVENT_AMPLITUDE_THRESHOLD = int(args.sound)
RECOLLECTION = float(args.recollection)
CONTINUATION = float(args.continuation)
REPLAY_PLAYBACK_RATE = float(args.playback)

# pyaudio constants
CHUNK = 1024

# initialize audio capture
log.info("initializing audio stream 👂...")
audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNK
)
log.info("audio stream initialized.")

# initialize the webcam
log.info("initializing webcam 📹...")
cap = cv2.VideoCapture(0)
log.info("webcam initialized.")

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
            log.info(f"event with amplitude {np.max(np.abs(audio_data))} detected!")
            playback_control = REPLAY_FRAME_COUNT * REPLAY_FRAME_INTERVAL
    else:
        if playback_control % REPLAY_FRAME_INTERVAL == 0:
            cv2.imshow("Webcam", memory.pop(0))
        playback_control -= 1
        if playback_control == 0:
            log.info("resume live stream.")

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == " ":
        save_replay(memory)

    if key == "q":
        log.info("quitting...")
        cap.release()
        cv2.destroyAllWindows()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        exit(0)
