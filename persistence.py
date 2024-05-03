from typing import List
import cv2
import numpy as np


def create_video(frames: List[np.ndarray], output_path: str, fps: int = 30) -> None:
    """
    Create a video from a list of frames and write it to the local filesystem.

    Parameters:
        frames (List[np.ndarray]): List of frames to create the video from.
        output_path (str): Output path to save the video.
        fps (int, optional): Frames per second for the output video. Default is 30.

    Returns:
        None
    """
    print("Creating video...")
    if not frames:
        raise ValueError("List of frames is empty")

    # Get dimensions of the frames
    height, width, _ = frames[0].shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )  # Choose the codec according to file extension
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Write frames to the video
    for frame in frames:
        out.write(frame)

    # Release the VideoWriter object
    out.release()


# Example usage:
# frames_list = [frame1, frame2, frame3, ...]  # List of frames (numpy arrays)
# create_video(frames_list, 'output_video.mp4')
