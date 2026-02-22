#!/usr/bin/env python3
"""
E-Shape Tower v3 - Corrected middle shelf
Middle: 4cm closed box (plants) + 2cm open space below (no floor)
Bottom: 4cm + 4cm divided closed spaces
Top: 2cm solid
Back wall: open (no back panel)
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

def create_bottom_shelf():
    """Bottom shelf: 80mm total, divided into two 40mm closed spaces"""
    meshes = []
    total_height = 80
    z_pos = Z_BOTTOM
    y_center = WALL_THICK + SHELF_DEPTH/2
    internal_depth = SHELF_DEPTH - FRONT_THICK
    front_width = WIDTH - 2*SIDE_THICK
    
    # Bottom floor
    bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, TOP_THICK])
    bottom.apply_translation([WIDTH/2, y_center, z_pos + TOP_THICK/2])
    meshes.append(bottom)
    
    # Left wall
    left = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, total_height])
    left.apply_translation([SIDE_THICK/2, y_center, z_pos + total_height/2])
    meshes.append(left)
    
    # Right wall
    right = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, total_height])
    right.apply_translation([WIDTH - SIDE_THICK/2, y_center, z_pos + total_height/2])
    meshes.append(right)
    
    # Front wall
    front = trimesh.creation.box(extents=[front_width, FRONT_THICK, total_height])
    front.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH - FRONT_THICK/2, 
                            z_pos + total_height/2])
    meshes.append(front)
    
    # Divider at 40mm from bottom (middle of 80mm)
    divider = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
    divider_z = z_pos + 40
    divider.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, divider_z])
    meshes.append(divider)
    
    # Top with holes
    top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
    top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                          z_pos + total_height - TOP_THICK/2])
    
    holes = []
    for i in range(HOLE_COUNT):
        x_pos = SIDE_THICK + HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
        hole = trimesh.creation.box(extents=[HOLE_SIZE, internal_depth + 2, TOP_THICK + 2])
        hole.apply_translation([x_pos, WALL_THICK + internal_depth/2, 
                               z_pos + total_height - TOP_THICK/2])
        holes.append(hole)
    
    top = top.difference(trimesh.util.concatenate(holes))
    meshes.append(top)
    
    return meshes

def create_middle_shelf():
    """Middle shelf: 60mm total
    Upper 40mm: closed box for plants (with top holes)
    Lower 20mm: open space (no walls, no floor - just empty)
    Divider at 20mm from bottom
    """
    meshes = []
    total_height = 60
    z_pos = Z_MIDDLE
    y_center = WALL_THICK + SHELF_DEPTH/2
    internal_depth = SHELF_DEPTH - FRONT_THICK
    front_width = WIDTH - 2*SIDE_THICK
    
    # Divider floor at 20mm from bottom (so upper part is 40mm)
    divider_z = z_pos + 20
    
    # Lower 20mm space: NO floor, NO walls - it's just open under the divider
    # Only the divider itself separates upper and lower
    
    # DIVIDER (at 20mm from bottom)
    divider = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
    divider.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, divider_z])
    meshes.append(divider)
    
    # UPPER 40mm CLOSED BOX (from divider at 20mm to top at 60mm)
    # Left wall (only upper 40mm)
    left_upper = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, 40])
    left_upper.apply_translation([SIDE_THICK/2, y_center, divider_z + 20])
    meshes.append(left_upper)
    
    # Right wall (only upper 40mm)
    right_upper = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, 40])
    right_upper.apply_translation([WIDTH - SIDE_THICK/2, y_center, divider_z + 20])
    meshes.append(right_upper)
    
    # Front wall (only upper 40mm)
    front_upper = trimesh.creation.box(extents=[front_width, FRONT_THICK, 40])
    front_upper.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH - FRONT_THICK/2, 
                                  divider_z + 20])
    meshes.append(front_upper)
    
    # Top with holes (at very top)
    top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
    top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                          z_pos + total_height - TOP_THICK/2])
    
    holes = []
    for i in range(HOLE_COUNT):
        x_pos = SIDE_THICK + HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
        hole = trimesh.creation.box(extents=[HOLE_SIZE, internal_depth + 2, TOP_THICK + 2])
        hole.apply_translation([x_pos, WALL_THICK + internal_depth/2, 
                               z_pos + total_height - TOP_THICK/2])
        holes.append(hole)
    
    top = top.difference(trimesh.util.concatenate(holes))
    meshes.append(top)
    
    return meshes

def create_top_shelf():
    """Top shelf: 20mm closed solid box"""
    meshes = []
    total_height = 20
    z_pos = Z_TOP
    y_center = WALL_THICK + SHELF_DEPTH/2
    internal_depth = SHELF_DEPTH - FRONT_THICK
    front_width = WIDTH - 2*SIDE_THICK
    
    # Bottom
    bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, TOP_THICK])
    bottom.apply_translation([WIDTH/2, y_center, z_pos + TOP_THICK/2])
    meshes.append(bottom)
    
    # Left wall
    left = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, total_height])
    left.apply_translation([SIDE_THICK/2, y_center, z_pos + total_height/2])
    meshes.append(left)
    
    # Right wall
    right = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, total_height])
    right.apply_translation([WIDTH - SIDE_THICK/2, y_center, z_pos + total_height/2])
    meshes.append(right)
    
    # Front wall
    front = trimesh.creation.box(extents=[front_width, FRONT_THICK, total_height])
    front.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH - FRONT_THICK/2, 
                            z_pos + total_height/2])
    meshes.append(front)
    
    # Solid top
    top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
    top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                          z_pos + total_height - TOP_THICK/2])
    meshes.append(top)
    
    return meshes

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

def create_e_tower_v3():
    """Create E-tower v3"""
    meshes = []
    
    # Back wall (open from back)
    back_wall = create_open_back_wall()
    meshes.extend(back_wall)
    
    # Bottom shelf (80mm, divided 40+40, both closed)
    bottom = create_bottom_shelf()
    meshes.extend(bottom)
    
    # Middle shelf (60mm: 40cm closed + 20cm open below)
    middle = create_middle_shelf()
    meshes.extend(middle)
    
    # Top shelf (20mm, solid closed)
    top = create_top_shelf()
    meshes.extend(top)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating E-tower v3...")
print("   Middle: 4cm closed box + 2cm open space below")
print("   Bottom: 4cm + 4cm (both closed)")

model = create_e_tower_v3()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

output = "/home/oreo/.openclaw/workspace/e_tower_v3.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*60)
print("E-TOWER v3 - CORRECTED")
print("="*60)
print(f"Size: {WIDTH}mm × {DEPTH}mm × {HEIGHT}mm")
print(f"\nBACK WALL (E vertical):")
print(f"  U-shape channel (no back panel)")
print(f"\nBOTTOM SHELF (80mm = 40mm + 40mm):")
print(f"  ┌───┬───┬───┐")
print(f"  │ ○ │ ○ │ ○ │  ← 3 holes")
print(f"  ├───┴───┴───┤  ← Divider")
print(f"  │ (closed)  │  ← 40mm closed space")
print(f"  └───────────┘")
print(f"\nMIDDLE SHELF (60mm = 40mm + 20mm):")
print(f"  ┌───┬───┬───┐")
print(f"  │ ○ │ ○ │ ○ │  ← 3 holes")
print(f"  ├───┴───┴───┤  ← Divider at 20mm")
print(f"  (open space - no walls/floor)")
print(f"\nTOP SHELF (20mm): solid closed box")
print("="*60)
