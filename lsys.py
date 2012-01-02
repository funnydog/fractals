#!/usr/bin/env python2
#coding=utf8

import cairo, math, random

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
        if c == 'F':
            move()
        elif c == 'S':
            shorter(0.4)
        elif c == '+':
            turn(-60.)
        elif c == '-':
            turn(+60.)
        elif c == '[':
            save()
        elif c == ']':
            restore()
        else:
            pass

#surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 128, 128)
surface = cairo.PDFSurface('file.pdf', 72.0 * 21.0 / 2.54, 72 * 29.7 / 2.54)
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

# l-system axiom (initial condition) and rules
# lsys = 'FX'
# rules = {
#     'X': 'S[-FX]+FX',
# }
# generate n times
# for c in xrange(15):
#     lsys = lsysgen(lsys, rules)

# lsysdraw(lsys)
# cr.stroke()
# surface.finish()

gen = 6
x = 210. - 20.
y = 80.
length = 20. * pow(0.5, gen-1)
lsys = 'FXF--FF--FF'
rules = {
    'X': 'X+YF++YF-FX--FXFX-YF+',
    'Y': '-FX+YFYF++YF+FX--FX-Y',
}

for c in xrange(gen):
    lsys = lsysgen(lsys, rules)

cr.move_to(x, y)

lsysdraw(lsys)
cr.stroke()
surface.finish()
