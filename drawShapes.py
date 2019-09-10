from PIL import Image, ImageDraw, ImageFont, ImageColor
import math
#################
##INPUT FUNCTIONS
#################
def getPentagon(radius, flip=0, canvas=(0,0)):
    #RETURNS THE POINTS OF A PENTAGON, CAN FLIP ACROSS THE X-AXIS
    pi = math.pi
    if(canvas!=(0,0)):
        origin = canvas[0], canvas[1]
    else:
        origin = radius, radius
    c1 = int(radius*(math.sqrt(5)-1)/4)
    c2 = int(radius*(math.sqrt(5)+1)/4)
    s1 = int(radius*(math.sqrt(10 + (2 * math.sqrt(5)) ) )/4)
    s2 = int(radius*(math.sqrt(10 - (2 * math.sqrt(5)) ) )/4)
    if(flip):
        p1 = origin[0] - radius, origin[1]
        p2 = origin[0] - c1, origin[1] - s1
        p5 = origin[0] - c1, origin[1] + s1
        p3 = origin[0] + c2, origin[1] - s2
        p4 = origin[0] + c2, origin[1] + s2
    else:
        p1 = origin[0] + radius, origin[1]
        p2 = origin[0] + c1, origin[1] - s1
        p5 = origin[0] + c1, origin[1] + s1
        p3 = origin[0] - c2, origin[1] - s2
        p4 = origin[0] - c2, origin[1] + s2
    output = (radius,p1,p2,p3,p4,p5)
    return output

def buildImage(width, height):
    image = Image.new('RGBA', (width+1, height+1))
    return image

def buildImageR(radius):
    print("buildImageR (" + str(int(radius*2+1)) + ", " + str(int(radius*2+1)) + ")")
    radius = int(radius)
    image = Image.new('RGBA', (int(radius*2+1), int(radius*2+1)))
    return image



##################
##OUTPUT FUNCTIONS
##################
##TRIANGLES
def drawRightTriangle(*dims, outline=None, fill=None):
    image = buildImage(dims[0], dims[1])
    draw = ImageDraw.Draw(image)
    draw.polygon(((0,dims[1]),(dims[0],dims[1]),(dims[0],0)), outline=outline, fill=fill)
    return image

def drawIsoTriangle(w,h, outline=None, fill=None):
    image = buildImage(w,h)
    draw = ImageDraw.Draw(image)
    draw.polygon((0,h,w,h,w/2,0), outline=outline, fill=fill)
    return image

def drawEqTriangle(side, outline=None, fill=None):
    return drawIsoTriangle(side,side, outline=outline, fill=fill)

##RECTANGLES
def drawRectangle(w,h, outline=None, fill=None):
    image = buildImage(w,h)
    draw = ImageDraw.Draw(image)
    draw.rectangle(((0,0),(w,h)), outline=outline, fill=fill)
    return image

def drawSquare(side, outline=None, fill=None):
    return drawRectangle(side,side,outline=outline, fill=fill)

##PENTAGON
def drawPentagon(radius, flip=0, canvas=(0,0), outline=None, fill=None):
    pentagon = getPentagon(radius, flip, canvas)
    image = buildImageR(radius)
    draw = ImageDraw.Draw(image)
    draw.polygon((pentagon[1],pentagon[2],pentagon[3],pentagon[4],pentagon[5],), outline=outline, fill=fill)
    return image

##PENTAGRAM
def drawPentagram(radius, flip=0, outline=None, fill=None):
    pentagon = getPentagon(radius, flip)
    #print(pentagon)
    radius = pentagon[0]
    circ = drawCircle(radius, outline=outline, fill=fill)
    image = buildImageR(radius)
    draw = ImageDraw.Draw(image)
    draw.polygon((pentagon[1],pentagon[3],pentagon[5],pentagon[2],pentagon[4],), outline=outline, fill=fill)
    image = image.rotate(90,expand=True)
    image = Image.alpha_composite(circ, image)
    return image

