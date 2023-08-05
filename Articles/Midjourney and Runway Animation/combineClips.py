from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
from PIL import Image
import os
import re
import cv2
import matplotlib.pyplot as plt

target_resolution = (1280, 720)  # You can change this to any desired size
duration = 8
title = "sculptures"

def get_image_resolution(image_path):
    with Image.open(image_path) as img:
        return img.size

def get_video_resolution(video_path):
    video_clip = VideoFileClip(video_path)
    return video_clip.size



def process_image(file_path, target_resolution, duration=duration):
    # Load the image and get its original resolution
    image_resolution = get_image_resolution(file_path)

    # Calculate the scaling factors for width and height
    width_factor = target_resolution[0] / image_resolution[0]
    height_factor = target_resolution[1] / image_resolution[1]

    # Use the smaller scaling factor to maintain the aspect ratio
    scaling_factor = min(width_factor, height_factor)

    # Calculate the new dimensions after scaling
    new_width = int(image_resolution[0] * scaling_factor)
    new_height = int(image_resolution[1] * scaling_factor)

    # Resize the image to the new dimensions
    image_clip = ImageClip(file_path).resize((new_width, new_height))
    return image_clip.set_duration(duration)


def process_video(file_path, target_resolution):
    # Load the video and get its original resolution
    video_resolution = get_video_resolution(file_path)

    # Calculate the scaling factors for width and height
    width_factor = target_resolution[0] / video_resolution[0]
    height_factor = target_resolution[1] / video_resolution[1]

    # Use the smaller scaling factor to maintain the aspect ratio
    scaling_factor = min(width_factor, height_factor)

    # Calculate the new dimensions after scaling
    new_width = int(video_resolution[0] * scaling_factor)
    new_height = int(video_resolution[1] * scaling_factor)

    # Resize the video to the new dimensions
    video_clip = VideoFileClip(file_path).resize((new_width, new_height))

    return video_clip

def main():
    folder_path = "sculptures/toProduction/"
    file_list = sorted(os.listdir(folder_path))

   

    clips = []

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.png'):
            image_clip = process_image(file_path, target_resolution)
            clips.append(image_clip)
        elif file_name.endswith('.mp4'):
            video_clip = process_video(file_path, target_resolution)
            clips.append(video_clip)

    #final_clip = concatenate_videoclips(clips, method="compose")
    output_file_path = f"sculptures/videos/{title}_{int(duration)}_{target_resolution[0]}x{target_resolution[1]}.mp4"

    #clips = [process_image(file_path, target_resolution) for file_path in file_list]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_file_path, fps=30)

if __name__ == "__main__":
    main()
