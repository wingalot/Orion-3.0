#!/usr/bin/env python3
"""
Microgreens Tower Frame - E-SHAPE from side view
Dimensions: 340mm (W) x 160mm (D) x 360mm (H)
E-shape from side: Vertical wall on RIGHT, 3 shelves extend to LEFT
"""

import trimesh
import numpy as np

# Dimensions (in mm)
WIDTH = 340       # Total width - shelves extend this direction
DEPTH = 160       # Depth - front to back (constant)
HEIGHT = 360      # Total height
WALL_THICKNESS = 3  # Vertical wall thickness
SHELF_THICKNESS = 3  # Shelf thickness (horizontal part)

# Shelf configurations
# From bottom to top, measured from bottom (z=0)
SHELVES = [
    {"z": 0, "thickness": 80, "holes": True},      # Bottom - 8cm thick
    {"z": 180, "thickness": 60, "holes": True},    # Middle - 6cm thick (0+80+100=180)
    {"z": 340, "thickness": 20, "holes": False},   # Top - 2cm thick (180+60+100=340)
]

# Pot holes configuration
HOLE_SIZE = 100  # 10x10cm square holes
# 3 holes side by side in WIDTH direction, centered
HOLE_SPACING = (WIDTH - WALL_THICKNESS - 3*HOLE_SIZE) / 4

def create_e_shape_side():
    """Create E-shape from side view:
    - Vertical wall on the RIGHT side (at x=WIDTH)
    - 3 shelves extending to the LEFT (toward x=0)
    """
    all_meshes = []
    
    # 1. RIGHT VERTICAL WALL (full height, extends full depth)
    # Positioned at the right edge
    right_wall = trimesh.creation.box(extents=[WALL_THICKNESS, DEPTH, HEIGHT])
    right_wall.apply_translation([WIDTH - WALL_THICKNESS/2, DEPTH/2, HEIGHT/2])
    all_meshes.append(right_wall)
    
    # 2. Create shelves extending from right wall to left
    for shelf in SHELVES:
        shelf_meshes = create_shelf_extending_left(
            shelf["z"], shelf["thickness"], shelf["holes"]
        )
        all_meshes.extend(shelf_meshes)
    
    return trimesh.util.concatenate(all_meshes)

def create_shelf_extending_left(z_pos, thickness, has_holes):
    """Create a shelf that extends from right wall toward left
    Shelf goes from x=WALL_THICKNESS to x=WIDTH (attached to right wall)
    """
    meshes = []
    
    # Shelf dimensions
    shelf_length = WIDTH - WALL_THICKNESS  # How far it extends from wall
    
    if not has_holes:
        # Solid shelf - simple box
        shelf = trimesh.creation.box(extents=[shelf_length, DEPTH, thickness])
        # Position: extends from right wall toward left
        shelf.apply_translation([shelf_length/2 + WALL_THICKNESS, DEPTH/2, z_pos + thickness/2])
        meshes.append(shelf)
        return meshes
    
    # Shelf WITH HOLES - need to create frame with 3 cutouts
    full_shelf = trimesh.creation.box(extents=[shelf_length, DEPTH, thickness])
    full_shelf.apply_translation([shelf_length/2 + WALL_THICKNESS, DEPTH/2, z_pos + thickness/2])
    
    # Create 3 holes to subtract
    holes = []
    # Calculate hole positions (from left to right, but not including the wall area)
    # Holes start from left edge of shelf
    hole_step = HOLE_SIZE + HOLE_SPACING
    start_x = HOLE_SPACING + HOLE_SIZE/2
    
    hole_positions = [
        start_x,
        start_x + hole_step,
        start_x + 2*hole_step
    ]
    
    for x_pos in hole_positions:
        # Hole goes all the way through the shelf (in Y direction)
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

