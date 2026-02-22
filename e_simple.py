#!/usr/bin/env python3
"""
Simple E-Shape Tower Frame
Dimensions: 340mm (W) x 160mm (D) x 360mm (H)
Pure E-shape: vertical wall on left, 3 horizontal shelves extending right
"""

import trimesh
import numpy as np

# Dimensions (mm)
WIDTH = 340       # Total width
DEPTH = 160       # Front-to-back depth
HEIGHT = 360      # Total height
THICKNESS = 3     # Wall/shelf thickness

# Shelf positions (z = height from bottom)
# Bottom: 0 to 80mm
# Gap: 80 to 180mm (100mm gap)
# Middle: 180 to 240mm (60mm thick)
# Gap: 240 to 340mm (100mm gap)  
# Top: 340 to 360mm (20mm thick)

def create_simple_e():
    """Create simple E shape:
    - Vertical wall on LEFT side (full height)
    - 3 shelves extending to RIGHT
    """
    meshes = []
    
    # 1. LEFT VERTICAL WALL (full height, full depth)
    left_wall = trimesh.creation.box(extents=[THICKNESS, DEPTH, HEIGHT])
    left_wall.apply_translation([THICKNESS/2, DEPTH/2, HEIGHT/2])
    meshes.append(left_wall)
    
    # 2. BOTTOM SHELF (thickest, 80mm)
    # Extends from left wall to right edge
    bottom = trimesh.creation.box(extents=[WIDTH, DEPTH, 80])
    bottom.apply_translation([WIDTH/2, DEPTH/2, 40])  # z=0 to 80, center at 40
    meshes.append(bottom)
    
    # 3. MIDDLE SHELF (60mm thick)
    # Starts at z=180 (80 + 100 gap)
    middle = trimesh.creation.box(extents=[WIDTH, DEPTH, 60])
    middle.apply_translation([WIDTH/2, DEPTH/2, 180 + 30])  # z=180 to 240, center at 210
    meshes.append(middle)
    
    # 4. TOP SHELF (thinnest, 20mm)
    # Starts at z=340 (240 + 100 gap)
    top = trimesh.creation.box(extents=[WIDTH, DEPTH, 20])
    top.apply_translation([WIDTH/2, DEPTH/2, 340 + 10])  # z=340 to 360, center at 350
    meshes.append(top)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating simple E-shape tower...")
model = create_simple_e()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

# Export
output = "/home/oreo/.openclaw/workspace/e_tower_simple.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*40)
print("E-SHAPE SUMMARY:")
print("="*40)
print(f"Overall: {WIDTH}mm x {DEPTH}mm x {HEIGHT}mm")
print(f"Wall thickness: {THICKNESS}mm")
print("\nStructure:")
print("  [LEFT] Vertical wall (full height)")
print("         ║")
print("    80mm ╠═══════════ →  [BOTTOM shelf]")
print("         ║ (gap 100mm)")
print("    60mm ╠═══════════ →  [MIDDLE shelf]")  
print("         ║ (gap 100mm)")
print("    20mm ╠═══════════ →  [TOP shelf]")
print("="*40)
