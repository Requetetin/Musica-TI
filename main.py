import cv2

def process_video (input_movie, size=(2000,100)):
    colours = []

    # Takes the frames of the video
    cap = cv2.VideoCapture(input_movie)
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            continue

        # Processes the frame
        colours_frame = process_frame(frame, size[1])
        colours.append(colours_frame)
    
    # Generates the final picture
    generate_pic(colours, size)

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

def generate_pic (colours, size):
    # Generates the picture
    height = size[1]
    img = np.zeros((height,len(colours),3), np.uint8)

    # Puts the colours in the image
    for x in range(0, len(colours)):
        for y in range(0, height):
            img[y,x,:] = colours[x][y,0]

    # Converts back to RGB
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    cv2.imwrite("barcode_full.png", img)

import pafy

# Download the video
video = pafy.new('https://www.youtube.com/watch?v=2GD7T9FgLRk')
resolution = video.getbestvideo(preftype="mp4")
input_movie = resolution.download(quiet=False)

# Process it
process_video(input_movie)
os.remove(input_movie)