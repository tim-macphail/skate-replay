from datetime import datetime
from typing import List
import cv2
import numpy as np
from logger import log
from os import path, mkdir

REPLAY_DIR_NAME = "replays"

if not path.exists(REPLAY_DIR_NAME):
    mkdir(REPLAY_DIR_NAME)


def save_video(frames: List[np.ndarray], fps: int = 30) -> None:
    if not frames:
        raise ValueError("list of frames is empty")

    video_name = f"skate-replay_{datetime.now().strftime('%Y-%m-%d_%H%M')}.mp4"
    log.info(f"saving video {video_name}...")
    filepath = path.join(REPLAY_DIR_NAME, video_name)

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # type: ignore
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    log.info(f"video {filepath} saved")
