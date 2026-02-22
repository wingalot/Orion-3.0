#!/usr/bin/env python3
"""
E-Shape Tower - Modified shelves + hollow back wall
Middle shelf: 4cm top + 2cm raised floor
Bottom shelf: 4cm + 4cm (divided)
Back wall: hollow for electronics
"""

import trimesh
import numpy as np

# Dimensions
WIDTH = 340
DEPTH = 160
HEIGHT = 360
WALL_THICK = 30  # Back wall thickness
SHELF_DEPTH = 130  # Shelf extension
SIDE_THICK = 3
FRONT_THICK = 3
TOP_THICK = 3

# Shelf configurations
# Bottom: 80mm total, split into 40mm + 40mm with middle floor
# Middle: 60mm total, 40mm top space + 20mm raised floor
# Top: 20mm solid

Z_BOTTOM = 0
Z_MIDDLE = 180  # 80 + 100
Z_TOP = 340     # 180 + 60 + 100 = 340

HOLE_SIZE = 100
HOLE_COUNT = 3
HOLE_SPACING = (WIDTH - 2*SIDE_THICK - HOLE_COUNT * HOLE_SIZE) / (HOLE_COUNT + 1)

def create_shelf_with_divider(z_pos, total_height, divider_z_ratio, with_holes):
    """Create shelf with divider floor inside
    divider_z_ratio: where to place divider (0-1 of internal height)
    """
    meshes = []
    internal_height = total_height - TOP_THICK
    y_center = WALL_THICK + SHELF_DEPTH/2
    
    # Calculate divider position from bottom of internal space
    divider_z = z_pos + TOP_THICK + (internal_height * divider_z_ratio)
    
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
    front_width = WIDTH - 2*SIDE_THICK
    front = trimesh.creation.box(extents=[front_width, FRONT_THICK, total_height])
    front.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH - FRONT_THICK/2, z_pos + total_height/2])
    meshes.append(front)
    
    # 5. DIVIDER FLOOR (inside, at specified height)
    internal_depth = SHELF_DEPTH - FRONT_THICK
    divider = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
    divider.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, divider_z])
    meshes.append(divider)
    
    # 6. TOP with holes
    if with_holes:
        top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, z_pos + total_height - TOP_THICK/2])
        
        holes = []
        for i in range(HOLE_COUNT):
            x_pos = SIDE_THICK + HOLE_SPACING + HOLE_SIZE/2 + i * (HOLE_SIZE + HOLE_SPACING)
            hole = trimesh.creation.box(extents=[HOLE_SIZE, internal_depth + 2, TOP_THICK + 2])
            hole.apply_translation([x_pos, WALL_THICK + internal_depth/2, z_pos + total_height - TOP_THICK/2])
            holes.append(hole)
        
        top_with_holes = top.difference(trimesh.util.concatenate(holes))
        meshes.append(top_with_holes)
    else:
        top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
        top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, z_pos + total_height - TOP_THICK/2])
        meshes.append(top)
    
    return meshes

def create_middle_shelf_raised():
    """Middle shelf: 60mm total
    - 40mm top space (for plants)
    - 20mm raised floor (so floor is at 40mm from bottom)
    Divider at 40mm from bottom (2/3 of 60mm internal space)
    """
    z_pos = Z_MIDDLE
    total_height = 60
    # Divider at 40mm from bottom = 40/57 ≈ 0.7 of internal
    # Actually: top_thickness=3mm, so internal = 57mm
    # We want divider at 40mm from bottom of internal space
    # That's 40/57 ≈ 0.7
    divider_ratio = 40 / (total_height - TOP_THICK)
    return create_shelf_with_divider(z_pos, total_height, divider_ratio, with_holes=True)

def create_bottom_shelf_divided():
    """Bottom shelf: 80mm total, split into 40mm + 40mm
    Divider in middle (at 40mm from bottom)
    """
    z_pos = Z_BOTTOM
    total_height = 80
    # Divider at 40mm = middle of internal space
    divider_ratio = 40 / (total_height - TOP_THICK)
    return create_shelf_with_divider(z_pos, total_height, divider_ratio, with_holes=True)

