import math


def continuous_flow(products, rows, cols):

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    # Sort largest brands first
    products = sorted(products, key=lambda x: x["shelves_needed"], reverse=True)

    def fits(r, c, height, width):
        if r + height > rows or c + width > cols:
            return False

        for i in range(height):
            for j in range(width):
                if grid[r+i][c+j] is not None:
                    return False

        return True


    def place_block(r, c, width, height, brand, shelves):
    
        placed = 0
    
        for i in range(height):
            for j in range(width):
    
                if placed >= shelves:
                    break
    
                grid[r + i][c + j] = brand
                placed += 1
    
            if placed >= shelves:
                break


    for p in products:

        brand = p["brand_key"]
        flavors = int(p["flavor_count"])
        strengths = int(p["strength_count"])
        capacity = int(p["capacity_per_foot"])

        shelves_per_strength = math.ceil(flavors / capacity)
        shelves_needed = shelves_per_strength * strengths

        # Planogram merchandising rule
        width = min(cols, shelves_per_strength)
        height = math.ceil(shelves_needed / width)

        placed = False

        for r in range(rows):

            if placed:
                break

            for c in range(cols):

                if fits(r, c, height, width):

                    place_block(r, c, width, height, brand, shelves_needed)

                    placed = True
                    break

    return grid


# -----------------------------------
# NEW: Vertical Planogram Layout
# -----------------------------------

def vertical_layout(products, rows, cols):

    grid = [[None for _ in range(cols)] for _ in range(rows)]

    # Largest brands first
    products = sorted(products, key=lambda x: x["shelves_needed"], reverse=True)

    col = 0
    row = 0

    for p in products:

        brand = p["brand_key"]
        shelves = int(p["shelves_needed"])

        for _ in range(shelves):

            if col >= cols:
                break

            grid[row][col] = brand

            row += 1

            if row >= rows:
                row = 0
                col += 1

    return grid
