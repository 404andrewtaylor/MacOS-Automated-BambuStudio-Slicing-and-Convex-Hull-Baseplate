#!/usr/bin/env python3
"""
Complete pipeline: Extract convex hull from gcode and create extruded STL.
"""

import sys
import os
import tempfile
import numpy as np
from stl import mesh
from extract_and_analyze import extract_gcode_from_3mf_file, parse_gcode_first_layer, compute_convex_hull
from extrude_hull_to_stl import create_stl_from_hull


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 hull_to_stl.py <gcode_3mf_file> <output_stl_file> <original_stl_file>")
        print("Example: python3 hull_to_stl.py model.gcode.3mf extruded_hull.stl original_model.stl")
        sys.exit(1)
    
    gcode_3mf_path = sys.argv[1]
    output_stl_path = sys.argv[2]
    original_stl_path = sys.argv[3]
    
    if not os.path.exists(gcode_3mf_path):
        print(f"❌ Error: File not found: {gcode_3mf_path}")
        sys.exit(1)
    
    if not os.path.exists(original_stl_path):
        print(f"❌ Error: Original STL file not found: {original_stl_path}")
        sys.exit(1)
    
    try:
        print(f"🚀 Starting hull extraction and STL creation...")
        print(f"📁 Input: {gcode_3mf_path}")
        print(f"📁 Output: {output_stl_path}")
        
        # Step 1: Extract gcode
        print("\n📦 Step 1: Extracting gcode...")
        gcode_content = extract_gcode_from_3mf_file(gcode_3mf_path)
        
        # Step 2: Parse first layer
        print("🔍 Step 2: Analyzing first layer...")
        first_layer_points = parse_gcode_first_layer(gcode_content)
        
        # Step 3: Compute convex hull
        print("🔺 Step 3: Computing convex hull...")
        hull, hull_points = compute_convex_hull(first_layer_points)
        
        # Use hull points as-is (no offset calculation needed)
        aligned_hull_points = hull_points
        
        # Step 4: Create STL
        print("📐 Step 4: Creating extruded STL...")
        create_stl_from_hull(aligned_hull_points, height=1.0, output_path=output_stl_path)
        
        print(f"\n✅ Successfully created extruded STL: {output_stl_path}")
        print(f"📊 Hull vertices: {len(hull_points)}")
        print(f"📊 Extrusion height: 1.0mm")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
