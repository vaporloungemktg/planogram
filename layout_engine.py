def continuous_flow(products, rows, cols):

    # create empty grid
    grid = [[None for _ in range(cols)] for _ in range(rows)]

    r = 0
    c = 0

    for p in products:

        brand = p["brand_key"]
        total_products = int(p["total_products"])

        for _ in range(total_products):

            grid[r][c] = brand

            c += 1

            if c >= cols:
                c = 0
                r += 1

            if r >= rows:
                raise Exception("Planogram overflow")

    return grid
