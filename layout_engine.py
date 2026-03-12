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
    grid = create_grid(rows, cols)
    
    # 1. Pre-fill the grid with obstacles so the 'fits' function can see them
    for (r, c) in restricted_coords:
        if r < rows and c < cols:
            grid[r][c] = "BLOCKED"

    for p in products:
        brand = p["brand_key"]
        flavors = int(p["flavor_count"])
        strengths = int(p["strength_count"])
        capacity = int(p["capacity_per_foot"])
        shelves_needed = int(p["shelves_needed"])
        
        # Keep your 2x2 style logic
        shelves_per_strength = math.ceil(flavors / capacity)
        primary_width = shelves_per_strength
        primary_height = strengths
        
        possible_shapes = [
            (primary_width, primary_height), 
            (primary_height, primary_width), 
            (shelves_needed, 1), 
            (1, shelves_needed)
        ]
        
        placed = False
        for width, height in possible_shapes:
            if placed: break
            # Search for a spot that is NOT occupied and NOT "BLOCKED"
            for c in range(cols - width + 1):
                if placed: break
                for r in range(rows - height + 1):
                    # The 'fits' function already checks if grid[r][c] is None
                    # Since we marked obstacles as "BLOCKED", 'fits' will skip them!
                    if fits(grid, r, c, height, width, rows, cols):
                        place_block(grid, r, c, width, height, p["product_name"], shelves_needed)
                        placed = True
                        break
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
