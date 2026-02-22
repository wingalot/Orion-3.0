#!/usr/bin/env python3
"""
Microgreens Tower Frame - 3D Printable STL Generator
Dimensions: 340mm (W) x 160mm (D) x 360mm (H)
"""

import trimesh
import numpy as np

# Dimensions (in mm)
WIDTH = 340       # Total width
DEPTH = 160       # Total depth  
HEIGHT = 360      # Total height
WALL_THICKNESS = 3  # Wall thickness

# Shelf configurations
SHELVES = [
    {"z": 0, "thickness": 80, "holes": True},      # Bottom - 8cm, with holes
    {"z": 180, "thickness": 60, "holes": True},    # Middle - 6cm, with holes (80 + 100 gap = 180)
    {"z": 340, "thickness": 20, "holes": False},   # Top - 2cm, solid (180 + 60 + 100 = 340)
]

# Pot holes configuration
HOLE_SIZE = 100  # 10x10cm
HOLE_SPACING = 20  # Space between holes
# Calculate starting X for 3 holes centered
# 3 holes * 100mm + 2 gaps * 20mm = 340mm total
# Start at 0, but we need to center them
# Total holes width = 3*100 + 2*20 = 340mm exactly!
HOLE_START_X = 20  # Start after left wall thickness

def create_box(width, depth, height, wall_thickness):
    """Create hollow box with 5 walls (no back wall - it will be removable)"""
    meshes = []
    
    # Front wall
    front = trimesh.creation.box(extents=[width, wall_thickness, height])
    front.apply_translation([width/2, wall_thickness/2, height/2])
    meshes.append(front)
    
    # Left wall  
    left = trimesh.creation.box(extents=[wall_thickness, depth, height])
    left.apply_translation([wall_thickness/2, depth/2, height/2])
    meshes.append(left)
    
    # Right wall
    right = trimesh.creation.box(extents=[wall_thickness, depth, height])
    right.apply_translation([width - wall_thickness/2, depth/2, height/2])
    meshes.append(right)
    
    return meshes

def create_shelf_with_holes(width, depth, thickness, z_pos, has_holes, wall_thickness):
    """Create a shelf with optional pot holes"""
    
    # Create full shelf
    shelf = trimesh.creation.box(extents=[width - 2*wall_thickness, depth, thickness])
    shelf.apply_translation([width/2, depth/2, z_pos + thickness/2])
    
    if not has_holes:
        return [shelf]
    
    # Cut holes for pots
    holes = []
    # 3 holes side by side
    hole_positions = [
        wall_thickness + HOLE_START_X + HOLE_SIZE/2,
        wall_thickness + HOLE_START_X + HOLE_SIZE + HOLE_SPACING + HOLE_SIZE/2,
        wall_thickness + HOLE_START_X + 2*(HOLE_SIZE + HOLE_SPACING) + HOLE_SIZE/2
    ]
    
    for x_pos in hole_positions:
        hole = trimesh.creation.box(extents=[HOLE_SIZE, depth + 2, thickness + 2])
        hole.apply_translation([x_pos, depth/2, z_pos + thickness/2])
        holes.append(hole)
    
    # Subtract holes from shelf
    if holes:
        shelf_with_holes = shelf.difference(trimesh.util.concatenate(holes))
        return [shelf_with_holes]
    
    return [shelf]

def create_back_panel(width, depth, height, wall_thickness):
    """Create removable back panel with screw holes"""
    # Panel dimensions - covers all 3 levels
    panel_thickness = 3
    
    # Main panel
    panel = trimesh.creation.box(extents=[width - 2*wall_thickness, panel_thickness, height])
    panel.apply_translation([width/2, depth - panel_thickness/2, height/2])
    
    # Screw holes (4mm diameter) - 4 corners per level = 12 holes total
    # Positions: near corners of each shelf section
    screw_holes = []
    screw_diameter = 4
    screw_depth = panel_thickness + 2
    
    # For each shelf level, add screw holes at corners
    corner_offsets = [
        (wall_thickness + 10, 10),  # Bottom left
        (width - wall_thickness - 10, 10),  # Bottom right
    ]
    
    # Actually, let's do 4 screws per shelf level for stability
    screw_positions = []
    
    for shelf in SHELVES:
        z_center = shelf["z"] + shelf["thickness"]/2
        # 4 corners per shelf
        screw_positions.extend([
            (wall_thickness + 15, z_center),
            (width - wall_thickness - 15, z_center),
        ])
    
    for x, z in screw_positions:
        hole = trimesh.creation.cylinder(radius=screw_diameter/2, height=screw_depth)
        hole.apply_translation([x, depth - panel_thickness/2, z])
        screw_holes.append(hole)
    
    if screw_holes:
        panel = panel.difference(trimesh.util.concatenate(screw_holes))
    
    return panel

def create_frame():
    """Create the complete microgreens tower frame"""
    all_meshes = []
    
    # Create main walls (front, left, right)
    wall_meshes = create_box(WIDTH, DEPTH, HEIGHT, WALL_THICKNESS)
    all_meshes.extend(wall_meshes)
    
    # Create shelves
    for shelf in SHELVES:
        shelf_meshes = create_shelf_with_holes(
            WIDTH, DEPTH, shelf["thickness"], 
            shelf["z"], shelf["holes"], WALL_THICKNESS
        )
        all_meshes.extend(shelf_meshes)
    
    # Create removable back panel
    back_panel = create_back_panel(WIDTH, DEPTH, HEIGHT, WALL_THICKNESS)
    all_meshes.append(back_panel)
    
    # Combine all meshes
    frame = trimesh.util.concatenate(all_meshes)
    
    return frame

# Generate the model
print("Generating microgreens tower frame...")
model = create_frame()

# Check if manifold
print(f"Is manifold: {model.is_watertight}")
print(f"Volume: {model.volume / 1000:.1f} cm³")
print(f"Surface area: {model.area / 100:.1f} cm²")

# Export to STL
output_path = "/home/oreo/.openclaw/workspace/microgreens_tower.stl"
model.export(output_path)
print(f"✅ Exported to: {output_path}")

# Also export back panel separately for easier printing
print("\nGenerating separate back panel...")
back_panel = create_back_panel(WIDTH, DEPTH, HEIGHT, WALL_THICKNESS)
back_path = "/home/oreo/.openclaw/workspace/microgreens_back_panel.stl"
back_panel.export(back_path)
print(f"✅ Back panel exported to: {back_path}")

print("\n📐 Model Summary:")
print(f"  Overall: {WIDTH}mm x {DEPTH}mm x {HEIGHT}mm")
print(f"  Wall thickness: {WALL_THICKNESS}mm")
print(f"  Pot holes: 6 x {HOLE_SIZE}mm x {HOLE_SIZE}mm")
print(f"  Screw holes: 4mm diameter (for M4 screws)")
