import math

def continuous_flow(products, rows, cols):

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    row = 0
    col = 0

    for p in products:

        height = p["shelves_needed"]

        if row + height > rows:
            col += 1
            row = 0

        if col >= cols:
            raise Exception("Planogram overflow")

        for i in range(height):
            grid[row + i][col] = p["product_name"]

        row += height

    return grid
