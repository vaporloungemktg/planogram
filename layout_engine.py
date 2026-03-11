import math

def continuous_flow(products, rows, cols):

    total_slots = rows * cols

    # create full shelf list
    shelves = []

    for p in products:
        brand = p["brand_key"]
        count = int(p["shelves_needed"])

        for _ in range(count):
            shelves.append(brand)

    # check overflow
    if len(shelves) > total_slots:
        raise Exception("Not enough fixture space")

    # pad empty shelves
    while len(shelves) < total_slots:
        shelves.append(None)

    # build grid
    grid = []
    idx = 0

    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(shelves[idx])
            idx += 1
        grid.append(row)

    return grid
