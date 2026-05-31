#!/usr/bin/env python3
"""
CTF Video Color Decoder
- Samples the first frame of every 30-frame block
- Reads the center pixel color as a hex code (e.g. #620000)
- Takes the first two hex digits (e.g. "62"), interprets as hex byte
- Converts to ASCII character (0x62 = 98 = 'b')
- Prints the full decoded message
"""

import cv2
import sys


def get_center_pixel_hex(frame):
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    b, g, r = frame[cy, cx]
    return f"{r:02x}{g:02x}{b:02x}"  # RGB hex string, e.g. "620000"


def decode_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: could not open '{video_path}'")
        sys.exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video: {total_frames} frames @ {fps:.1f} fps")
    print(f"Sampling frame 0, 30, 60, ... (first frame of each 30-frame block)\n")

    message = ""
    frame_idx = 0

    while True:
        # Jump to the target frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        hex_color = get_center_pixel_hex(frame)
        first_two = hex_color[:2]           # e.g. "62"
        byte_val = int(first_two, 16)       # e.g. 0x62 = 98
        char = chr(byte_val)                # e.g. 'b'

        print(f"Frame {frame_idx:>5}: #{hex_color.upper()}  ->  0x{first_two.upper()} = {byte_val:>3}  ->  '{char}'")
        message += char

        frame_idx += 30

    cap.release()

    print(f"\n{'='*50}")
    print(f"Decoded message: {message}")
    print(f"{'='*50}")

    # Also print hex dump in case some chars are non-printable
    hex_dump = " ".join(f"{ord(c):02x}" for c in message)
    print(f"Hex dump:        {hex_dump}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decode_video.py <video.mp4>")
        sys.exit(1)

    decode_video(sys.argv[1])
