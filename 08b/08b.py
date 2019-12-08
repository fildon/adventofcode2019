def get_pixels_from_file(file_name):
    file = open(file_name, "r")
    return file.read().strip()

def parse_encoded_image(pixels, height, width):
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
    return output

def render_parsed_image(image):
    # 0 is black, 1 is white, and 2 is transparent.
    for row in image:
        rendered_row = ''
        for pixel in row:
            if pixel == '0':
                rendered_row += ' '
            if pixel == '1':
                rendered_row += '@'
            if pixel == '2':
                rendered_row += '+'
        print(rendered_row)

encoded_pixels = get_pixels_from_file('input.txt')
image = parse_encoded_image(encoded_pixels, 6, 25)
render_parsed_image(image)
# SOLVED CYKBY
