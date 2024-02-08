from PIL import Image
from os import scandir

count: int = 0

def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, 1

    # RGB [0,255] -> CMYK [0,1]
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    # Extract the black component
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # CMYK [0,1] -> CMYK [0,100]
    return c*100, m*100, y*100, k*100

def cmyk_to_rgb(c, m, y, k):
    # CMYK [0,100] -> CMYK [0,1]
    c = c / 100
    m = m / 100
    y = y / 100
    k = k / 100

    # CMYK -> RGB
    r = 255 * (1-c) * (1-k)
    g = 255 * (1-m) * (1-k)
    b = 255 * (1-y) * (1-k)

    return round(r), round(g), round(b)

def cap(currentvalue, maxvalue):
    if currentvalue > maxvalue:
        return maxvalue
    else:
        return currentvalue

for f in scandir("./input/"):
    if f.is_file() and f.name.endswith("png"):

        print("ALPHAZING " + f.name + "...")
               
        # Open the source image
        source_image = Image.open(f.path)

        # Create a new image with alpha channel
        result_image = Image.new("RGBA", source_image.size)

        # Iterate over each pixel in the image
        for xpos in range(source_image.width):
            for ypos in range(source_image.height):

                r, g, b, a = source_image.getpixel((xpos,ypos))
                result_image.putpixel((int(xpos), int(ypos)), (r, g, b, max(r, g, b)))
                
                
        # Save the result image with alpha
        result_image.save("./output/" + f.name)

        print("CONVERTED " + f.name)

        count += 1

if count == 0:
    print("no png images to convert were found")
else:
    print(str(count) + " images were converted")
