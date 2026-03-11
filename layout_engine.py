import math


# -----------------------------
# Helper Functions
# -----------------------------

def create_grid(rows, cols):
    return [[None for _ in range(cols)] for _ in range(rows)]


def fits(grid, r, c, height, width, rows, cols):

    if r + height > rows or c + width > cols:
        return False

    for i in range(height):
        for j in range(width):
            if grid[r+i][c+j] is not None:
                return False

    return True


def place_block(grid, r, c, width, height, product_names, shelves):

    placed = 0

    for i in range(height):
        for j in range(width):

            if placed >= shelves:
                return

            grid[r+i][c+j] = product_names[placed % len(product_names)]
            placed += 1


# -----------------------------
# Brand Blocking Layout
# -----------------------------

def continuous_flow(products, rows, cols):

    grid = create_grid(rows, cols)

    # Largest brands first
    products = sorted(products, key=lambda x: x["shelves_needed"], reverse=True)

    for p in products:

        brand = p["brand_key"]
        flavors = int(p["flavor_count"])
        strengths = int(p["strength_count"])
        capacity = int(p["capacity_per_foot"])
        shelves_needed = int(p["shelves_needed"])

        shelves_per_strength = math.ceil(flavors / capacity)

        # Primary merchandising shape
        primary_width = shelves_per_strength
        primary_height = strengths

        # Possible fallback shapes
        possible_shapes = [
            (primary_width, primary_height),
            (primary_height, primary_width),
            (shelves_needed, 1),
            (1, shelves_needed)
        ]

        placed = False

        for width, height in possible_shapes:

            for r in range(rows):

                if placed:
                    break

                for c in range(cols):

                    if fits(grid, r, c, height, width, rows, cols):

                        product_names = p["product_names"]
                        place_block(grid, r, c, width, height, product_names, shelves_needed)

                        placed = True
                        break

            if placed:
                break

    return grid


# -----------------------------
# Vertical Layout
# -----------------------------

def vertical_layout(products, rows, cols):

    grid = create_grid(rows, cols)

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

            products_list = p["product_names"]
            grid[row][col] = products_list[_ % len(products_list)]

            row += 1

            if row >= rows:
                row = 0
                col += 1

    return grid
