from dxfwrite import DXFEngine as dxf
from enum import Enum
import random


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def empty_drawing():
    drawing = dxf.drawing()
    drawing.add_layer('cut', color=1)
    drawing.add_layer('mark', color=5)
    drawing.add_layer('engrave', color=3)
    return drawing


def tile(width, height, offsetX=0, offsetY=0, drawing=None, allNegative=False):
    if drawing is None:
        drawing = empty_drawing()
    entities = []
    for x in range(0, width):
        px = 32 * x + offsetX
        xDir = Direction.NORTH if x % 2 == 0 else Direction.SOUTH
        for y in range(0, height):
            yDir = Direction.WEST if y % 2 == 0 else Direction.EAST
            py = 32 * y + offsetY
            # right
            if x == width - 1:
                right = notchedLine(px + 32, py, yDir)
                if allNegative:
                    right = notchedLine(px + 32, py, Direction.EAST)
                entities.append(right)
            # top
            if y == height - 1:
                top = notchedLine(px, py + 32, xDir)
                if allNegative:
                    top = notchedLine(px, py + 32, Direction.NORTH)
                entities.append(top)
            # bottom
            bottom = dxf.line((px, py), (px + 32, py), layer='mark')
            if y == 0:
                bottom = notchedLine(px, py, xDir)
                if allNegative:
                    bottom = notchedLine(px, py, Direction.SOUTH)
            entities.append(bottom)
            # left
            left = dxf.line((px, py), (px, py + 32), layer='mark')
            if x == 0:
                left = notchedLine(px, py, yDir)
                if allNegative:
                    left = notchedLine(px, py, Direction.WEST)
            entities.append(left)
            # circles
            entities.append(dxf.circle(
                            radius=1.5,
                            center=(px + 4, py + 4),
                            layer='engrave'))
            entities.append(dxf.circle(
                            radius=1.5,
                            center=(px + 28, py + 28),
                            layer='engrave'))
    for entity in entities:
        drawing.add(entity)
    return drawing


def base(width, height, offsetX=0, offsetY=0, drawing=None):
    if drawing is None:
        drawing = empty_drawing()
    entities = []

    for x in range(0, width):
        px = 32 * x + offsetX
        for y in range(0, height):
            py = 32 * y + offsetY
            if x == 0:
                entities.append(notchedLine(px, py, Direction.WEST))
            if y == 0:
                entities.append(notchedLine(px, py, Direction.SOUTH))
            if x == width - 1:
                entities.append(notchedLine(px, py, Direction.EAST))
            if y == height - 1:
                entities.append(notchedLine(px, py, Direction.NORTH))

    for entity in entities:
        drawing.add(entity)
    return drawing


def notchedLine(x, y, direction=Direction.SOUTH, depth=4, width=8):
    line = dxf.polyline(layer='cut')
    if direction == Direction.NORTH:
        points = [
            (x,                             y),
            (x + 16 - width / 2,            y),
            (x + 16 - width / 2 - depth,    y - depth),
            (x + 16 + width / 2 + depth,    y - depth),
            (x + 16 + width / 2,            y),
            (x + 32,                        y)
        ]
    elif direction == Direction.WEST:
        points = [
            (x,                             y),
            (x,                             y + 16 - width / 2),
            (x + depth,                     y + 16 - width / 2 - depth),
            (x + depth,                     y + 16 + width / 2 + depth),
            (x,                             y + 16 + width / 2),
            (x,                             y + 32)
        ]
    elif direction == Direction.EAST:
        points = [
            (x,                        y),
            (x,                        y + 16 - width / 2),
            (x - depth,                y + 16 - width / 2 - depth),
            (x - depth,                y + 16 + width / 2 + depth),
            (x,                        y + 16 + width / 2),
            (x,                        y + 32)
        ]
    else:  # SOUTH
        points = [
            (x,                             y),
            (x + 16 - width / 2,            y),
            (x + 16 - width / 2 - depth,    y + depth),
            (x + 16 + width / 2 + depth,    y + depth),
            (x + 16 + width / 2,            y),
            (x + 32,                        y)
        ]
    line.add_vertices(points)
    return line


def waterPoints(start, end, p=2):
    stepX = (end[0] - start[0]) / (p + 1)
    stepY = (end[1] - start[1]) / (p + 1)
    width = .3

    points = []
    points.append(start)
    i = 1
    while i <= p:
        x = start[0] + i * stepX
        y = start[1] + i * stepY
        xp = random.uniform(x - width, x + width)
        yp = random.uniform(y - width, y + width)
        points.append((xp, yp))
        # x = xp + stepX / 2.0
        # y = yp + stepY / 2.0
        # xp = random.uniform(xp - width / 3, xp + width / 3)
        # yp = random.uniform(yp - width / 3, yp + width / 3)
        # points.append((xp, yp))
        i += 1
    points.append(end)
    rpoints = [(d * 32.0, e * 32.0) for (d, e) in points]
    return rpoints
