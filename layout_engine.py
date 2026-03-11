import math

def continuous_flow(products, rows, cols):

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    # sort largest blocks first
    products = sorted(products, key=lambda x: x["shelves_needed"], reverse=True)

    r = 0
    c = 0

    for p in products:

        brand = p["brand_key"]
        shelves = int(p["shelves_needed"])

        placed = 0

        while placed < shelves:

            if r >= rows:
                return grid

            if grid[r][c] is None:
                grid[r][c] = brand
                placed += 1

            c += 1

            if c >= cols:
                c = 0
                r += 1

    return grid
