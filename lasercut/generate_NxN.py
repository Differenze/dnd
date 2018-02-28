from generate_tile import tile
from generate_tile import base

for x in range(1, 7):
    for y in range(x, 7):
        drawing = tile(x, y)
        drawing = base(x, y, x*32+10, 0, drawing)
        drawing.saveas('dxf/tile_{}x{}.dxf'.format(x, y))
        del drawing
