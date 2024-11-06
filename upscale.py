import argparse
import os
import torch
import torchvision.transforms as transforms
from torchvision.io import read_video, write_video
from tqdm import tqdm
import ffmpeg  # Import ffmpeg-python for deinterlacing
import subprocess

# Import the frame interpolation model from frame-interpolation-pytorch
# from frame_interpolation_pytorch.interpolator import Interpolator  # Commented out as interpolation is disabled

def parse_arguments():
    parser = argparse.ArgumentParser(description='Upscale and process video using PyTorch.')
    parser.add_argument('input_video', type=str, help='Path to the input video file.')
    parser.add_argument('--duration', type=int, help='Duration in seconds for processing.')
    parser.add_argument('--deinterlace', action='store_true', help='Deinterlace the video.')
    parser.add_argument('--double-fps', action='store_true', help='Double the frame rate by interpolating frames.')
    return parser.parse_args()

def trim_video(input_video, output_video, duration):
    # Use ffmpeg-python to trim the video to the specified duration
    ffmpeg.input(input_video, t=duration).output(output_video).run()

def upscale_with_video2x(input_video, output_video):
    # Call video2x to upscale the video
    subprocess.run(['video2x', '--input', input_video, '--output', output_video])

def deinterlace_video(input_video, output_video):
    # Use ffmpeg-python to deinterlace the video
    ffmpeg.input(input_video).vf('yadif').output(output_video).run()

def process_video(input_video, duration=None, deinterlace=False, double_fps=False):
    # Trim video if duration is specified
    if duration:
        trimmed_video = f"{os.path.splitext(input_video)[0]}-trimmed.mp4"
        trim_video(input_video, trimmed_video, duration)
        input_video = trimmed_video

    # Deinterlace if required
    if deinterlace:
        deinterlaced_video = f"{os.path.splitext(input_video)[0]}-deinterlaced.mp4"
        deinterlace_video(input_video, deinterlaced_video)
        input_video = deinterlaced_video

    # Load video
    video, audio, info = read_video(input_video)
    fps = info['video_fps']
    num_frames = video.size(0)

    # Upscale to 4k using video2x
    output_name = f"{os.path.splitext(input_video)[0]}-upscaled.mp4"
    upscale_with_video2x(input_video, output_name)

    # Double FPS if required
    if double_fps:
        # Interpolation logic is disabled
        print("Frame interpolation is currently disabled.")

    # Write output video with original FPS
    write_video(output_name, video, fps=fps)

    print(f"Output video saved as {output_name}")

def main():
    args = parse_arguments()
    process_video(args.input_video, args.duration, args.deinterlace, args.double_fps)

if __name__ == "__main__":
    main() 