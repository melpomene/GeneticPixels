""" This is the result that we want the genetic algorithm to do. """

from PIL import Image
from random import randint, random
def find_color_square(img):
    colors = img.getcolors(img.size[0]*img.size[1])
    r=0 
    g=0
    b=0
    for c in colors:
        r += c[0] * c[1][0]
        g += c[0] * c[1][1]
        b += c[0] * c[1][2]
    r = int(r / len(colors))
    g = int(g / len(colors))
    b = int(b / len(colors))
    return (r, g, b)

if __name__ == "__main__":
    original = Image.open("test_small.jpg")
    size = original.size
    new = Image.new("RGB", size)
    for x in range(0, size[0], 10):
        for y in range(0, size[1], 10):
            color = find_color_square(original.transform( (10, 10), Image.EXTENT, (x, y, x+10,y+10 ) ))
            new.putpixel((x,y),color)
            new.paste(color, (x,y,x+10,y+10))
    
    new.show()

