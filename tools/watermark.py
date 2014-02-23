# -*- coding: utf-8 -*-
import Image, ImageDraw, ImageFont, uuid
import os

import ImageEnhance


POSITION = ('LEFTTOP','RIGHTTOP','CENTER','LEFTBOTTOM','RIGHTBOTTOM', 'CENTERTOP', 'CENTERBOTTOM')
PADDING = 5
MARKIMAGE = 'water.png'

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(imagefile, markfile, position=POSITION[4], opacity=1):
    """Adds a watermark to an image."""    
    im = Image.open(imagefile)
    mark = Image.open(markfile)    
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'title':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    elif position == POSITION[0]:
        #lefttop
        position = (PADDING,PADDING)
        layer.paste(mark, position)
    elif position == POSITION[1]:
        #righttop
        position = (im.size[0] - mark.size[0]-PADDING, PADDING)
        layer.paste(mark, position)
    elif position == POSITION[2]:
        #center
        position = ((im.size[0] - mark.size[0])/2,(im.size[1] - mark.size[1])/2)
        layer.paste(mark, position)
    elif position == POSITION[3]:
        #left bottom
        position = (PADDING,im.size[1] - mark.size[1]-PADDING,)
        layer.paste(mark, position)

    elif position == 'CENTERBOTTOM':
        #center bottom
        position = ((im.size[0] - mark.size[0])/2, im.size[1] - mark.size[1]-PADDING,)
        layer.paste(mark, position)
    elif position == 'CENTERTOP':
        #center bottom
        position = ((im.size[0] - mark.size[0])/2, PADDING,)
        layer.paste(mark, position)
    else:
        #right bottom (default)
        position = (im.size[0] - mark.size[0]-PADDING, im.size[1] - mark.size[1]-PADDING,)
        layer.paste(mark, position)
        
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)



def text2png(text):
    # config:
    adTexts = ['---------------', 'http://www.planabc.net']
    imgBg = '#FFFFFF'
    textColor = "#000000"
    adColor = "#FF0000"
    ttf = "H:\Windows\Fonts\STXIHEI.TTF"
    fontSize = 20
    tmp = 'tmp/'

    # Build rich text for ads
    ads = []
    for adText in adTexts:
        ads += [(adText.decode('utf-8'), adColor)]

    # Format wrapped lines to rich text
    bodyTexts = [""]
    l = 0
    # x.decode() ==> unicode
    for character in text.decode('utf-8'):
        c = character
        delta = len(c)
        if c == '\n':
            bodyTexts += [""]
            l = 0
        elif l + delta > 40:
            bodyTexts += [c]
            l = delta
        else:
            bodyTexts[-1] += c
            l += delta

    body = [(text, textColor) for text in bodyTexts]
    body += ads

    # Draw picture
    img = Image.new("RGB", (330, len(body) * fontSize + 5), imgBg)
    # Ref: http://blog.163.com/zhao_yunsong/blog/static/34059309200762781023987/
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(ttf, fontSize)
    for num, (text, color) in enumerate(body):
        draw.text((2, fontSize * num), text, font=font, fill=color)

    # Write result to a temp file
    filename = uuid.uuid4().hex + ".png"
    file = open(tmp + filename, "wb")
    img.save(file, "PNG")

    return tmp + filename

def text2image():
    text = u"???????????????????????????test 123???"
    im = Image.new("RGB", (300, 50), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("H:/Windows/Fonts", "STXIHEI.TTF"), 14)
     
    dr.text((10, 5), text, font=font, fill="#000000")
    im.show()
    im.save("t.png")



if __name__ == "__main__":
    #watermark("old.jpg",MARKIMAGE,POSITION[4],opacity=1).save("new.jpg",quality=90)
    # text2png("keep")
    text2image()
