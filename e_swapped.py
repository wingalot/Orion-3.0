#!/usr/bin/env python3
"""
E-Shape Tower - Swapped dimensions
Dimensions: 160mm (W) x 340mm (D) x 360mm (H)
E vertical line: 30mm thick
Shelves extend: 130mm from wall
"""

import trimesh

# NEW Dimensions (swapped)
WIDTH = 160       # Width (left-to-right): 160mm
DEPTH = 340       # Depth (front-to-back): 340mm
HEIGHT = 360      # Total height

# E-shape dimensions
VERTICAL_THICKNESS = 30  # 3cm - the vertical line of E
SHELF_EXTEND = 130       # 13cm - how far shelves extend (160-30=130)

# Shelf thicknesses (same as before)
BOTTOM_THICK = 80   # 8cm
MIDDLE_THICK = 60   # 6cm
TOP_THICK = 20      # 2cm

# Positions (z from bottom)
BOTTOM_Z = 0
MIDDLE_Z = BOTTOM_THICK + 100  # 80 + 100 gap = 180? Wait...
# Actually: 0 + 80 + 100 gap = 180 for middle start
MIDDLE_Z = 180
TOP_Z = MIDDLE_Z + MIDDLE_THICK + 100  # 180 + 60 + 100 = 340

def create_e_swapped():
    """Create E shape with swapped W/D:
    - Vertical wall on BACK (y=0), 30mm thick, extends forward
    - 3 shelves extend toward FRONT (increasing Y)
    """
    meshes = []
    
    # 1. BACK VERTICAL WALL (the | of E)
    # Full height, 30mm thick, full width
    back_wall = trimesh.creation.box(extents=[WIDTH, VERTICAL_THICKNESS, HEIGHT])
    back_wall.apply_translation([WIDTH/2, VERTICAL_THICKNESS/2, HEIGHT/2])
    meshes.append(back_wall)
    
    # 2. BOTTOM SHELF (extends from back wall toward front)
    # 130mm long (from y=30 to y=160), 80mm thick
    bottom = trimesh.creation.box(extents=[WIDTH, SHELF_EXTEND, BOTTOM_THICK])
    bottom.apply_translation([WIDTH/2, VERTICAL_THICKNESS + SHELF_EXTEND/2, BOTTOM_THICK/2])
    meshes.append(bottom)
    
    # 3. MIDDLE SHELF (at z=180)
    middle = trimesh.creation.box(extents=[WIDTH, SHELF_EXTEND, MIDDLE_THICK])
    middle.apply_translation([WIDTH/2, VERTICAL_THICKNESS + SHELF_EXTEND/2, MIDDLE_Z + MIDDLE_THICK/2])
    meshes.append(middle)
    
    # 4. TOP SHELF (at z=340)
    top = trimesh.creation.box(extents=[WIDTH, SHELF_EXTEND, TOP_THICK])
    top.apply_translation([WIDTH/2, VERTICAL_THICKNESS + SHELF_EXTEND/2, TOP_Z + TOP_THICK/2])
    meshes.append(top)
    
    return trimesh.util.concatenate(meshes)

# Generate
print("🌱 Generating E-tower (swapped dimensions)...")
model = create_e_swapped()

print(f"✅ Is manifold: {model.is_watertight}")
print(f"📊 Volume: {model.volume / 1000:.1f} cm³")

# Export
output = "/home/oreo/.openclaw/workspace/e_tower_swapped.stl"
model.export(output)
print(f"💾 Exported: {output}")

print("\n" + "="*45)
print("E-TOWER SPECIFICATIONS:")
print("="*45)
print(f"Overall: {WIDTH}mm(W) x {DEPTH}mm(D) x {HEIGHT}mm(H)")
print(f"\nE-shape:")
print(f"  Vertical wall (back): {VERTICAL_THICKNESS}mm thick")
print(f"  Shelf extension: {SHELF_EXTEND}mm toward front")
print(f"\nShelves (from bottom):")
print(f"  Bottom: {BOTTOM_THICK}mm thick @ z={BOTTOM_Z}-{BOTTOM_THICK}mm")
print(f"  Middle: {MIDDLE_THICK}mm thick @ z={MIDDLE_Z}-{MIDDLE_Z+MIDDLE_THICK}mm")
print(f"  Top: {TOP_THICK}mm thick @ z={TOP_Z}-{TOP_Z+TOP_THICK}mm")
print(f"\nGaps between: 100mm")
print("="*45)
print("\nSide view (from left):")
print("     160mm")
print("     ┌───────┐")
print(f"     │       ││  ← Top ({TOP_THICK}mm)")
print("     │       ││")
print("     │       ║│  ← 100mm gap")
print("     │       ││")
print(f"     │       ││  ← Middle ({MIDDLE_THICK}mm)")
print("     │       ││")
print("     │       ║│  ← 100mm gap")
print("     │       ││")
print(f"     │       ││  ← Bottom ({BOTTOM_THICK}mm)")
print("     └───────┘│")
print("     └────────┘ ← Back wall (30mm)")
print("      340mm →")
