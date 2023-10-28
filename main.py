import cv2
import os

from pytube import YouTube
from moviepy.editor import VideoFileClip

def process_video (input_movie, title, size=(2000,100)):
    colours = []
    counter = 0

    # Takes the frames of the video
    cap = cv2.VideoCapture(input_movie)
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            print(flag)
            break

        # Processes the frame
        colours_frame = process_frame(frame, size[1])
        colours.append(colours_frame)
    print('WWOOOOO')
    # Generates the final picture
    generate_pic(colours, size, title)

import numpy as np
import colorsys

def process_frame (frame, height=100):
    # Resize and put in a single line
    image = resize_image(frame)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    image = image.reshape((image.shape[0] * image.shape[1], 1, 3))
    
    # Sort the pixels
    sorted_idx = np.lexsort(    (image[:,0,2], image[:,0,1], image[:,0,0]  )   )
    image = image[sorted_idx]

    # Resize into a column
    image_column = cv2.resize(image, (1, height), interpolation=cv2.INTER_AREA)
    return image_column

def resize_image (image, size=100):
    # Resize it
    h, w, _ = image.shape
    w_new = int(size * w / max(w, h) )
    h_new = int(size * h / max(w, h) )
     
    image = cv2.resize(image, (w_new, h_new));
    return image

def generate_pic (colours, size, title):
    print('HERE')
    # Generates the picture
    height = size[1]
    img = np.zeros((height,len(colours),3), np.uint8)

    # Puts the colours in the image
    for x in range(0, len(colours)):
        for y in range(0, height):
            img[y,x,:] = colours[x][y,0]

    # Converts back to RGB
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    cv2.imwrite(title + ".png", img)


# Download the video
url = 'https://www.youtube.com/watch?v=GZLkZ03vYgk'
title = 'EtG Speedrun Any (0635) [WR]'

# Initialize a YouTube object
yt = YouTube(url)
print('CP1')

# Choose the highest resolution stream
video_stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
print('CP2')

# Download the video
video_stream.download(output_path='VIDEO_TITLE')
print('CP3')

# Define the input and output file paths
input_path = './VIDEO_TITLE/' + title + '.mp4'
output_path = './VIDEO_TITLE/download.mp4'

# Load the video using moviepy
video_clip = VideoFileClip(input_path)

# # Convert the video to MP4 format
video_clip.write_videofile(output_path, codec='libx264')

print(f"Video downloaded and converted to {output_path}")

# Process it
process_video(output_path, title)
print('CP4')
#os.remove(output_path)
