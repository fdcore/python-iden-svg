import struct
import hashlib
import math

class SvgNode:
    fillColor = ''
    strokeColor = ''
    strokeWidth = ''

class Svg(SvgNode):

    width = ''
    height = ''
    children = []

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def __str__(self):
        return '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{0}" height="{1}" viewBox="0 0 {0} {1}">{2}</svg>'.format(self.width, self.height, "\n".join(self.children))

class Rectangle(SvgNode):
    def  __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="{}" stroke-width="{}" />'.format(
            self.x,
            self.y,
            self.width,
            self.height,
            self.fillColor,
            self.strokeColor,
            self.strokeWidth
        )

class CircleSvg(SvgNode):
    def  __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    def __str__(self):
        return '<circle cx="{}" cy="{}" r="{}" fill="{}" stroke="{}" stroke-width="{}" />'.format(self.x, self.y, self.radius, self.fillColor, self.strokeColor, self.strokeWidth)

class Path(SvgNode):
    path = []

    def  __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = ['M {},{}'.format(x, y)]

    def lineTo(self, x, y, relative=False):
        relative = 'l' if relative else 'L'
        self.path.append('{} {},{}'.format(relative, x, y))

    def arcTo(self, x, y, xRadius, yRadius, xRotation, largeArc, sweepClockwise, relative = False):
        self.path.append(
            '{} {},{} {} {} {} {},{}'.format(
            'a' if relative else 'A',
            xRadius, yRadius, xRotation,
            1 if largeArc else 0,
            1 if sweepClockwise else 0,
            x,y))
    def __str__(self):
        return '<path fill="{}" stroke="{}" stroke-width="{}" d="{}" />'.format(self.fillColor, self.strokeColor, self.strokeWidth, ''.join(self.path))

class BaseGen:
    def getColorFromHex(self, hex_color):
        hex_color = hex_color.replace('#', '')
        return 'rgb'+str(struct.unpack('BBB', hex_color.decode('hex')))

    def getColor(self, hash_string):
        return self.getColorFromHex(hash_string[0:6])

class Pixel(BaseGen):
    def __init__(self, hash, color, size=480):
        self.svg = Svg(size, size)
        self.bgColor = color
        self.size = size
        self.fgColor = self.getColor(hash)
        self.svg.addChild(self.getBackground())

        for i in range(0, 5):
            for x in range(0, 5):
                if self.showPixel(i, x, hash):
                    self.svg.addChild(self.getPixel(i, x, self.fgColor))

    def getPixel(self, x, y, color):
        size_offset = self.size / 6
        size_padding = size_offset / 2
        r = Rectangle((x * size_offset) + size_padding, (y * size_offset) + size_padding, size_offset, size_offset)
        r.fillColor = color
        r.strokeWidth = 0

        return str(r)

    def showPixel(self, x, y, hash):
        min = 6 + abs(2-x) * 5 + y
        return int(hash[min:min+1], 16) % 2 == 0

    def render(self):
        return str(self.svg)

    def getBackground(self):
        r = Rectangle(0, 0, self.size, self.size)
        r.fillColor = self.bgColor
        r.strokeWidth = 0

        return str(r)

class Circle(BaseGen):
    sideLength = 1000

    def __init__(self, hash, color=(255, 255, 255), size = 1000):
        self.sideLength = size
        self.svg = Svg(self.sideLength, self.sideLength)
        self.bgColor = color
        self.fgColor = self.getColor(hash)
        self.svg.addChild(self.getBackground())

        if self.showCenter(hash):
            self.svg.addChild(self.getCenter(self.fgColor))

        for i in range(0, 4):
            self.svg.addChild(self.getArc(
                self.fgColor,
                self.getRadius(),
                self.getRadius(),
                self.getRingRadius(i),
                self.getRingAngle(i, hash),
                self.getRingWidth(),
                self.getRingRotation(i, hash)
            ))

    def getRadius(self):
        return self.sideLength / 2

    def getMultiplier(self):
        return self.sideLength / 1000

    def getCenterRadius(self):
        return 125 * self.getMultiplier()

    def getRingWidth(self):
        return 125 * self.getMultiplier()

    def getRingAngle(self, ring, hash):
        return 10 * pow(2, 3 - ring) * reduce(lambda total, step: int(total) + (int(step, 16) % 2), self.split2len(hash, pow(2, 3 - ring)), 0)

    def getRingRotation(self, ring, hash):
        return 36 * reduce(lambda total, step: int(total) + (int(step[ring-1], 16) % 2), self.split2len(hash[0:30], 3), 0)

    def getRingRadius(self, ring):
        return ring * 120 * self.getMultiplier()

    def render(self):
        return str(self.svg)

    def getBackground(self):
        c = CircleSvg(self.getRadius(), self.getRadius(), self.getRadius())
        c.fillColor = self.bgColor
        return str(c)

    def showCenter(self, hash):
        return int(hash[24:24+8], 16) % 2 == 0

    def getCenter(self, color):
        c = CircleSvg(self.getRadius(), self.getRadius(), self.getRadius())
        c.fillColor = self.bgColor
        return str(c)

    def split2len(self, s, n):
        def _f(s, n):
            while s:
                yield s[:n]
                s = s[n:]
        return list(_f(s, n))

    def getArc(self, color, x, y, radius, angle, width, start = 0):

        p = Path(x + radius * math.cos(math.radians(start)), y + radius * math.sin(math.radians(start)))

        p.fillColor = color
        p.strokeColor = color
        p.strokeWidth = 1

        p.arcTo(x + radius * math.cos(math.radians(start + angle)),
                y + radius * math.sin(math.radians(start + angle)),
                radius,
                radius,
                0,
                angle > 180,
                1)

        p.lineTo(
                x + (radius + width) * math.cos(math.radians(start + angle)),
                y + (radius + width) * math.sin(math.radians(start + angle))
            )

        p.arcTo(
                x + (radius + width) * math.cos(math.radians(start)),
                y + (radius + width) * math.sin(math.radians(start)),
                radius + width,
                radius + width,
                0,
                angle > 180,
                0
            )

        p.lineTo(
                x + radius * math.cos(math.radians(start)),
                y + radius * math.sin(math.radians(start))
        )

        return str(p)

class Iden:

    backgroundColor = 'rgb(255, 255, 255)'
    hash_string = ''
    type_iden = ''

    def __init__(self, text, type_iden='pixel', size=None):
        m = hashlib.md5()
        m.update(text)
        self.type_iden = type_iden
        self.size = size
        self.hash_string = m.hexdigest()

    def getColorFromHex(self, hex_color):
        hex_color = hex_color.replace('#', '')
        return 'rgb'+str(struct.unpack('BBB', hex_color.decode('hex')))

    def setBackgroundColor(self, hex_color):
        self.backgroundColor = self.getColorFromHex(hex_color)

    # generate and return svg code
    def getIcon(self):

        if self.type_iden == 'pixel':
            if not self.size:
                self.size = 480
            aid = Pixel(self.hash_string, self.backgroundColor, self.size)

        if self.type_iden == 'circle':
            if not self.size or self.size < 1000:
                self.size = 1000
            aid = Circle(self.hash_string, self.backgroundColor, self.size)

        return aid.render()

    def getColor(self, hash_string):
        return self.getColorFromHex(hash_string[0:6])

    # generate and save svg
    def save(self, file_path):
        f = open(file_path, 'w')
        f.write(self.getIcon())
        f.close()
