from dxfwrite import DXFEngine as dxf
from enum import Enum

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


def tile(width, height, offsetX=0, offsetY=0, drawing=None):
    if(drawing==None):
        drawing = empty_drawing()
    entities = []
    for x in range(0, width):
        px = 32 * x + offsetX
        for y in range(0, height):
            py = 32 * y + offsetY
            # right
            if x == width - 1:
                right = dxf.line(
                                (px + 32, py),
                                (px + 32, py + 32), layer='cut')
                entities.append(right)
            # top
            if y == height - 1:
                top = dxf.line((px, py + 32), (px + 32, py + 32), layer='cut')
                entities.append(top)
            # bottom
            bottom = dxf.line((px, py), (px + 32, py), layer='mark')
            if y == 0:
                bottom['layer'] = 'cut'
            entities.append(bottom)
            # left
            left = dxf.line((px, py), (px, py + 32), layer='mark')
            if x == 0:
                left['layer'] = 'cut'
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
    if(drawing==None):
        drawing = empty_drawing()
    entities = []

    for x in range(0, width):
        px = 32 * x + offsetX
        for y in range(0, height):
            py = 32 * y + offsetY
            if x==0:
                entities.append(notchedLine(px, py, Direction.WEST))
            if y==0:
                entities.append(notchedLine(px, py, Direction.SOUTH))
            if x==width-1:    
                entities.append(notchedLine(px, py, Direction.EAST))
            if y==height-1:
                entities.append(notchedLine(px, py, Direction.NORTH))

    for entity in entities:
        drawing.add(entity)
    return drawing

def notchedLine(x, y, direction=Direction.SOUTH, depth=4, width=8):
    line = dxf.polyline(layer='cut')
    if direction==Direction.NORTH:
        points = [
            (x,                     y+32),
            (x+16-width/2,          y+32),
            (x+16-width/2-depth,    y+32-depth),
            (x+16+width/2+depth,    y+32-depth),
            (x+16+width/2,          y+32),
            (x+32,                  y+32)
        ]
    elif direction==Direction.WEST:
        points = [
            (x,                     y),
            (x,                     y+16-width/2),
            (x+depth,               y+16-width/2-depth),
            (x+depth,               y+16+width/2+depth),
            (x,                     y+16+width/2),
            (x,                     y+32)
        ]
    elif direction==Direction.EAST:
        points = [
            (x+32,                  y),
            (x+32,                  y+16-width/2),
            (x+32-depth,            y+16-width/2-depth),
            (x+32-depth,            y+16+width/2+depth),
            (x+32,                  y+16+width/2),
            (x+32,                  y+32)
        ]
    else: # SOUTH
        points = [
            (x,                     y),
            (x+16-width/2,          y),
            (x+16-width/2-depth,    y+depth),
            (x+16+width/2+depth,    y+depth),
            (x+16+width/2,          y),
            (x+32,                  y)
        ]
    line.add_vertices(points)
    return line
