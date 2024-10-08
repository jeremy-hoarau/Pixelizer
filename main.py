import cv2
import numpy as np
from pathlib import Path

def get_closest_color(colors, color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))
    closest_color = colors[index_of_smallest][0]
    return closest_color

# PARAMS --------------------------------
pixelation = 128
last_color_palette_index = 7
img_index = 14
use_palette = True
save_image = True
saved_image_name = "sakura_landscape"
override_existing_files = True
# ---------------------------------------

#loop on each palette to have different renders
for palette_index in range(last_color_palette_index + 2):
    if(palette_index != last_color_palette_index + 1):
        color_palette = []
        color_palette_img = cv2.imread('./color_palettes/color_palette_' + str(palette_index) + '.png')
        for y in range(color_palette_img.shape[0]):
            for x in range(color_palette_img.shape[1]):
                color_palette.append(color_palette_img[y][x])

    image = cv2.imread('./input/img_'+str(img_index)+'.png')
    image = cv2.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
    resolution = image.shape        # y - x - channels
    target_resolution = int(resolution[0]/pixelation)

    cv2.imshow('input image', image)

    new_img = np.zeros((resolution[0], resolution[1], 3), dtype=np.uint8)

    offset = [0, 0]

    while(offset[0] < resolution[0] and offset[1] < resolution[1]):
        pixel_sum = (0, 0, 0)
        pixels_skipped = 0
        for y in range(target_resolution):
            for x in range(target_resolution):
                if(len(image) > offset[0]+y and len(image[offset[0]+y]) > offset[1]+x):
                    pixel_sum += image[offset[0]+y][offset[1]+x]
                else:
                    pixels_skipped += 1
        total_pixels = (target_resolution*target_resolution)-pixels_skipped
        if(total_pixels > 0):
            new_pixel = tuple(pi/total_pixels for pi in pixel_sum)
        else:
            new_pixel = pixel_sum

        if use_palette and palette_index != last_color_palette_index + 1:
            #apply color palette
            color = [new_pixel[0], new_pixel[1], new_pixel[2]]
            new_pixel = get_closest_color(color_palette, color)

        for y in range(target_resolution):
            for x in range(target_resolution):
                if(len(new_img) > offset[0]+y and len(new_img[offset[0]+y]) > offset[1]+x):
                    new_img[offset[0]+y][offset[1]+x] = new_pixel

        offset[0] += target_resolution
        if(offset[0] >= resolution[0]):
            offset[0] = 0
            offset[1] += target_resolution

    cv2.imshow('render ' + str(palette_index), new_img)
    if(save_image):
        img_name = saved_image_name+"_"+str(palette_index)+".png"
        path = Path('./output/'+img_name)
        if override_existing_files == False and path.is_file():
            print("Error: file already exists")
        else:
            cv2.imwrite("./output/"+saved_image_name+"_"+str(palette_index)+".png", new_img)
            print("Image saved")

cv2.waitKey(0)