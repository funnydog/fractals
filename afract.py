#!/usr/bin/env python3
# inspired by https://archive.org/details/LIST1989-05/page/n43

import cairo
import math
import sys

# width and height of A4 in dpi
WIDTH = 72.0 * 21.0 / 2.54
HEIGHT = 72.0 * 29.7 / 2.54

# parameters for the fractal
min_len   = 1.0                    # minimum length of the branch
cur_len   = 20.0                   # current length of the branch
decay     = 0.8                    # ratio of branch decay
br_angle  = math.radians(30)       # branch angle
cur_angle = math.radians(90)       # current angle

def draw_tree(lvl, cur_angle, cur_len, x, y):
    global context, br_angle, min_len, decay

    c = lvl / 14.0
    context.set_source_rgb(c, c, c)
    context.move_to(x, y)
    x -= math.cos(cur_angle) * cur_len
    y -= math.sin(cur_angle) * cur_len
    context.line_to(x, y)
    context.stroke()

    cur_len *= decay
    if cur_len > min_len:
        draw_tree(lvl+1, cur_angle - br_angle, cur_len, x, y)
        draw_tree(lvl+1, cur_angle + br_angle, cur_len, x, y)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <filename.pdf>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    # create the surface and context
    surface = cairo.PDFSurface(sys.argv[1], WIDTH, HEIGHT)
    context = cairo.Context(surface)

    # convert the coordinates to millimeters
    context.scale(72.0 / 25.4, 72.0 / 25.4)

    # set the line color and width
    context.set_source_rgb(0.0, 0.0, 0.0)
    context.set_line_width(0.1)

    # move to the origin
    x = 210.0 / 2.0
    y = 297.0 / 2.0
    context.move_to(x, y)

    # draw the tree
    draw_tree(0, cur_angle, cur_len, x, y)

    # stroke the drawings and save the file
    surface.finish()
