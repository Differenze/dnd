from generate_tile import tile

for x in range(1, 11):
    for y in range(x, 11):
        drawing = tile(x, y)
        drawing.saveas('dxf/basic/tile_{}x{}.dxf'.format(x, y))
        del drawing
