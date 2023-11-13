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

def rgb_to_hsl(rgb):
    r = rgb[0] / 255
    g = rgb[1] / 255
    b = rgb[2] / 255
    
    h, s, l = colorsys.rgb_to_hls(r, g, b)
    
    return round(h * 255), round(s * 255), round(l * 255)


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

def get_scale_notes(scale):
    scale_notes = {
        'c minor': ['C', 'DS', 'G'],
        'c major': ['C', 'E', 'G'],
        'c# minor': ['CS', 'E', 'GS'],
        'c# major': ['CS', 'ES', 'GS'],
        'd minor': ['D', 'F', 'A'],
        'd major': ['D', 'FS', 'A'],
        'd# minor': ['DS', 'FS', 'AS'],
        'd# major': ['DS', 'G', 'AS'],
        'e minor': ['E', 'G', 'B'],
        'e major': ['E', 'GS', 'B'],
        'f minor': ['F', 'GS', 'C'],
        'f major': ['F', 'A', 'C'],
        'f# minor': ['FS', 'A', 'CS'],
        'f# major': ['FS', 'AS', 'CS'],
        'g minor': ['G', 'AS', 'D'],
        'g major': ['G', 'B', 'D'],
        'g# minor': ['GS', 'B', 'DS'],
        'g# major': ['GS', 'BS', 'DS'],
        'a minor': ['A', 'C', 'E'],
        'a major': ['A', 'CS', 'E'],
        'a# minor': ['AS', 'CS', 'ES'],
        'a# major': ['AS', 'CS', 'ES'],
        'b minor': ['B', 'D', 'FS'],
        'b major': ['B', 'DS', 'FS'],
    }
    return scale_notes.get(scale)

def build_chord(colors):
    chord_progression = []
    durations = []
    for color in colors:
        h, s, l = rgb_to_hsl(color)
        octave = None
        base_note = None
        if 0 <= h <= 60 or 300 < h <= 360 or 120 <= h <= 240:
            if(h <= 30):
                base_note = 'c'
            elif (h > 30 and h <=60):
                base_note = 'c#'
            elif (h > 60 and h <=90):
                base_note = 'd'
            elif (h > 90 and h <=120):
                base_note = 'd#'
            elif (h > 120 and h <=150):
                base_note = 'e'
            elif (h > 150 and h <=180):
                base_note = 'f'
            elif (h > 180 and h <=210):
                base_note = 'f#'
            elif (h > 210 and h <=240):
                base_note = 'g'
            elif (h > 240 and h <=270):
                base_note = 'g#'
            elif (h > 270 and h <=300):
                base_note = 'a'
            elif (h > 300 and h <=330):
                base_note = 'a#'
            elif (h > 330 and h <=360):
                base_note = 'b'

            if 0 <= h <= 60 or 300 < h <= 360:
                base_note += ' major'
            elif 120 <= h <= 240:
                base_note += ' minor'

            scale_notes = get_scale_notes(base_note)

            if s <= 84:
                durations.append('TN')
            elif s > 84 and s <= 169:
                durations.append('SN')
            elif s > 169 and s <= 255:
                durations.append('EN')
                
            if l <= 24:
                octave = '_1'
            elif l > 24 and l <= 50:
                octave = '0'
            elif l > 50 and l <= 75:
                octave = '1'
            elif l > 75 and l <= 101:
                octave = '2'
            elif l > 101 and l <= 126:
                octave = '3'
            elif l > 126 and l <= 152:
                octave = '4'
            elif l > 152 and l <= 177:
                octave = '5'
            elif l > 177 and l <= 203:
                octave = '6'
            elif l > 203 and l <= 228:
                octave = '7'
            elif l > 228:
                octave = '8'

            for i in range(3):
                scale_notes[i] = scale_notes[i] + octave
                
            chord_progression.append(scale_notes)
        else:
            chord_progression.append('REST')
            if s <= 84:
                durations.append('TN')
            elif s > 84 and s <= 169:
                durations.append('SN')
            elif s > 169 and s <= 255:
                durations.append('EN')
        
        
        
    return chord_progression, durations
    

image_path = os.path.join( 'Barcodes', 'Roguelikes', 'Hades.png')
colors = average_colors_in_segments(image_path)
print(colors)
scale = get_scale(colors)
print(scale)
chords, durations = build_chord(colors)
print(len(chords), chords)
print(len(durations), durations)
f = open("chords.txt", "w")
for chord in chords:
    str_chord = str(chord)
    str_chord = str_chord.replace('[', '').replace(']', '').replace(' ', '').replace('\'', '')
    f.write(str_chord)
    f.write('\n')
f.close()

f = open("durations.txt", "w")
for duration in durations:
    f.write(str(duration))
    f.write('\n')
f.close()
