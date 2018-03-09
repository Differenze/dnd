from generate_tile import tile
from generate_tile import waterPoints
from generate_tile import dxf

y = 2
for x in range(2, 5, 2):
    start = (0, 1)
    end = (x, 1)
    for i in range(0, 10):
        drawing = tile(x, y, allNegative=True)
        points = waterPoints(start, end, x + 1)
        spline = dxf.spline(points, color=1)
        drawing.add(spline)
        drawing.saveas('dxf/water/tile_{}x{}_{}.dxf'.format(x, y, i))
        del drawing
