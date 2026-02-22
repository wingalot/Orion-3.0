#!/usr/bin/env python3
"""
E-Shape Tower with hollow shelves (open frame)
Each shelf is an open box:
- Top with 3 holes (10x10cm) for pots
- Solid bottom (no holes) 
- Open sides and front
- Connected to back wall
"""

import trimesh
import numpy as np

# Dimensions
WIDTH = 340       # X: total width
DEPTH = 160       # Y: total depth (30mm wall + 130mm shelf)
HEIGHT = 360      # Z: total height

# E-shape
WALL_THICK = 30   # Back vertical wall thickness
SHELF_DEPTH = 130 # How far shelves extend from wall

# Shelf thicknesses
SHELF_THICK_TOP = 3    # Top surface thickness (with holes)
SHELF_THICK_BOTTOM = 3 # Bottom surface thickness (solid)
SHELF_HEIGHT_BOTTOM = 80   # 8cm total height
SHELF_HEIGHT_MIDDLE = 60   # 6cm total height
SHELF_HEIGHT_TOP = 20      # 2cm total height (just top, no hollow space)

# Positions
BOTTOM_Z = 0
MIDDLE_Z = 180  # 80 + 100 gap
TOP_Z = 340     # 180 + 60 + 100 = 340

# Holes
HOLE_SIZE = 100  # 10x10cm
HOLE_COUNT = 3
# Space holes evenly across width
HOLE_SPACING = (WIDTH - HOLE_COUNT * HOLE_SIZE) / (HOLE_COUNT + 1)

def create_open_shelf(z_pos, shelf_height, with_holes):
    """Create an open shelf (top + bottom only, no sides/front)
    - Top surface: with 3 holes if with_holes=True
    - Bottom surface: always solid
    - Open sides and front
    """
    meshes = []
    
    # Internal space height (between top and bottom surfaces)
    internal_height = shelf_height - SHELF_THICK_TOP - SHELF_THICK_BOTTOM
    
    if internal_height < 0:
        internal_height = 0
    
    # 1. TOP SURFACE (with holes)
    if with_holes and internal_height > 0:
        # Create top with holes
        top = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, SHELF_THICK_TOP])
        top.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH/2, 
                               z_pos + shelf_height - SHELF_THICK_TOP/2])
        
        # Create 3 holes
        holes = []
        for i in range(HOLE_COUNT):
            x_pos = HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
            hole = trimesh.creation.box(extents=[HOLE_SIZE, SHELF_DEPTH + 2, SHELF_THICK_TOP + 2])
            hole.apply_translation([x_pos, WALL_THICK + SHELF_DEPTH/2, 
                                   z_pos + shelf_height - SHELF_THICK_TOP/2])
            holes.append(hole)
        
        top_with_holes = top.difference(trimesh.util.concatenate(holes))
        meshes.append(top_with_holes)
    elif with_holes:
        # Thin shelf, just create solid top with holes cut through
        top = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, shelf_height])
        top.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH/2, z_pos + shelf_height/2])
        
        holes = []
        for i in range(HOLE_COUNT):
            x_pos = HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
            hole = trimesh.creation.box(extents=[HOLE_SIZE, SHELF_DEPTH + 2, shelf_height + 2])
            hole.apply_translation([x_pos, WALL_THICK + SHELF_DEPTH/2, z_pos + shelf_height/2])
            holes.append(hole)
        
        top_with_holes = top.difference(trimesh.util.concatenate(holes))
        meshes.append(top_with_holes)
    else:
        # Solid top (for top shelf or if no holes needed)
        top = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, SHELF_THICK_TOP])
        top.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH/2, 
                               z_pos + shelf_height - SHELF_THICK_TOP/2])
        meshes.append(top)
    
    # 2. BOTTOM SURFACE (always solid, no holes)
    if internal_height > 0:
        bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, SHELF_THICK_BOTTOM])
        bottom.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH/2, 
                                 z_pos + SHELF_THICK_BOTTOM/2])
        meshes.append(bottom)
    
    return meshes

def create_e_tower_open():
    """Create E-shape with open hollow shelves"""
    meshes = []
    
    # 1. BACK VERTICAL WALL (full, solid)
    back_wall = trimesh.creation.box(extents=[WIDTH, WALL_THICK, HEIGHT])
    back_wall.apply_translation([WIDTH/2, WALL_THICK/2, HEIGHT/2])
    meshes.append(back_wall)
    
    # 2. BOTTOM SHELF (open box, 80mm height, with holes in top)
    bottom_shelf = create_open_shelf(BOTTOM_Z, SHELF_HEIGHT_BOTTOM, with_holes=True)
    meshes.extend(bottom_shelf)
    
    # 3. MIDDLE SHELF (open box, 60mm height, with holes in top)
    middle_shelf = create_open_shelf(MIDDLE_Z, SHELF_HEIGHT_MIDDLE, with_holes=True)
    meshes.extend(middle_shelf)
    
    # 4. TOP SHELF (just a thin solid shelf, 20mm)
    # For top, it's solid (no hollow space, just a solid plate)
    top_shelf = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, SHELF_HEIGHT_TOP])
    top_shelf.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH/2, 
                                 TOP_Z + SHELF_HEIGHT_TOP/2])
    meshes.append(top_shelf)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating E-tower with open hollow shelves...")
print("   Structure: Top with holes + solid bottom, open sides/front/back")

model = create_e_tower_open()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

# Export main frame
output = "/home/oreo/.openclaw/workspace/e_tower_with_holes.stl"
model.export(output)
print(f"💾 Main frame exported: {output}")

print("\n" + "="*55)
print("E-TOWER WITH HOLES - SPECIFICATIONS:")
print("="*55)
print(f"Overall: {WIDTH}mm(W) × {DEPTH}mm(D) × {HEIGHT}mm(H)")
print(f"\nStructure:")
print(f"  BACK: Solid wall ({WALL_THICK}mm thick)")
print(f"\n  BOTTOM SHELF (80mm height):")
print(f"    - Top: 3 holes (10×10cm each), spaced evenly")
print(f"    - Bottom: Solid (3mm)")
print(f"    - Sides/Front: OPEN (hollow inside)")
print(f"\n  MIDDLE SHELF (60mm height):")
print(f"    - Top: 3 holes (10×10cm each)")
print(f"    - Bottom: Solid (3mm)")  
print(f"    - Sides/Front: OPEN")
print(f"\n  TOP SHELF (20mm height):")
print(f"    - Solid plate (no holes, no hollow space)")
print(f"\nHole positions (center X):")
for i in range(HOLE_COUNT):
    x_pos = HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
    print(f"  Hole {i+1}: X = {x_pos:.1f}mm")
print("="*55)
