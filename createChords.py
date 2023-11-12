from PIL import Image
import colorsys
import os


def rgb_to_hue(rgb):
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255

    h, s, l = colorsys.rgb_to_hls(r, g, b)

    hue = h * 360
    return hue


def get_scale(rgb_list):
    warm_count = 0
    cold_count = 0
    none_count = 0

    notes = [{'c': 0},{'c#': 0},{'d': 0},{'d#': 0},{'e': 0},{'f': 0},{'f#': 0},{'g': 0},{'g#': 0},{'a': 0},{'a#': 0},{'b': 0}]

    for rgb in rgb_list:
        
        hue = rgb_to_hue(rgb)
        
        if 0 <= hue <= 60 or 300 < hue <= 360:
            warm_count += 1
        elif 120 <= hue <= 240:
            cold_count += 1
        else:
            none_count += 1    

        if(hue <= 30):
            notes[0]['c'] += 1
        elif (hue > 30 and hue <=60):
            notes[1]['c#'] += 1
        elif (hue > 60 and hue <=90):
            notes[2]['d'] += 1
        elif (hue > 90 and hue <=120):
            notes[3]['d#'] += 1
        elif (hue > 120 and hue <=150):
            notes[4]['e'] += 1
        elif (hue > 150 and hue <=180):
            notes[5]['f'] += 1
        elif (hue > 180 and hue <=210):
            notes[6]['f#'] += 1
        elif (hue > 210 and hue <=240):
            notes[7]['g'] += 1
        elif (hue > 240 and hue <=270):
            notes[8]['g#'] += 1
        elif (hue > 270 and hue <=300):
            notes[9]['a'] += 1
        elif (hue > 300 and hue <=330):
            notes[10]['a#'] += 1
        elif (hue > 330 and hue <=360):
            notes[11]['b'] += 1
        
        sorted_notes = sorted(notes, key=lambda x: list(x.values())[0], reverse=True)
        most_common = list(sorted_notes[0].keys())[0]

    print(f'Warm Count: {warm_count}, Cold Count: {cold_count}, None Count: {none_count}')
    if(warm_count > cold_count):
        return most_common + ' major'
    elif(cold_count > warm_count):
        return most_common + ' minor'
        

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

        non_black_pixels = [pixel for pixel in segment.getdata() if not(pixel[0] <= 45 and pixel[1] <= 45 and pixel[2] <= 45)]

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

image_path = os.path.join( 'Barcodes', 'Platformers', 'Celeste.png')
colors = average_colors_in_segments(image_path)
print(colors)
print(get_scale(colors))