##STAR
def drawStar(*radius, flip=0, outline=None, fill=None):
    o = getPentagon(radius[0], flip)
    i = getPentagon(radius[0]/2.63, not(flip), (radius[0],radius[0]))
    #pent1 = drawPentagon(o)
    #pent2 = drawPentagon(i,radius)
    image = buildImageR(radius[0])
    draw = ImageDraw.Draw(image)
    draw.polygon((o[5],i[5],o[4],i[1],o[3],i[2],o[2],i[3],o[1],i[4]), outline=outline, fill=fill)
    #image = Image.alpha_composite(image,pent1)
    #image = Image.alpha_composite(image,pent2)
    image = image.rotate(90,expand=True)
    return image

##OCTAGON
def drawOctagon(radius, outline=None, fill=None):
    image = buildImageR(radius)
    draw = ImageDraw.Draw(image)
    offset = (radius*math.sqrt(2)/2)

    p1 = (2*radius, radius)
    p2 = (radius+offset, radius-offset)
    p3 = (radius, 0)
    p4 = (radius-offset, radius-offset)
    p5 = (0, radius)
    p6 = (radius-offset, radius+offset)
    p7 = (radius, 2*radius)
    p8 = (radius+offset, radius+offset)

    draw.polygon((p1,p2,p3,p4,p5,p6,p7,p8), outline=outline, fill=fill)
    return image

##CIRCLE
def drawCircle(radius, canvas=(0,0), outline=None, fill=None):
    if(canvas==(0,0)):
        image = buildImageR(radius)
    else:
        image = buildImage(canvas[0],canvas[1])
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 2*radius, 2*radius), outline=outline, fill=fill)
    return image

##LOCK
def drawLock(w,h, outline=None, fill=None):
    image = drawCircle(int(w/2),(w,h), outline=outline, fill=fill)
    image2 = drawIsoTriangle(w,h, outline=outline, fill=fill)
    imgSize = image.size
    img2Size = image2.size
    print(imgSize, img2Size)
    image = Image.alpha_composite(image, image2)
    return image

##ARC
def drawChord(xy,start, end, outline=None, fill=None):
    image = buildImage(xy[2],xy[3])
    draw = ImageDraw.Draw(image)
    draw.chord(xy, start, end, fill=fill)
    return image

def bezier(*whxy, curve_smoothness=100, outline=None, fill=None):
    image = buildImage(whxy[0],whxy[1])
    draw = ImageDraw.Draw(image)

    #First, select start and end of curve (pixels)
    curve_start = [(whxy[3],whxy[4])]
    curve_end = [(whxy[5],whxy[6])]

    #Second, split the path into segments
    curve = []
    for i in range(1,curve_smoothness,1):
        split = (curve_end[0][0] - curve_start[0][0])/curve_smoothness
        x = curve_start[0][0] + split * i
        curve.append((x, -7 * math.pow(10,-7) * math.pow(x,3) - 0.0011 * math.pow(x,2) + 0.235 * x + 682.68))

    #Third, edit any other corners of polygon
    other =[(1026,721), (167,688)]

    #Finally, combine all parts of polygon into one list
    xys = curve_start + curve + curve_end + other #putting all parts of the polygon together
    draw.polygon(xys, fill = None, outline = 256)
    return image

##HEART

##CLUB

##DIAMOND

##SPADE

##TEAR

##FLEUR



##TEST OUTPUT
testBezier = bezier()
testBezier.save('testBezier.png')

# TestChord = drawChord([0,0,50,50], 150, 360, fill='red')
# TestChord.save('testChord.png')

# TestRT = drawRightTriangle(300,500, fill='black')
# TestRT.save('testRightTriangle.png')
#
# TestIT = drawIsoTriangle(300,500, fill='black')
# TestIT.save('testIsoTriangle.png')
#
# TestET = drawEqTriangle(300, fill='black')
# TestET.save('testEqTriangle.png')
#
# TestRec = drawRectangle(300,500, fill='black')
# TestRec.save('testRectangle.png')
#
# TestSquare = drawSquare(300, fill='black')
# TestSquare.save('testSquare.png')
#
# TestPentagon = drawPentagon(150, fill='black')
# TestPentagon.save('testPentagon.png')
#
# TestPentagram = drawPentagram(150, outline='black', flip=1)
# TestPentagram.save('testPentagram.png')
#
# TestStar = drawStar(300, fill='black')
# TestStar.save('testStar2.png')
#
# TestOctagon = drawOctagon(200, fill='black')
# TestOctagon.save('testOctagon.png')
#
# TestLock = drawLock(250,500, fill='black')
# TestLock.save('testLock.png')
