#!/usr/bin/env python3
import os
import subprocess
import argparse
import glob
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Automation script to generate .rrd files for all point cloud files")
    parser.add_argument("--dir", default="FinalResults", help="Directory containing .ply and .txt files")
    parser.add_argument("--radius", type=float, default=0.01, help="Point radius for visualization")
    parser.add_argument("--max_points", type=int, default=1000000, help="Maximum number of points for visualization")
    args = parser.parse_args()
    
    # Get all .ply files in the specified directory
    ply_files = glob.glob(os.path.join(args.dir, "*.ply"))
    print(f"Found {len(ply_files)} .ply files in {args.dir}")
    
    # Process each .ply file
    success_count = 0
    skipped_count = 0
    error_count = 0
    
    for ply_file in ply_files:
        # Construct the corresponding .txt and .rrd file paths
        base_name = os.path.splitext(os.path.basename(ply_file))[0]
        txt_file = os.path.join(args.dir, f"{base_name}.txt")
        rrd_file = os.path.join(args.dir, f"{base_name}.rrd")
        
        # Skip if .rrd file already exists
        if os.path.exists(rrd_file):
            print(f"Skipping {base_name} - .rrd file already exists")
            skipped_count += 1
            continue
        
        # Check if the corresponding .txt file exists
        if not os.path.exists(txt_file):
            print(f"Error: Layout file {txt_file} not found for {ply_file}")
            error_count += 1
            continue
        
        # Construct and run the visualization command with conda environment
        cmd = [
            "bash", "-c", 
            f"conda activate spatiallm && python visualize.py --point_cloud {ply_file} --layout {txt_file} --save {rrd_file} --radius {args.radius} --max_points {args.max_points}"
        ]
        
        print(f"Processing {base_name}...")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Successfully generated {rrd_file}")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"Error processing {base_name}: {e}")
            print(f"Command output: {e.stdout}")
            print(f"Command error: {e.stderr}")
            error_count += 1
    
    # Print summary
    print("\nProcessing Summary:")
    print(f"Total files: {len(ply_files)}")
    print(f"Successfully processed: {success_count}")
    print(f"Skipped (already exist): {skipped_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    main() 