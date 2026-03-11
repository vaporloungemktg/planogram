def continuous_flow(products, rows, cols):

    total_shelves = rows * cols

    # create list of shelves needed by brand
    shelf_list = []

    for p in products:
        brand = p["brand_key"]
        shelves = int(p["shelves_needed"])

        for _ in range(shelves):
            shelf_list.append(brand)

    if len(shelf_list) > total_shelves:
        raise Exception("Planogram overflow")

    # fill remaining shelves
    while len(shelf_list) < total_shelves:
        shelf_list.append(None)

    # create grid
    grid = [[None for _ in range(cols)] for _ in range(rows)]

    index = 0

    # block placement algorithm
    for c in range(cols):
        for r in range(rows):

            if index >= len(shelf_list):
                break

            grid[r][c] = shelf_list[index]
            index += 1

    return grid
