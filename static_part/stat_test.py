#!/usr/bin/env python3
import cv2
import numpy as np

def extract_frames(video_path, num_frames=30):
  """Extracts a specified number of frames from the beginning of the video."""
  cap = cv2.VideoCapture(video_path)
  frames = []
  for _ in range(num_frames):
    ret, frame = cap.read()
    if not ret:
      break
    frames.append(frame)
  cap.release()
  return frames

def find_static_regions(frames, check_header=True, check_banner=True):
  """Finds static regions (header and/or banner) in the given frames."""
  if not frames:
    return None, None

  base_frame = frames[0]
  height, width, _ = base_frame.shape
  accum_diff = np.zeros((height, width), dtype=np.float32)

  # Calculating the difference with other frames
  for frame in frames[1:]:
    diff = cv2.absdiff(base_frame, frame)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh_diff = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
    accum_diff += thresh_diff

  accum_diff = accum_diff / len(frames)
  _, static_mask = cv2.threshold(accum_diff, 1, 255, cv2.THRESH_BINARY_INV)

  header, banner = None, None
  header_section = height // 10
  banner_section = height // 10

  if check_header:
    header_staticness = np.mean(static_mask[:header_section])
    print("Find static header: ", header_staticness)
    if header_staticness > 250:  # High value indicates static region
      header = base_frame[:header_section]

  if check_banner:
    banner_staticness = np.mean(static_mask[-banner_section:])
    print("Find static banner, got: ", banner_staticness)
    if banner_staticness > 250:  # High value indicates static region
      banner = base_frame[-banner_section:]

  return header, banner

def save_images(header, banner, output_dir="."):
  """Saves the header and banner images."""
  if header is not None:
    cv2.imwrite(f"{output_dir}/header.png", header)
  if banner is not None:
    cv2.imwrite(f"{output_dir}/banner.png", banner)

# Example Usage
video_path = '../rec1.mp4'
frames = extract_frames(video_path)
header, banner = find_static_regions(frames, check_header=True, check_banner=False)
save_images(header, banner)

