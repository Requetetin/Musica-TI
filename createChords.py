from PIL import Image
import webcolors
import colorsys

def rgb_to_hue(rgb):
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255

    h, s, l = colorsys.rgb_to_hls(r, g, b)

    hue = h * 360
    return hue


def cold_or_warm(rgb_list):
    warm_count = 0
    cold_count = 0
    none_count = 0
    for rgb in rgb_list:
        
        hue = rgb_to_hue(rgb)
        
        if 0 <= hue <= 60 or 300 < hue <= 360:
            warm_count += 1
        elif 120 <= hue <= 240:
            cold_count += 1
        else:
            none_count += 1       

    print(warm_count, cold_count, none_count)
    if(warm_count > cold_count):
        return 'warm'
    elif(cold_count > warm_count):
        return 'cold'
        

def average_colors_in_segments(image_path):
    img = Image.open(image_path)

    img = img.resize((int(img.width * (100 / img.height)), 100))

    segment_width = 20
    num_segments = img.width // segment_width

    avg_colors = []

    for i in range(num_segments):
        left = i * segment_width
        right = (i + 1) * segment_width

        if i == num_segments - 1:
            right = img.width

        segment = img.crop((left, 0, right, 100))

        non_black_pixels = [pixel for pixel in segment.getdata() if pixel != (0, 0, 0)]

        if non_black_pixels:
            avg_color = (
                sum(p[0] for p in non_black_pixels) // len(non_black_pixels),
                sum(p[1] for p in non_black_pixels) // len(non_black_pixels),
                sum(p[2] for p in non_black_pixels) // len(non_black_pixels)
            )
            avg_colors.append(avg_color)
        else:
            avg_colors.append((0, 0, 0))

    return avg_colors

image_path = "C:\\Users\\Lenovo Y40\\Desktop\\Musica-TI-main\\Barcodes\\Platformers\\Celeste.png"
colors = average_colors_in_segments(image_path)
print(colors)
print(cold_or_warm(colors))