def create_hollow_back_wall():
    """Create hollow back wall (box shape) for electronics
    Outer: 30mm thick, 340mm wide, 360mm tall
    Inner: hollow space
    """
    meshes = []
    
    # Wall thickness (outer shell)
    shell_thick = 3
    
    # Outer dimensions
    outer_w = WIDTH
    outer_d = WALL_THICK
    outer_h = HEIGHT
    
    # Inner dimensions (hollow space)
    inner_w = WIDTH - 2*shell_thick
    inner_d = WALL_THICK - 2*shell_thick  # If this is negative, wall is solid
    inner_h = HEIGHT - 2*shell_thick
    
    if inner_d <= 0:
        # Wall too thin to be hollow, make it solid
        wall = trimesh.creation.box(extents=[outer_w, outer_d, outer_h])
        wall.apply_translation([outer_w/2, outer_d/2, outer_h/2])
        return wall
    
    # Create hollow box by making 5 walls (no front face - it's open)
    # Actually let's make a box with one side open (front)
    
    # Back panel
    back = trimesh.creation.box(extents=[outer_w, shell_thick, outer_h])
    back.apply_translation([outer_w/2, shell_thick/2, outer_h/2])
    meshes.append(back)
    
    # Top panel
    top = trimesh.creation.box(extents=[outer_w, outer_d, shell_thick])
    top.apply_translation([outer_w/2, outer_d/2, outer_h - shell_thick/2])
    meshes.append(top)
    
    # Bottom panel
    bottom = trimesh.creation.box(extents=[outer_w, outer_d, shell_thick])
    bottom.apply_translation([outer_w/2, outer_d/2, shell_thick/2])
    meshes.append(bottom)
    
    # Left panel
    left = trimesh.creation.box(extents=[shell_thick, outer_d, outer_h])
    left.apply_translation([shell_thick/2, outer_d/2, outer_h/2])
    meshes.append(left)
    
    # Right panel
    right = trimesh.creation.box(extents=[shell_thick, outer_d, outer_h])
    right.apply_translation([outer_w - shell_thick/2, outer_d/2, outer_h/2])
    meshes.append(right)
    
    return trimesh.util.concatenate(meshes)

def create_top_shelf():
    """Top shelf: 20mm solid (no holes)"""
    meshes = []
    z_pos = Z_TOP
    total_height = 20
    y_center = WALL_THICK + SHELF_DEPTH/2
    front_width = WIDTH - 2*SIDE_THICK
    internal_depth = SHELF_DEPTH - FRONT_THICK
    
    # Bottom
    bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, TOP_THICK])
    bottom.apply_translation([WIDTH/2, y_center, z_pos + TOP_THICK/2])
    meshes.append(bottom)
    
    # Walls
    left = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, total_height])
    left.apply_translation([SIDE_THICK/2, y_center, z_pos + total_height/2])
    meshes.append(left)
    
    right = trimesh.creation.box(extents=[SIDE_THICK, SHELF_DEPTH, total_height])
    right.apply_translation([WIDTH - SIDE_THICK/2, y_center, z_pos + total_height/2])
    meshes.append(right)
    
    front = trimesh.creation.box(extents=[front_width, FRONT_THICK, total_height])
    front.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH - FRONT_THICK/2, z_pos + total_height/2])
    meshes.append(front)
    
    # Solid top
    top = trimesh.creation.box(extents=[front_width, internal_depth, TOP_THICK])
    top.apply_translation([WIDTH/2, WALL_THICK + internal_depth/2, z_pos + total_height - TOP_THICK/2])
    meshes.append(top)
    
    return meshes

def create_e_tower_modified():
    """Create modified E-tower"""
    meshes = []
    
    # Hollow back wall
    back = create_hollow_back_wall()
    meshes.append(back)
    
    # Bottom shelf (divided into 40+40)
    bottom = create_bottom_shelf_divided()
    meshes.extend(bottom)
    
    # Middle shelf (40mm space + 20mm raised floor)
    middle = create_middle_shelf_raised()
    meshes.extend(middle)
    
    # Top shelf (solid)
    top = create_top_shelf()
    meshes.extend(top)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating modified E-tower...")
print("   Middle: 40mm space + 20mm raised floor")
print("   Bottom: 40mm + 40mm (divided)")
print("   Back: hollow for electronics")

model = create_e_tower_modified()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

output = "/home/oreo/.openclaw/workspace/e_tower_modified.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*65)
print("MODIFIED E-TOWER")
print("="*65)
print(f"Overall: {WIDTH}mm × {DEPTH}mm × {HEIGHT}mm")
print(f"\nBACK WALL (E vertical):")
print(f"  Hollow box for electronics (3mm shell)")
print(f"\nBOTTOM SHELF (80mm total):")
print(f"  ├─ Top section: 40mm (with 3 holes for pots)")
print(f"  ├─ Middle floor (divider)")
print(f"  └─ Bottom section: 40mm (empty space)")
print(f"\nMIDDLE SHELF (60mm total):")
print(f"  ├─ Top section: 40mm (with 3 holes for plants)")
print(f"  └─ Raised floor: 20mm (floor moved up)")
print(f"\nTOP SHELF (20mm):")
print(f"  Solid box (no holes)")
print("="*65)
