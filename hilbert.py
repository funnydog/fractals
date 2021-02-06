#!/usr/bin/env python3

import cairo
import math
import sys

def lsysgen(lsys, rules):
    out = []
    for x in lsys:
        out.append(rules.get(x, x))
    return ''.join(out)

def turn(angle):
    global dir
    dir += math.pi * angle / 180.

def move():
    global x, y, dir, cr, length
    x += math.cos(dir) * length
    y += math.sin(dir) * length
    cr.line_to(x, y)

def save():
    global stack, x, y, dir, length
    stack.append((x, y, dir, length))

def restore():
    global stack, x, y, dir, length, cr
    (x, y, dir, length) = stack.pop()
    cr.move_to(x, y)

def shorter(factor):
    global length
    length *= factor

def lsysdraw(axiom):
    for c in axiom:
        if c == 'f':
            move()
        elif c == 'S':
            shorter(0.4)
        elif c == 'r':
            turn(-90.)
        elif c == 'l':
            turn(+90.)
        elif c == '[':
            save()
        elif c == ']':
            restore()
        else:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <filename.pdf>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    #surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 128, 128)
    surface = cairo.PDFSurface(sys.argv[1], 72.0 * 21.0 / 2.54, 72 * 29.7 / 2.54)
    cr = cairo.Context(surface)

    # turtle graphics state
    stack = []
    x = 210. / 2.
    y = 217.
    dir = -math.pi / 2.
    length = 50.

    # convert to millimeters
    cr.scale(72. / 25.4, 72. / 25.4)

    # set some default values
    cr.set_source_rgb(0.0, 0.0, 0.0)
    cr.set_line_width(0.1)
    cr.move_to(x, y)

    gen = 6
    x = 20.
    y = 287.
    length = 20. * pow(0.5, gen-1)
    lsys = 'A'
    rules = {
        'A': 'lBfrAfArfBl',
        'B': 'rAflBfBlfAr',
    }

    for c in range(gen):
        lsys = lsysgen(lsys, rules)

    cr.move_to(x, y)

    lsysdraw(lsys)
    cr.stroke()
    surface.finish()