def create_removable_wall():
    """Create a removable panel that covers the LEFT side (optional)"""
    panel_thickness = 3
    
    # Panel covers the left side where shelves end
    panel = trimesh.creation.box(extents=[panel_thickness, DEPTH, HEIGHT])
    panel.apply_translation([panel_thickness/2, DEPTH/2, HEIGHT/2])
    
    # Add screw holes (4mm diameter) - at corners and middle for each shelf
    screw_holes = []
    
    # Positions: left side corners at each shelf level
    for shelf in SHELVES:
        z_center = shelf["z"] + shelf["thickness"]/2
        screw_positions = [
            (10, z_center),  # Front
            (DEPTH - 10, z_center),  # Back
        ]
        for y, z in screw_positions:
            hole = trimesh.creation.cylinder(radius=2, height=panel_thickness + 2)
            # Rotate to go through the panel (along X axis)
            hole.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
            hole.apply_translation([panel_thickness/2, y, z])
            screw_holes.append(hole)
    
    if screw_holes:
        panel = panel.difference(trimesh.util.concatenate(screw_holes))
    
    return panel

# Generate the E-shape model (side view)
print("🌱 Generating E-shape microgreens tower (side view)...")
print(f"   Dimensions: {WIDTH}mm x {DEPTH}mm x {HEIGHT}mm")
print(f"   Shape: E from side (right wall + 3 shelves extending left)")

e_frame = create_e_shape_side()

# Check model
print(f"\n✅ Is manifold: {e_frame.is_watertight}")
print(f"📊 Volume: {e_frame.volume / 1000:.1f} cm³")
print(f"📐 Surface area: {e_frame.area / 100:.1f} cm²")

# Export main frame
output_path = "/home/oreo/.openclaw/workspace/microgreens_tower_E_side.stl"
e_frame.export(output_path)
print(f"\n💾 Main frame exported: {output_path}")

# Generate optional left side panel (removable)
print("\n🔩 Generating removable left side panel...")
left_panel = create_removable_wall()
left_path = "/home/oreo/.openclaw/workspace/microgreens_left_panel.stl"
left_panel.export(left_path)
print(f"💾 Left panel exported: {left_path}")

print("\n" + "="*50)
print("📋 FINAL MODEL SPECIFICATIONS:")
print("="*50)
print(f"Shape: E-shape from SIDE view")
print(f"Overall: {WIDTH}mm (W) x {DEPTH}mm (D) x {HEIGHT}mm (H)")
print(f"\nStructure:")
print(f"  • RIGHT side: Full vertical wall (attached to all shelves)")
print(f"  • 3 shelves extend LEFT from the wall")
print(f"\nShelves (from bottom to top):")
print(f"  1. Bottom: 80mm thick (Z: 0-80mm), 3 holes")
print(f"  2. Middle: 60mm thick (Z: 180-240mm), 3 holes")
print(f"  3. Top: 20mm thick (Z: 340-360mm), solid")
print(f"\nGap between shelves: 100mm")
print(f"Pot holes: 6 total (3 on middle + 3 on bottom)")
print(f"Hole size: 100mm x 100mm square")
print("="*50)
print("\n📐 SIDE VIEW (looking from front):")
print("     ←───── 337mm ─────→")
print("     ┌─────────────────┐│  ↑")
print("     │                 ││  │")
print("     │   ┌───┐ ┌───┐   ││  │ 20mm")
print("     │   │   │ │   │   ││  ↓")
print("     │   └───┘ └───┘   ││  ← Top shelf (solid)")
print("     │                 ││  ↑")
print("     │   ┌───┐ ┌───┐   ││  │")
print("     │   │ ○ │ │ ○ │   ││  │ 60mm")
print("     │   └───┘ └───┘   ││  ↓")
print("     │       ○         ││  ← Middle shelf (3 holes)")
print("     │                 ││  ↑")
print("     │   ┌───┐ ┌───┐   ││  │")
print("     │   │ ○ │ │ ○ │   ││  │ 80mm")
print("     │   └───┘ └───┘   ││  ↓")
print("     │       ○         ││  ← Bottom shelf (3 holes)")
print("     └─────────────────┘│  ← Vertical wall on RIGHT")
print("                         360mm total height")
print("="*50)
