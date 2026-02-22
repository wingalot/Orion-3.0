#!/usr/bin/env python3
"""
Microgreens Tower Frame - E-SHAPE Design
Dimensions: 340mm (W) x 160mm (D) x 360mm (H)
E-shape: Vertical back wall with 3 horizontal shelves extending forward
"""

import trimesh
import numpy as np

# Dimensions (in mm)
WIDTH = 340       # Total width (horizontal)
DEPTH = 160       # Depth - how far shelves extend from back wall
HEIGHT = 360      # Total height
WALL_THICKNESS = 3  # Back wall thickness
SHELF_THICKNESS = 3  # Shelf thickness

# Shelf configurations - E shape means shelves extend from back wall
# Bottom shelf at z=0, then gap, then middle, then gap, then top
SHELVES = [
    {"z": 0, "thickness": 80, "holes": True},      # Bottom - 8cm thick
    {"z": 180, "thickness": 60, "holes": True},    # Middle - 6cm thick (0+80+100 gap=180)
    {"z": 340, "thickness": 20, "holes": False},   # Top - 2cm thick (180+60+100=340)
]

# Pot holes configuration
HOLE_SIZE = 100  # 10x10cm square holes
# 3 holes side by side, centered in width
HOLE_SPACING = (WIDTH - 3*HOLE_SIZE) / 4  # Equal spacing

def create_e_shape_frame():
    """Create E-shape frame: vertical back wall + 3 shelves extending forward"""
    all_meshes = []
    
    # 1. BACK WALL (vertical, full height and width)
    back_wall = trimesh.creation.box(extents=[WIDTH, WALL_THICKNESS, HEIGHT])
    back_wall.apply_translation([WIDTH/2, WALL_THICKNESS/2, HEIGHT/2])
    all_meshes.append(back_wall)
    
    # 2. SIDE SUPPORTS (vertical posts on left and right, connecting all shelves)
    # Left post
    left_post = trimesh.creation.box(extents=[WALL_THICKNESS, DEPTH, HEIGHT])
    left_post.apply_translation([WALL_THICKNESS/2, DEPTH/2, HEIGHT/2])
    all_meshes.append(left_post)
    
    # Right post
    right_post = trimesh.creation.box(extents=[WALL_THICKNESS, DEPTH, HEIGHT])
    right_post.apply_translation([WIDTH - WALL_THICKNESS/2, DEPTH/2, HEIGHT/2])
    all_meshes.append(right_post)
    
    # 3. SHELVES extending from back wall to front
    for shelf in SHELVES:
        shelf_meshes = create_shelf(
            shelf["z"], shelf["thickness"], shelf["holes"]
        )
        all_meshes.extend(shelf_meshes)
    
    return trimesh.util.concatenate(all_meshes)

def create_shelf(z_pos, thickness, has_holes):
    """Create a shelf extending from back wall, with optional holes"""
    meshes = []
    
    # Shelf extends from back wall (y=0) to front (y=DEPTH)
    # But we need to leave gaps for the holes
    
    if not has_holes:
        # Solid shelf - simple box
        shelf = trimesh.creation.box(extents=[WIDTH, DEPTH, thickness])
        shelf.apply_translation([WIDTH/2, DEPTH/2, z_pos + thickness/2])
        meshes.append(shelf)
        return meshes
    
    # Shelf WITH HOLES - create frame with 3 square cutouts
    # Each hole is 100x100mm
    
    # Create the shelf as a solid first
    full_shelf = trimesh.creation.box(extents=[WIDTH, DEPTH, thickness])
    full_shelf.apply_translation([WIDTH/2, DEPTH/2, z_pos + thickness/2])
    
    # Create 3 holes to subtract
    holes = []
    hole_positions = [
        HOLE_SPACING + HOLE_SIZE/2,
        HOLE_SPACING + HOLE_SIZE + HOLE_SPACING + HOLE_SIZE/2,
        HOLE_SPACING + 2*(HOLE_SIZE + HOLE_SPACING) + HOLE_SIZE/2
    ]
    
    for x_pos in hole_positions:
        # Hole goes all the way through the shelf
        hole = trimesh.creation.box(extents=[HOLE_SIZE, DEPTH + 2, thickness + 2])
        hole.apply_translation([x_pos, DEPTH/2, z_pos + thickness/2])
        holes.append(hole)
    
    # Subtract holes
    if holes:
        shelf_with_holes = full_shelf.difference(trimesh.util.concatenate(holes))
        meshes.append(shelf_with_holes)
    else:
        meshes.append(full_shelf)
    
    return meshes

def create_removable_back_panel():
    """Create removable panel that covers the back (optional accessory)"""
    # This would be a thin panel that screws onto the back
    panel_thickness = 3
    
    panel = trimesh.creation.box(extents=[WIDTH, panel_thickness, HEIGHT])
    panel.apply_translation([WIDTH/2, -panel_thickness/2, HEIGHT/2])
    
    # Add screw holes (4mm diameter) - 4 corners
    screw_holes = []
    screw_positions = [
        (20, 20), (WIDTH-20, 20),
        (20, HEIGHT-20), (WIDTH-20, HEIGHT-20)
    ]
    
    for x, z in screw_positions:
        hole = trimesh.creation.cylinder(radius=2, height=panel_thickness + 2)
        hole.apply_translation([x, -panel_thickness/2, z])
        screw_holes.append(hole)
    
    if screw_holes:
        panel = panel.difference(trimesh.util.concatenate(screw_holes))
    
    return panel

# Generate the E-shape model
print("🌱 Generating E-shape microgreens tower...")
print(f"   Dimensions: {WIDTH}mm x {DEPTH}mm x {HEIGHT}mm")
print(f"   Shape: E-shape (back wall + 3 extending shelves)")

e_frame = create_e_shape_frame()

# Check model
print(f"\n✅ Is manifold: {e_frame.is_watertight}")
print(f"📊 Volume: {e_frame.volume / 1000:.1f} cm³")
print(f"📐 Surface area: {e_frame.area / 100:.1f} cm²")

# Export main frame
output_path = "/home/oreo/.openclaw/workspace/microgreens_tower_E.stl"
e_frame.export(output_path)
print(f"\n💾 Main frame exported: {output_path}")

# Generate optional back cover panel
print("\n🔩 Generating optional back cover panel...")
back_panel = create_removable_back_panel()
back_path = "/home/oreo/.openclaw/workspace/microgreens_back_cover.stl"
back_panel.export(back_path)
print(f"💾 Back cover exported: {back_path}")

print("\n" + "="*50)
print("📋 FINAL MODEL SPECIFICATIONS:")
print("="*50)
print(f"Shape: E-shape (vertical back + horizontal shelves)")
print(f"Overall: {WIDTH}mm (W) x {DEPTH}mm (D) x {HEIGHT}mm (H)")
print(f"\nShelves (from bottom to top):")
print(f"  1. Bottom: 80mm thick, 3 holes (100x100mm each)")
print(f"  2. Middle: 60mm thick, 3 holes (100x100mm each)")
print(f"  3. Top: 20mm thick, solid (no holes)")
print(f"\nGap between shelves: 100mm")
print(f"Side supports: Left and right vertical posts")
print(f"Back wall: Full coverage (can add removable panel)")
print("="*50)
