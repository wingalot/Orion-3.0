#!/usr/bin/env python3
"""
E-Shape Tower v5 - All closed boxes
Middle: 4cm closed + 2cm closed (both with floors)
Bottom: 4cm + 4cm closed
Top: 2cm closed
Back: U-shape (no back panel)
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

def create_closed_box_full(z_pos, box_height, with_holes=False):
    """Create a fully closed box with all walls and floor"""
    meshes = []
    y_center = WALL_THICK + SHELF_DEPTH/2
    internal_depth = SHELF_DEPTH - FRONT_THICK
    front_width = WIDTH - 2*SIDE_THICK
    
    # Side walls
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
    
    # Bottom floor
    bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, TOP_THICK])
    bottom.apply_translation([WIDTH/2, y_center, z_pos + TOP_THICK/2])
    meshes.append(bottom)
    
    # Top with or without holes
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
    
    return meshes

def create_bottom_shelf():
    """Bottom: 80mm = 40mm + 40mm, both fully closed"""
    meshes = []
    
    # Upper 40mm with holes
    upper = create_closed_box_full(Z_BOTTOM + 40, 40, with_holes=True)
    meshes.extend(upper)
    
    # Lower 40mm closed
    lower = create_closed_box_full(Z_BOTTOM, 40, with_holes=False)
    meshes.extend(lower)
    
    return meshes

def create_middle_shelf():
    """Middle: 60mm = 40mm + 20mm, both fully closed"""
    meshes = []
    
    # Upper 40mm with holes
    upper = create_closed_box_full(Z_MIDDLE + 20, 40, with_holes=True)
    meshes.extend(upper)
    
    # Lower 20mm closed (with floor!)
    lower = create_closed_box_full(Z_MIDDLE, 20, with_holes=False)
    meshes.extend(lower)
    
    return meshes

def create_top_shelf():
    """Top: 20mm closed"""
    return create_closed_box_full(Z_TOP, 20, with_holes=False)

def create_open_back_wall():
    """Back wall U-shape (no back panel)"""
    meshes = []
    shell_thick = 3
    
    # Top
    top = trimesh.creation.box(extents=[WIDTH, WALL_THICK, shell_thick])
    top.apply_translation([WIDTH/2, WALL_THICK/2, HEIGHT - shell_thick/2])
    meshes.append(top)
    
    # Bottom
    bottom = trimesh.creation.box(extents=[WIDTH, WALL_THICK, shell_thick])
    bottom.apply_translation([WIDTH/2, WALL_THICK/2, shell_thick/2])
    meshes.append(bottom)
    
    # Left
    left = trimesh.creation.box(extents=[shell_thick, WALL_THICK, HEIGHT - 2*shell_thick])
    left.apply_translation([shell_thick/2, WALL_THICK/2, HEIGHT/2])
    meshes.append(left)
    
    # Right
    right = trimesh.creation.box(extents=[shell_thick, WALL_THICK, HEIGHT - 2*shell_thick])
    right.apply_translation([WIDTH - shell_thick/2, WALL_THICK/2, HEIGHT/2])
    meshes.append(right)
    
    return meshes

def create_e_tower_v5():
    """Create E-tower v5 - all closed boxes"""
    meshes = []
    
    # Back wall
    back_wall = create_open_back_wall()
    meshes.extend(back_wall)
    
    # Shelves
    meshes.extend(create_bottom_shelf())
    meshes.extend(create_middle_shelf())
    meshes.extend(create_top_shelf())
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating E-tower v5...")
print("   ALL boxes fully closed with floors")

model = create_e_tower_v5()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

output = "/home/oreo/.openclaw/workspace/e_tower_v5.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*60)
print("E-TOWER v5 - ALL CLOSED")
print("="*60)
print(f"Size: {WIDTH}mm × {DEPTH}mm × {HEIGHT}mm")
print(f"\nBOTTOM (80mm = 40mm + 40mm):")
print(f"  ┌───┬───┬───┐  ← Upper 40mm, holes")
print(f"  │ ○ │ ○ │ ○ │  ← Closed box")
print(f"  ├───┴───┴───┤")
print(f"  │ (closed)  │  ← Lower 40mm, closed box")
print(f"  └───────────┘")
print(f"\nMIDDLE (60mm = 40mm + 20mm):")
print(f"  ┌───┬───┬───┐  ← Upper 40mm, holes")
print(f"  │ ○ │ ○ │ ○ │  ← Closed box")
print(f"  ├───┴───┴───┤")
print(f"  │ (closed)  │  ← Lower 20mm, CLOSED BOX (with floor)")
print(f"  └───────────┘")
print(f"\nTOP (20mm): closed box")
print(f"\nBACK: U-shape (no back panel)")
print("="*60)
