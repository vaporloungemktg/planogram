import math

def continuous_flow(products, rows, cols):

    total_shelves = rows * cols

    # build list of brand shelves
    shelf_list = []

    for p in products:
        brand = p["brand_key"]
        shelves = int(p["shelves_needed"])

        for _ in range(shelves):
            shelf_list.append(brand)

    if len(shelf_list) > total_shelves:
        raise Exception("Planogram overflow")

    while len(shelf_list) < total_shelves:
        shelf_list.append(None)

    # create empty grid
    grid = [[None for _ in range(cols)] for _ in range(rows)]

    index = 0

    for r in range(rows):
        for c in range(cols):

            if index >= len(shelf_list):
                break

            grid[r][c] = shelf_list[index]
            index += 1

    return grid
