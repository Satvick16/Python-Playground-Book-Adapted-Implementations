"""
Steps:

1. Convert the input image to grayscale.

2. Split the image into M×N tiles.

3. Correct M (the number of rows) to match the image and font
aspect ratio.

4. Compute the average brightness for each image tile and then
look up a suitable ASCII character for each.

5. Assemble rows of ASCII character strings and print them to
a file to form the final image.
"""

# Pillow allows us to access image data

import numpy as np
from PIL import Image

# 70 level grayscale ramp
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`. "

# 10 levels grayscale ramp
gscale2 = "@%#*+=-:. "


def getAverageL(image):
    """
    Given PIL image, return average grayscale value of each tile
    """
    # get the image as a numpy array
    im = np.array(image)
    # get the dimensions
    w, h = im.shape
    # get the average
    return np.average(im.reshape(w*h))


def convertImageToAscii(fileName, cols, scale):
    """
    Given Image and dimensions (rows, cols), return a m*n list of Images
    """
    # declare globals
    global gscale1, gscale2
    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')
    # store image dimensions
    W, H = image.size[0], image.size[1]
    print(f"Input image dims: {W} x {H}")
    # compute tile width
    w = W/cols
    # compute tile height based on aspect ratio and scale of font
    h = w/scale
    # compute the number of rows to use in final grid
    rows = int(H/h)

    print(f"cols: {cols}, rows: {rows}")
    print(f"tile dims: {w} x {h}")

    print("Please wait...")

    # an ASCII image is a list of character strings
    aimg = []
    # generate the list of tile dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        # correct the last tile
        if j == rows-1:
            y2 = H
        # append an empty string
        aimg.append("")
        for i in range(cols):
            # crop the image to fit the tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
            # correct the last tile
            if i == cols-1:
                x2 = W
            # crop the image to extract tile into another Image object
            img = image.crop((x1, y1, x2, y2))
            # get the average luminance
            avg = int(getAverageL(img))
            # look up the ASCII character fr grayscale value (avg)
            gsval = gscale2[int((avg*9)/255)]
            # append the ASCII character to the string
            aimg[j] += gsval

    # return text image
    return aimg


def main():
    while True:
        # set output file
        outFile = 'out.txt'
        # set scale default as 0.43 which suits a Courier font
        scale = 0.43

        imgFile = str(input("Image to be converted: "))

        image = Image.open(imgFile).convert('L')
        cols = image.size[0]

        print('Generating ASCII art...')
        # convert image to ascii txt
        aimg = convertImageToAscii(imgFile, cols, scale)

        # open file
        f = open(outFile, 'w')
        # write to file
        for row in aimg:
            f.write(row + '\n')
        # cleanup
        f.close()
        print("ASCII art written to %s" % outFile)
        print("Image rendering is complete. You may now view your file.")
        x = input('Thank you for using ASCII ART. Would you like to render another image? (Y or N): ')
        if x == "y" or x == "Y":
            pass
        else:
            exit(0)


if __name__ == '__main__':
    main()
