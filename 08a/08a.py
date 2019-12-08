file = open("input.txt", "r")

pixels = file.read(25 * 6).strip()
leastzeroes = None
checksum = None
while len(pixels) > 0:
    zeroes = 0
    ones = 0
    twos = 0
    for pixel in pixels:
        if pixel == "0":
            zeroes += 1
        if pixel == "1":
            ones += 1
        if pixel == "2":
            twos += 1
    if leastzeroes is None or zeroes < leastzeroes:
        leastzeroes = zeroes
        checksum = ones * twos
    pixels = file.read(25 * 6).strip()

print(checksum)
# Solved 2176
