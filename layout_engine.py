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


def place_block(grid, r, c, width, height, product_name, shelves):

    placed = 0

    for i in range(height):
        for j in range(width):

            if placed >= shelves:
                return

            grid[r+i][c+j] = product_name
            placed += 1


# -----------------------------
# Brand Blocking Layout
# -----------------------------

def brand_block_layout(products, rows, cols, restricted_coords=[]):
    grid = [[None for _ in range(cols)] for _ in range(rows)]
    
    # Pre-fill restricted cells
    for (r, c) in restricted_coords:
        if r < rows and c < cols:
            grid[r][c] = "BLOCKED"

    # Group products by brand
    brands = {}
    for p in products:
        brand = p.get('brand', 'Other')
        if brand not in brands:
            brands[brand] = []
        brands[brand].append(p)

    current_col = 0
    current_row = 0

    for brand, brand_products in brands.items():
        for p in brand_products:
            shelves = int(p.get('shelves_needed', 1))
            placed = False
            
            while not placed and current_col < cols:
                # Check if enough vertical space exists in current column (skipping BLOCKED)
                available = 0
                for r in range(current_row, rows):
                    if grid[r][current_col] is None:
                        available += 1
                    else:
                        break # Hit the bottom or a BLOCKED cell
                
                if shelves <= available:
                    for i in range(shelves):
                        grid[current_row + i][current_col] = p['product_name']
                    current_row += shelves
                    placed = True
                else:
                    # Move to next column
                    current_col += 1
                    current_row = 0
                    
                if current_row >= rows:
                    current_col += 1
                    current_row = 0
    return grid


# -----------------------------
# Vertical Layout
# -----------------------------

def vertical_layout(products, rows, cols, restricted_coords=[]):
    # Initialize the grid
    grid = [[None for _ in range(cols)] for _ in range(rows)]
    
    # NEW: Mark restricted cells first so the engine skips them
    for (r, c) in restricted_coords:
        if r < rows and c < cols:
            grid[r][c] = "BLOCKED" 

    remaining_products = products.copy()
    
    for c in range(cols):
        for r in range(rows):
            # Skip if cell is occupied OR blocked
            if grid[r][c] is not None:
                continue
                
            # Check for consecutive space before the next BLOCKED cell or bottom
            space_available = 0
            for i in range(r, rows):
                if grid[i][c] is None:
                    space_available += 1
                else:
                    break
            
            # Find the first product that fits in this specific gap
            for idx, p in enumerate(remaining_products):
                shelves = int(p.get("shelves_needed", 1))
                if shelves <= space_available:
                    name = p.get("product_name", "Unknown")
                    for s in range(shelves):
                        grid[r + s][c] = name
                    
                    remaining_products.pop(idx)
                    break 
                    
    return grid

# -----------------------------
# Alphabetical Layout
# -----------------------------

def alphabetical_layout(products, rows, cols):

    grid = create_grid(rows, cols)

    # products = sorted(products, key=lambda x: x["product_name"])

    row = 0
    col = 0

    for p in products:
            name = p["product_name"]
            shelves = int(p["shelves_needed"])
            
            # Check if it fits in current column
            if (rows - row) < shelves:
                col += 1
                row = 0
                
            for _ in range(shelves):
                # Only place if within the physical grid
                if col < cols and row < rows:
                    grid[row][col] = name
                
                # Always advance row/col so no products are skipped
                row += 1
                if row >= rows:
                    row = 0
                    col += 1

    return grid

# -----------------------------
# Recommended Layout
# -----------------------------

def recommended_layout(products, rows, cols):

    grid = create_grid(rows, cols)

    # products = sorted(products, key=lambda x: x["priority"])

    row = 0
    col = 0

    for p in products:
            name = p["product_name"]
            shelves = int(p["shelves_needed"])
    
            if (rows - row) < shelves:
                col += 1
                row = 0
    
            for _ in range(shelves):
                if col < cols and row < rows:
                    grid[row][col] = name
                
                row += 1
                if row >= rows:
                    row = 0
                    col += 1

    return grid
