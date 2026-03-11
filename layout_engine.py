import math

def continuous_flow(products, rows, cols):

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    # pointer where we are placing next block
    r = 0
    c = 0

    for p in products:

        brand = p["brand_key"]
        shelves = int(p["shelves_needed"])

        # determine block shape
        width = min(cols, math.ceil(math.sqrt(shelves)))
        height = math.ceil(shelves / width)

        placed = 0

        for i in range(height):
            for j in range(width):

                if placed >= shelves:
                    break

                rr = r + i
                cc = c + j

                if rr < rows and cc < cols:
                    grid[rr][cc] = brand
                    placed += 1

        # move placement cursor
        c += width

        if c >= cols:
            c = 0
            r += height

        if r >= rows:
            break

    return grid
