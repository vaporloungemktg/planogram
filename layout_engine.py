import math

def continuous_flow(products, rows, cols):

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    # place largest brands first
    products = sorted(products, key=lambda x: x["shelves_needed"], reverse=True)

    def fits(r, c, height, width):
        if r + height > rows or c + width > cols:
            return False
        for i in range(height):
            for j in range(width):
                if grid[r+i][c+j] is not None:
                    return False
        return True

    def place(r, c, height, width, brand, shelves):
        placed = 0
        for i in range(height):
            for j in range(width):
                if placed >= shelves:
                    return
                grid[r+i][c+j] = brand
                placed += 1

    for p in products:

        brand = p["brand_key"]
        shelves = int(p["shelves_needed"])

        width = min(cols, math.ceil(math.sqrt(shelves)))
        height = math.ceil(shelves / width)

        placed = False

        # search entire grid for a spot the block fits
        for r in range(rows):
            if placed:
                break
            for c in range(cols):
                if fits(r, c, height, width):
                    place(r, c, height, width, brand, shelves)
                    placed = True
                    break

    return grid
