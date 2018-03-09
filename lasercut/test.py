from generate_tile import tile
from generate_tile import base
from generate_tile import waterPoints
from generate_tile import dxf

width = 2
height = 2
start = (1, 0)
end = (1, 3)
offset = 32 * width + 10

# for i in range(20):
#     drawing = tile(width, height)
#     drawing = base(width, height, offset, 0, drawing)
#     points = waterPoints(start, end, 4)
#     spline1 = dxf.spline(points, color=1)
#     spline2 = dxf.spline([(x + offset, y) for (x, y) in points], color=1)
#     drawing.add(spline1)
#     drawing.add(spline2)
#     for point in points:
#         drawing.add(dxf.circle(center=point, color=8))
#     drawing.saveas('tmp/test{}.dxf'.format(i))


drawing = tile(width, height, allNegative=True)
drawing.saveas('tmp/test.dxf')
