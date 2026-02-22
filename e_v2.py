#!/usr/bin/env python3
"""
E-Shape Tower - Open back wall (no back panel)
Each shelf is a closed box, only 3 holes on top are open
Back wall: open box (no back panel, will be covered later)
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

def create_closed_box_shelf(z_pos, total_height, divider_z=None, with_holes=True):
    """Create closed box shelf:
    - Top with 3 holes (if with_holes)
    - Solid bottom
    - Side walls (left/right)
    - Front wall
    - Open back (connects to E-wall)
    - Optional divider floor at divider_z (from bottom of internal space)
    """
    meshes = []
    internal_height = total_height - TOP_THICK
    y_center = WALL_THICK + SHELF_DEPTH/2
    internal_depth = SHELF_DEPTH - FRONT_THICK
    front_width = WIDTH - 2*SIDE_THICK
    
    # 1. BOTTOM floor
    bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, TOP_THICK])
    bottom.apply_translation([WIDTH/2, y_center, z_pos + TOP_THICK/2])
    meshes.append(bottom)
    
    # 2. LEFT WALL (full height)
    left = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, total_height])
    left.apply_translation([SIDE_THICK/2, y_center, z_pos + total_height/2])
    meshes.append(left)
    
    # 3. RIGHT WALL (full height)
    right = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, total_height])
    right.apply_translation([WIDTH - SIDE_THICK/2, y_center, z_pos + total_height/2])
    meshes.append(right)
    
    # 4. FRONT WALL (full height)
    front = trimesh.creation.box(extents=[front_width, FRONT_THICK, total_height])
    front.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH - FRONT_THICK/2, 
                            z_pos + total_height/2])
    meshes.append(front)
    
    # 5. DIVIDER FLOOR (if specified)
    if divider_z is not None and divider_z > 0:
        divider = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
        divider_z_abs = z_pos + TOP_THICK + divider_z
        divider.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, divider_z_abs])
        meshes.append(divider)
    
    # 6. TOP with 3 holes
    if with_holes:
        top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                              z_pos + total_height - TOP_THICK/2])
        
        # Cut 3 holes
        holes = []
        for i in range(HOLE_COUNT):
            x_pos = SIDE_THICK + HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
            hole = trimesh.creation.box(extents=[HOLE_SIZE, internal_depth + 2, TOP_THICK + 2])
            hole.apply_translation([x_pos, WALL_THICK + internal_depth/2, 
                                   z_pos + total_height - TOP_THICK/2])
            holes.append(hole)
        
        top = top.difference(trimesh.util.concatenate(holes))
        meshes.append(top)
    else:
        # Solid top
        top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, 
                              z_pos + total_height - TOP_THICK/2])
        meshes.append(top)
    
    return meshes

def create_open_back_wall():
    """Create hollow back wall WITHOUT back panel (open from back)
    Only: top, bottom, left, right panels forming a U-shape/channel
    """
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

def create_e_tower_v2():
    """Create final E-tower"""
    meshes = []
    
    # Back wall (open from back - no back panel)
    back_wall = create_open_back_wall()
    meshes.extend(back_wall)
    
    # Bottom shelf: 80mm, divided at 40mm (from bottom of internal space)
    # Internal height = 80 - 3 = 77mm, divider at 40mm
    bottom = create_closed_box_shelf(Z_BOTTOM, 80, divider_z=40, with_holes=True)
    meshes.extend(bottom)
    
    # Middle shelf: 60mm, divider at 40mm (so top space is 40mm, floor is raised)
    # Internal height = 60 - 3 = 57mm, divider at 40mm from bottom
    middle = create_closed_box_shelf(Z_MIDDLE, 60, divider_z=40, with_holes=True)
    meshes.extend(middle)
    
    # Top shelf: 20mm, solid (no holes, no divider)
    top = create_closed_box_shelf(Z_TOP, 20, divider_z=None, with_holes=False)
    meshes.extend(top)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating E-tower v2...")
print("   Back wall: NO back panel (open)")
print("   Shelves: closed boxes, only holes on top open")

model = create_e_tower_v2()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

output = "/home/oreo/.openclaw/workspace/e_tower_v2.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*60)
print("E-TOWER v2 - FINAL")
print("="*60)
print(f"Size: {WIDTH}mm × {DEPTH}mm × {HEIGHT}mm")
print(f"\nBACK WALL (E vertical):")
print(f"  ┌───────────────────────────┐  ← Top")
print(f"  │                           │")
print(f"  │  (OPEN - NO BACK PANEL)   │  ← Hollow for electronics")
print(f"  │                           │")
print(f"  └───────────────────────────┘  ← Bottom")
print(f"  Cover will be added separately")
print(f"\nBOTTOM SHELF (80mm):")
print(f"  ┌───┬───┬───┐")
print(f"  │ ○ │ ○ │ ○ │  ← 3 holes (only openings)")
print(f"  ├───┴───┴───┤  ← Divider at 40mm")
print(f"  │           │  ← Lower 40mm space")
print(f"  └───────────┘")
print(f"\nMIDDLE SHELF (60mm):")
print(f"  ┌───┬───┬───┐")
print(f"  │ ○ │ ○ │ ○ │  ← 3 holes")
print(f"  ├───┴───┴───┤  ← Raised floor (40mm up)")
print(f"  └───────────┘  ← 20mm space below")
print(f"\nTOP SHELF (20mm):")
print(f"  ┌───────────┐")
print(f"  │ (closed)  │  ← Solid, no holes")
print(f"  └───────────┘")
print("="*60)
