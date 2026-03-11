def continuous_flow(products, rows, cols):

    total_shelves = rows * cols

    shelves_used = []

    for p in products:

        brand = p["brand_key"]
        shelves_needed = int(p["shelves_needed"])

        for _ in range(shelves_needed):
            shelves_used.append(brand)

    if len(shelves_used) > total_shelves:
        raise Exception("Planogram overflow")

    # fill remaining shelves with empty
    while len(shelves_used) < total_shelves:
        shelves_used.append(None)

    # convert to grid
    grid = []
    index = 0

    for r in range(rows):

        row = []

        for c in range(cols):

            row.append(shelves_used[index])
            index += 1

        grid.append(row)

    return grid
