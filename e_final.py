#!/usr/bin/env python3
"""
E-Shape Tower - Correct orientation
Dimensions: 340mm (W) x 160mm (D) x 360mm (H)
E vertical wall: 340mm wide, 30mm thick
Shelves: 340mm wide, 130mm deep
"""

import trimesh

# Dimensions
WIDTH = 340       # X: left-to-right (340mm)
DEPTH = 160       # Y: back-to-front (30mm wall + 130mm shelf)
HEIGHT = 360      # Z: bottom-to-top

# E-shape
WALL_THICK = 30   # 3cm - back vertical wall
SHELF_DEPTH = 130 # 13cm - shelves extend forward (160-30)

# Shelf thicknesses
BOTTOM_THICK = 80   # 8cm
MIDDLE_THICK = 60   # 6cm  
TOP_THICK = 20      # 2cm

# Heights (Z positions)
BOTTOM_Z = 0
MIDDLE_Z = 180  # 80 + 100 gap
TOP_Z = 340     # 180 + 60 + 100

def create_e_correct():
    """Create E-shape:
    - Vertical wall on BACK (y=0 to 30), full width
    - 3 shelves extend FORWARD (y=30 to 160)
    """
    meshes = []
    
    # 1. BACK VERTICAL WALL (the | of E)
    # Full width (340), 30mm thick, full height
    back_wall = trimesh.creation.box(extents=[WIDTH, WALL_THICK, HEIGHT])
    back_wall.apply_translation([WIDTH/2, WALL_THICK/2, HEIGHT/2])
    meshes.append(back_wall)
    
    # 2. BOTTOM SHELF (at z=0)
    # Full width, extends 130mm forward
    bottom = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, BOTTOM_THICK])
    bottom.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH/2, BOTTOM_THICK/2])
    meshes.append(bottom)
    
    # 3. MIDDLE SHELF (at z=180)
    middle = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, MIDDLE_THICK])
    middle.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH/2, MIDDLE_Z + MIDDLE_THICK/2])
    meshes.append(middle)
    
    # 4. TOP SHELF (at z=340)
    top = trimesh.creation.box(extents=[WIDTH, SHELF_DEPTH, TOP_THICK])
    top.apply_translation([WIDTH/2, WALL_THICK + SHELF_DEPTH/2, TOP_Z + TOP_THICK/2])
    meshes.append(top)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating E-tower (correct orientation)...")
model = create_e_correct()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

# Export
output = "/home/oreo/.openclaw/workspace/e_tower_final.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*50)
print("E-TOWER FINAL SPECIFICATIONS:")
print("="*50)
print(f"Overall: {WIDTH}mm(W) × {DEPTH}mm(D) × {HEIGHT}mm(H)")
print(f"\nE-shape structure:")
print(f"  ┌─────────────────────────────┐ ← Top (20mm)")
print(f"  │                             │")
print(f"  ║                             ║ ← 100mm gap")
print(f"  │                             │")
print(f"  ├─────────────────────────────┤ ← Middle (60mm)")
print(f"  │                             │")
print(f"  ║                             ║ ← 100mm gap")
print(f"  │                             │")
print(f"  ├─────────────────────────────┤ ← Bottom (80mm)")
print(f"  │                             │")
print(f"  └─────────────────────────────┘")
print(f"  └─────────────────────────────┘ ← Back wall (30mm)")
print(f"\n  Width: {WIDTH}mm")
print(f"  Depth: {WALL_THICK}mm wall + {SHELF_DEPTH}mm shelves = {DEPTH}mm")
print(f"  Height: {BOTTOM_THICK}+100+{MIDDLE_THICK}+100+{TOP_THICK} = {HEIGHT}mm")
print("="*50)
