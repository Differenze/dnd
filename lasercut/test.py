from generate_tile import tile
from generate_tile import base


drawing = tile(2, 2)
drawing = base(2, 2, 70, 0, drawing)

drawing.saveas('test.dxf')
