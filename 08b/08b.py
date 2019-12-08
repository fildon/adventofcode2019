file = open("input.txt", "r")
pixels = file.read().strip()

width = 25
height = 6
layer_size = width * height

output = [['2' for x in range(width)] for y in range(height)]

while len(pixels) >= layer_size:
    pixel_batch = pixels[:layer_size]
    pixels = pixels[layer_size:]
    for i in range(len(pixel_batch)):
        x = i % width
        y = i // width
        if output[y][x] == '2' and pixel_batch[i] != '2':
            output[y][x] = pixel_batch[i]

# 0 is black, 1 is white, and 2 is transparent.
for row in output:
    rendered_row = ''
    for pixel in row:
        if pixel == '0':
            rendered_row += ' '
        if pixel == '1':
            rendered_row += '@'
        if pixel == '2':
            rendered_row += '+'
    print(rendered_row)

# SOLVED CYKBY
