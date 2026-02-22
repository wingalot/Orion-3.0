#!/usr/bin/env python3
"""
E-Shape Tower v4 - Final correction
Middle shelf lower 2cm: walls but no floor (open bottom)
All closed boxes have walls on all sides
"""

import trimesh
import numpy as np

# Dimensions
WIDTH = 340
DEPTH = 160
HEIGHT = 360
WALL_THICK = 30
SHELF_DEPTH = 130
SIDE_THICK = 3
FRONT_THICK = 3
TOP_THICK = 3

# Positions
Z_BOTTOM = 0
Z_MIDDLE = 180
Z_TOP = 340

HOLE_SIZE = 100
HOLE_COUNT = 3
HOLE_SPACING = (WIDTH - 2*SIDE_THICK - HOLE_COUNT * HOLE_SIZE) / (HOLE_COUNT + 1)

def create_closed_box(z_pos, box_height, with_holes=False, open_bottom=False):
    """Create a closed box
    - with_holes: cut 3 holes in top
    - open_bottom: no bottom floor (just walls)
    """
    meshes = []
    y_center = WALL_THICK + SHELF_DEPTH/2
    internal_depth = SHELF_DEPTH - FRONT_THICK
    front_width = WIDTH - 2*SIDE_THICK
    
    # Side walls (left and right)
    left = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, box_height])
    left.apply_translation([SIDE_THICK/2, y_center, z_pos + box_height/2])
    meshes.append(left)
    
    right = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, box_height])
    right.apply_translation([WIDTH - SIDE_THICK/2, y_center, z_pos + box_height/2])
    meshes.append(right)
    
    # Front wall
    front = trimesh.creation.box(extents=[front_width, FRONT_THICK, box_height])
    front.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH - FRONT_THICK/2, 
                            z_pos + box_height/2])
    meshes.append(front)
    
    # Top (with or without holes)
    if with_holes:
        top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                              z_pos + box_height - TOP_THICK/2])
        
        holes = []
        for i in range(HOLE_COUNT):
            x_pos = SIDE_THICK + HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
            hole = trimesh.creation.box(extents=[HOLE_SIZE, internal_depth + 2, TOP_THICK + 2])
            hole.apply_translation([x_pos, WALL_THICK + internal_depth/2, 
                                   z_pos + box_height - TOP_THICK/2])
            holes.append(hole)
        
        top = top.difference(trimesh.util.concatenate(holes))
        meshes.append(top)
    else:
        top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                              z_pos + box_height - TOP_THICK/2])
        meshes.append(top)
    
    # Bottom floor (unless open_bottom)
    if not open_bottom:
        bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, TOP_THICK])
        bottom.apply_translation([WIDTH/2, y_center, z_pos + TOP_THICK/2])
        meshes.append(bottom)
    
    return meshes

def create_bottom_shelf():
    """Bottom shelf: 80mm total
    Upper 40mm: closed box with holes
    Divider at 40mm
    Lower 40mm: closed box (all sides)
    """
    meshes = []
    z_pos = Z_BOTTOM
    
    # Upper 40mm closed box with holes
    upper = create_closed_box(z_pos + 40, 40, with_holes=True, open_bottom=False)
    meshes.extend(upper)
    
    # Lower 40mm closed box (no holes)
    lower = create_closed_box(z_pos, 40, with_holes=False, open_bottom=False)
    meshes.extend(lower)
    
    return meshes

def create_middle_shelf():
    """Middle shelf: 60mm total
    Upper 40mm: closed box with holes (walls on all sides)
    Divider at 20mm from bottom (so at z=20)
    Lower 20mm: walls but NO floor (open bottom)
    """
    meshes = []
    z_pos = Z_MIDDLE
    
    # Upper 40mm closed box with holes (from z=20 to z=60)
    upper = create_closed_box(z_pos + 20, 40, with_holes=True, open_bottom=False)
    meshes.extend(upper)
    
    # Lower 20mm: walls but open bottom (from z=0 to z=20)
    lower = create_closed_box(z_pos, 20, with_holes=False, open_bottom=True)
    meshes.extend(lower)
    
    return meshes

def create_top_shelf():
    """Top shelf: 20mm closed solid box"""
    return create_closed_box(Z_TOP, 20, with_holes=False, open_bottom=False)

def create_open_back_wall():
    """Back wall without back panel (U-shape channel)"""
    meshes = []
    shell_thick = 3
    
    # Top panel
    top = trimesh.creation.box(extents=[WIDTH, WALL_THICK, shell_thick])
    top.apply_translation([WIDTH/2, WALL_THICK/2, HEIGHT - shell_thick/2])
    meshes.append(top)
    
    # Bottom panel
    bottom = trimesh.creation.box(extents=[WIDTH, WALL_THICK, shell_thick])
    bottom.apply_translation([WIDTH/2, WALL_THICK/2, shell_thick/2])
    meshes.append(bottom)
    
    # Left panel
    left = trimesh.creation.box(extents=[shell_thick, WALL_THICK, HEIGHT - 2*shell_thick])
    left.apply_translation([shell_thick/2, WALL_THICK/2, HEIGHT/2])
    meshes.append(left)
    
    # Right panel
    right = trimesh.creation.box(extents=[shell_thick, WALL_THICK, HEIGHT - 2*shell_thick])
    right.apply_translation([WIDTH - shell_thick/2, WALL_THICK/2, HEIGHT/2])
    meshes.append(right)
    
    return meshes

def create_e_tower_v4():
    """Create E-tower v4"""
    meshes = []
    
    # Back wall (open from back)
    back_wall = create_open_back_wall()
    meshes.extend(back_wall)
    
    # Bottom shelf (80mm: 40+40, both closed)
    bottom = create_bottom_shelf()
    meshes.extend(bottom)
    
    # Middle shelf (60mm: 40cm closed + 20cm with walls but open bottom)
    middle = create_middle_shelf()
    meshes.extend(middle)
    
    # Top shelf (20mm, solid closed)
    top = create_top_shelf()
    meshes.extend(top)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating E-tower v4...")
print("   Middle upper: 4cm closed box")
print("   Middle lower: 2cm with walls, open bottom")
print("   Bottom: 4cm + 4cm (both fully closed)")

model = create_e_tower_v4()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

output = "/home/oreo/.openclaw/workspace/e_tower_v4.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*60)
print("E-TOWER v4 - FINAL CORRECT")
print("="*60)
print(f"Size: {WIDTH}mm × {DEPTH}mm × {HEIGHT}mm")
print(f"\nBACK WALL (E vertical): U-shape (no back panel)")
print(f"\nBOTTOM SHELF (80mm = 40mm + 40mm):")
print(f"  ┌───┬───┬───┐")
print(f"  │ ○ │ ○ │ ○ │  ← Upper 40mm, holes, closed")
print(f"  ├───┴───┴───┤")
print(f"  │ (closed)  │  ← Lower 40mm, fully closed")
print(f"  └───────────┘")
print(f"\nMIDDLE SHELF (60mm = 40mm + 20mm):")
print(f"  ┌───┬───┬───┐")
print(f"  │ ○ │ ○ │ ○ │  ← Upper 40mm, holes, closed all sides")
print(f"  ├───┴───┴───┤")
print(f"  │  (walls)  │  ← Lower 20mm, walls BUT NO FLOOR")
print(f"  └───────────┘  (open at bottom)")
print(f"\nTOP SHELF (20mm): solid closed box")
print("="*60)
