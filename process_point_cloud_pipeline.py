#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Point Cloud Processing Pipeline

This script implements a complete pipeline for processing point cloud data:
1. Align the point cloud using improved Manhattan alignment algorithm
2. Scale the point cloud using scale_pointcloud.py
3. Extract layout from the processed point cloud
4. Create visualization file
5. Display the result using qt_rerun_briefing.py (briefing is generated within the viewer)

Usage:
    python process_point_cloud_pipeline.py --input inputPLY/scene0020_00.ply
"""

import os
import argparse
import subprocess
import time
import tempfile
from pathlib import Path

def run_command(cmd, description=None):
    """Run a terminal command and return the result."""
    if description:
        print(f"\n{description}")
        print("-" * 80)
    
    print(f"Running command: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error executing command: {cmd}")
        print(f"Error output: {result.stderr}")
        raise RuntimeError(f"Command failed with exit code {result.returncode}")
    
    return result.stdout.strip()

def main():
    parser = argparse.ArgumentParser(description="Point Cloud Processing Pipeline")
    parser.add_argument("--input", required=True, help="Path to input point cloud file (.ply)")
    parser.add_argument("--output_dir", default="processed_results", help="Directory to save output files")
    parser.add_argument("--model", default="manycore-research/SpatialLM-Llama-1B", 
                        help="Path to the SpatialLM model for layout extraction")
    parser.add_argument("--language", default="korean", choices=["english", "korean"],
                        help="Language for the briefing (default: korean)")
    parser.add_argument("--visualize", action="store_true", help="Show visualization during processing")
    parser.add_argument("--min_points", type=int, default=500, 
                        help="Minimum points required for plane detection (default: 500)")
    parser.add_argument("--distance_threshold", type=float, default=0.03, 
                        help="RANSAC distance threshold for plane detection (default: 0.03)")
    parser.add_argument("--target_height", type=float, default=2.5, 
                        help="Target height in meters (default: 2.5, typical room height)")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Create subdirectories for intermediate results
    align_dir = os.path.join(args.output_dir, "aligned")
    scaled_dir = os.path.join(args.output_dir, "scaled")
    os.makedirs(align_dir, exist_ok=True)
    os.makedirs(scaled_dir, exist_ok=True)
    
    # Get input file information
    input_file = args.input
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return 1
        
    input_filename = os.path.basename(input_file)
    input_basename = os.path.splitext(input_filename)[0]
    
    # Setup output paths
    aligned_pcd_path = os.path.join(align_dir, f"{input_basename}_aligned.ply")
    scaled_pcd_path = os.path.join(scaled_dir, f"{input_basename}_scaled.ply")
    layout_path = os.path.join(args.output_dir, f"{input_basename}.txt")
    rerun_file = os.path.join(args.output_dir, f"{input_basename}.rrd")
    
    # Record start time
    start_time = time.time()
    
    try:
        # Step 1: Align the point cloud using improved Manhattan alignment
        print("\n=== STEP 1: ALIGNING POINT CLOUD USING MANHATTAN ALIGNMENT ===")
        visualize_flag = "--visualize" if args.visualize else ""
        cmd = f"python align_pointcloud.py --input {input_file} --output {aligned_pcd_path} --output_dir {align_dir} {visualize_flag} --min_points {args.min_points} --distance_threshold {args.distance_threshold}"
        run_command(cmd)
        print(f"Aligned point cloud saved to: {aligned_pcd_path}")
        
        # Step 2: Scale the point cloud to standard height
        print("\n=== STEP 2: SCALING POINT CLOUD TO STANDARD HEIGHT ===")
        cmd = f"python scale_pointcloud.py --input {aligned_pcd_path} --output {scaled_pcd_path} --output_dir {scaled_dir} --height {args.target_height} {visualize_flag}"
        run_command(cmd)
        print(f"Scaled point cloud saved to: {scaled_pcd_path}")
        
        # Step 3: Extract layout from the scaled point cloud
        print("\n=== STEP 3: EXTRACTING LAYOUT ===")
        # Check if code_template.txt exists
        if not os.path.exists("code_template.txt"):
            print("Warning: code_template.txt not found in current directory.")
            # Try to find it in the repository
            possible_paths = [".", "spatiallm", "../"]
            found = False
            for path in possible_paths:
                template_path = os.path.join(path, "code_template.txt")
                if os.path.exists(template_path):
                    print(f"Found code template at: {template_path}")
                    code_template_path = template_path
                    found = True
                    break
            if not found:
                code_template_path = "code_template.txt"
                print(f"Using default path: {code_template_path}")
        else:
            code_template_path = "code_template.txt"
            
        cmd = f"python inference.py --point_cloud {scaled_pcd_path} --output {layout_path} --model {args.model} --code_template_file {code_template_path}"
        run_command(cmd)
        print(f"Layout extracted and saved to: {layout_path}")
        
        # Step 4: Create visualization file for Qt viewer (skip briefing generation)
        print("\n=== STEP 4: CREATING VISUALIZATION ===")
        # Check if visualize.py supports --save parameter
        try:
            visualize_cmd = f"python visualize.py -p {scaled_pcd_path} -l {layout_path} --save {rerun_file}"
            run_command(visualize_cmd)
            print(f"Visualization saved to: {rerun_file}")
        except RuntimeError:
            print("Warning: Could not create visualization with --save parameter. Trying alternative method...")
            try:
                # Try alternate command format
                visualize_cmd = f"python visualize.py -p {scaled_pcd_path} -l {layout_path} -o {rerun_file}"
                run_command(visualize_cmd)
                print(f"Visualization saved to: {rerun_file}")
            except RuntimeError:
                print("Warning: Could not create visualization file. Creating empty file.")
                # Create empty file to ensure next step works
                Path(rerun_file).touch()
        
        # Step 5: Run the Qt briefing viewer (briefing will be generated inside the viewer)
        print("\n=== STEP 5: LAUNCHING QT BRIEFING VIEWER ===")
        cmd = f"python qt_rerun_briefing.py -r {rerun_file} -l {layout_path} -m {args.model} -g {args.language}"
        print(f"Starting Qt briefing viewer...\n{cmd}")
        
        # Use subprocess.run instead of Popen to wait for the viewer to finish
        viewer_process = subprocess.Popen(cmd, shell=True)
        print("QT viewer launched. Please wait for it to complete...")
        
        # Report time taken
        elapsed_time = time.time() - start_time
        print(f"\n=== PIPELINE COMPLETED SUCCESSFULLY ===")
        print(f"Total processing time: {elapsed_time:.2f} seconds")
        print(f"Results saved to: {args.output_dir}")
        print(f"  - Aligned point cloud: {aligned_pcd_path}")
        print(f"  - Scaled point cloud: {scaled_pcd_path}")
        print(f"  - Layout file: {layout_path}")
        print(f"  - Visualization file: {rerun_file}")
        
        # Wait a moment before exiting to ensure the viewer has time to start
        print("Waiting for Qt viewer to initialize...")
        time.sleep(3)
        
    except Exception as e:
        print(f"\n=== PIPELINE FAILED ===")
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 