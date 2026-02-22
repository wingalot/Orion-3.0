#!/usr/bin/env python3
"""
E-Shape Tower - Closed box shelves with shared internal space
Each shelf has walls on sides and front, top has 3 holes,
but internal space below is open/shared (not divided)
"""

import trimesh
import numpy as np

# Dimensions
WIDTH = 340       # X: total width
DEPTH = 160       # Y: total depth (30mm wall + 130mm shelf)
HEIGHT = 360      # Z: total height

# E-shape
WALL_THICK = 30   # Back vertical wall
SHELF_DEPTH = 130 # How far shelves extend from wall

# Shelf box dimensions
SIDE_THICK = 3    # Side wall thickness
FRONT_THICK = 3   # Front wall thickness
TOP_THICK = 3     # Top surface thickness
BOTTOM_THICK = 3  # Bottom surface thickness

# Shelf heights (internal space = total - top - bottom)
SHELF_H_BOTTOM = 80   # 8cm total
SHELF_H_MIDDLE = 60   # 6cm total
SHELF_H_TOP = 20      # 2cm total

# Positions
Z_BOTTOM = 0
Z_MIDDLE = 180  # 80 + 100
Z_TOP = 340     # 180 + 60 + 100

# Holes
HOLE_SIZE = 100
HOLE_COUNT = 3
HOLE_SPACING = (WIDTH - HOLE_COUNT * HOLE_SIZE) / (HOLE_COUNT + 1)

def create_closed_shelf(z_pos, shelf_height, with_holes):
    """Create a closed box shelf:
    - Top with 3 holes (if with_holes)
    - Bottom solid
    - Side walls (left and right)
    - Front wall
    - Back open (connects to E-wall)
    - Internal space is shared (no dividers between holes)
    """
    meshes = []
    
    internal_height = shelf_height - TOP_THICK - BOTTOM_THICK
    internal_depth = SHELF_DEPTH - FRONT_THICK
    internal_width = WIDTH - 2 * SIDE_THICK
    
    # Position: extends from back wall
    y_center = WALL_THICK + SHELF_DEPTH/2
    
    # 1. BOTTOM (solid)
    bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, BOTTOM_THICK])
    bottom.apply_translation([WIDTH/2, y_center, z_pos + BOTTOM_THICK/2])
    meshes.append(bottom)
    
    # 2. LEFT SIDE WALL (full height)
    left = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, shelf_height])
    left.apply_translation([SIDE_THICK/2, y_center, z_pos + shelf_height/2])
    meshes.append(left)
    
    # 3. RIGHT SIDE WALL (full height)
    right = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, shelf_height])
    right.apply_translation([WIDTH - SIDE_THICK/2, y_center, z_pos + shelf_height/2])
    meshes.append(right)
    
    # 4. FRONT WALL (between side walls, full height)
    front = trimesh.creation.box(extents=[internal_width, FRONT_THICK, shelf_height])
    front.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH - FRONT_THICK/2, z_pos + shelf_height/2])
    meshes.append(front)
    
    # 5. TOP with holes
    if with_holes and internal_height > 0:
        # Create top plate
        top = trimesh.creation.box(extents=[internal_width, internal_depth, TOP_THICK])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                              z_pos + shelf_height - TOP_THICK/2])
        
        # Create 3 holes (cut through top)
        holes = []
        for i in range(HOLE_COUNT):
            x_pos = SIDE_THICK + HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
            hole = trimesh.creation.box(extents=[HOLE_SIZE, internal_depth + 2, TOP_THICK + 2])
            hole.apply_translation([x_pos, WALL_THICK + internal_depth/2, 
                                   z_pos + shelf_height - TOP_THICK/2])
            holes.append(hole)
        
        top_with_holes = top.difference(trimesh.util.concatenate(holes))
        meshes.append(top_with_holes)
    elif with_holes:
        # Thin shelf - solid with holes
        top = trimesh.creation.box(extents=[internal_width, internal_depth, shelf_height])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, z_pos + shelf_height/2])
        
        holes = []
        for i in range(HOLE_COUNT):
            x_pos = SIDE_THICK + HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
            hole = trimesh.creation.box(extents=[HOLE_SIZE, internal_depth + 2, shelf_height + 2])
            hole.apply_translation([x_pos, WALL_THICK + internal_depth/2, z_pos + shelf_height/2])
            holes.append(hole)
        
        top_with_holes = top.difference(trimesh.util.concatenate(holes))
        meshes.append(top_with_holes)
    else:
        # Solid top (no holes)
        top = trimesh.creation.box(extents=[internal_width, internal_depth, TOP_THICK])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                              z_pos + shelf_height - TOP_THICK/2])
        meshes.append(top)
    
    return meshes

def create_e_tower_closed():
    """Create E-shape with closed box shelves"""
    meshes = []
    
    # Back vertical wall
    back_wall = trimesh.creation.box(extents=[WIDTH, WALL_THICK, HEIGHT])
    back_wall.apply_translation([WIDTH/2, WALL_THICK/2, HEIGHT/2])
    meshes.append(back_wall)
    
    # Bottom shelf (closed box, 80mm, with holes)
    bottom = create_closed_shelf(Z_BOTTOM, SHELF_H_BOTTOM, with_holes=True)
    meshes.extend(bottom)
    
    # Middle shelf (closed box, 60mm, with holes)
    middle = create_closed_shelf(Z_MIDDLE, SHELF_H_MIDDLE, with_holes=True)
    meshes.extend(middle)
    
    # Top shelf (closed box, 20mm, solid - no holes)
    top = create_closed_shelf(Z_TOP, SHELF_H_TOP, with_holes=False)
    meshes.extend(top)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating E-tower with closed box shelves...")
print("   Each shelf: walls on sides/front, top with holes, shared internal space")

model = create_e_tower_closed()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

output = "/home/oreo/.openclaw/workspace/e_tower_closed.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*60)
print("E-TOWER WITH CLOSED SHELVES")
print("="*60)
print(f"Overall: {WIDTH}mm × {DEPTH}mm × {HEIGHT}mm")
print(f"\nEach shelf is a closed box:")
print(f"  ┌───────────────────────────┐  ← Top with 3 holes (10×10cm)")
print(f"  │  [○]     [○]     [○]      │")
print(f"  │                           │  ← Shared internal space")
print(f"  │  (empty, no dividers)     │")
print(f"  │                           │")
print(f"  ├───────────────────────────┤  ← Solid bottom")
print(f"  │                           │")
print(f"  └───────────────────────────┘  ← Front wall")
print(f"  └───────────────────────────┘  ← Back wall (30mm)")
print(f"\nShelves:")
print(f"  Bottom: 80mm height, 3 holes, shared space")
print(f"  Middle: 60mm height, 3 holes, shared space")
print(f"  Top: 20mm height, solid (no holes)")
print(f"\nWalls: 3mm thickness (sides, front, top, bottom)")
print("="*60)
