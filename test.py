#!/usr/bin/env python3
import cv2
import numpy as np
import os
import shutil
from PIL import Image

def extract_frames(video_path):
  """Extracts frames from a video."""
  cap = cv2.VideoCapture(video_path)
  frames = []
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    frames.append(frame)
  cap.release()
  return frames

def is_frame_different(frame1, frame2, threshold=30):
  """Determines if two frames are different."""
  gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
  gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
  diff = cv2.absdiff(gray1, gray2)
  non_similar_pixels = np.sum(diff > threshold)
  return non_similar_pixels > (diff.size * 0.01)  # 1% difference

def find_unique_frames(frames):
  """Finds unique frames in a list of frames."""
  unique_frames = []
  last_frame = None
  for frame in frames:
    if last_frame is not None:
      if is_frame_different(frame, last_frame):
        unique_frames.append(frame)
    else:
      unique_frames.append(frame)
    last_frame = frame
  return unique_frames


def stitch_frames(frames):
  """Stitches frames together to form a single long image."""
  if len(frames) > 0:
    return np.vstack(frames)
  else:
    return None

def convert_to_jpg(input_path, output_path):
  try:
    # Open the image
    img = Image.open(input_path)

    # Ensure the output format is JPG
    if img.format != "JPEG":
      img = img.convert("RGB")

    # Save as JPG
    img.save(output_path, "JPEG")
    img.close()
    return True
  except Exception as e:
    print(f"Error converting to JPG: {e}")
    return False





if __name__ == "__main__":
  try:
    video_path = 'rec1.mp4' # source video

    frames = extract_frames(video_path)  # Using only the first 50 frames for testing
    print(f"Extracted {len(frames)} frames.")

    unique_frames = find_unique_frames(frames)
    print(f"Found {len(unique_frames)} unique frames.")

    long_screenshot = stitch_frames(unique_frames)
    png_output_file = 'long1.png'
    cv2.imwrite(png_output_file, long_screenshot)

    # Convert to JPG
    jpg_output_file = 'long1.jpg'
    if convert_to_jpg(png_output_file, jpg_output_file):
      print(f"Long screenshot saved as '{output_file_jpg}'.")
      # Optionally, you can remove the PNG file if no longer needed
      os.remove(png_output_file)
    else:
      print("Failed to convert to JPG.")

  except Exception as e:
    print(f"Error occurred: {e}")
