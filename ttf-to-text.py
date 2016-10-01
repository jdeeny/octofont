import string
from PIL import ImageFont, ImageDraw
from itertools import chain


def find_max_height(font, glyphs):
    max_height = 0
    for g in glyphs:
        bitmap = font.getmask(g, "1")
        bbox = bitmap.getbbox()
        if bbox != None:
            x1, y1, x2, y2 = bbox
            max_height = max(y2-y1, max_height)
    return max_height

def find_max_width(font, glyphs):
    max_width = 0
    for g in glyphs:
        bitmap = font.getmask(g, "1")
        bbox = bitmap.getbbox()
        if bbox != None:
            x1, y1, x2, y2 = bbox
            max_width = max(x2-x1, max_width)
    return max_width



def print_character(font, glyph, max_height):
    bitmap = font.getmask(glyph, "1")
    bbox = bitmap.getbbox()
    comment = "# " + glyph + " (ASCII: " + str(ord(glyph)) + ")"

    if bbox == None:
        print comment, "skipping empty glyph"
        print
        return

    x1, y1, x2, y2 = bbox

    pre = 0
    post = 0

    extra = max_height - (y2-y1)
    if glyph in vert_center:
        comment += " (centered)"
        post = extra / 2
        pre = extra - post
    elif glyph in vert_top:
        comment += " (align-top)"
        post = extra
        # Move one pixel down from the top if the glyph is really short
        if post > (y2 - y1):
            post -= 1
            pre = 1
    else:
        comment += " (align-bot)"
        pre = extra

    #print comment

    print str(ord(glyph)) + " " + str(x2-x1) + " " + comment

    for i in range(pre):
        print "." * (x2-x1)

    for y in range(y1, y2):
        s = ""
        for x in range(x1, x2):
            if bitmap.getpixel((x,y)) > 0:
                s += "X"
            else:
                s += "."
        print s
    for i in range(post):
        print "." * (x2-x1)

    print


vert_center = "~=%!#$()*+/<>@[]\{\}|"
vert_top = "^\"\'`"

font_file = "Small_5x3/small_5x3.ttf"
font_points = 8
font_glyphs = string.printable
exclude = set(chr(i) for i in chain(range(0, 31), range(128, 255)))
font_glyphs = ''.join(ch for ch in font_glyphs if ch not in exclude)

font = ImageFont.truetype(font_file, font_points)

max_height = find_max_height(font, font_glyphs)
max_width = find_max_height(font, font_glyphs)


print "# " + font_file + ", " + str(font_points) + " points, height " + str(max_height) + " px, widest " + str(max_width) + " px"
print "# Exporting: " + font_glyphs
print

for glyph in font_glyphs:
    print_character(font, glyph, max_height)
