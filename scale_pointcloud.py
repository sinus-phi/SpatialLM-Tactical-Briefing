import numpy as np
import open3d as o3d
import argparse
from pathlib import Path
import os

def load_point_cloud(file_path):
    print(f"Loading point cloud from {file_path}")
    point_cloud = o3d.io.read_point_cloud(file_path)
    return point_cloud

def get_points_and_colors(point_cloud):
    points = np.asarray(point_cloud.points)
    if point_cloud.has_colors():
        colors = np.asarray(point_cloud.colors) * 255.0
    else:
        colors = np.ones_like(points) * 255  # Default white color
    return points, colors.astype(np.uint8)

def scale_point_cloud(point_cloud, target_height=2.5):
    """
    Scale the point cloud to have a specific height (in meters)
    For indoor scenes, walls typically have a height around 2.5 meters
    """
    points = np.asarray(point_cloud.points)
    has_colors = point_cloud.has_colors()
    if has_colors:
        colors = np.asarray(point_cloud.colors).copy()
    
    # Find the current height (along z-axis)
    min_z = np.min(points[:, 2])
    max_z = np.max(points[:, 2])
    current_height = max_z - min_z
    
    print(f"Current point cloud height: {current_height} units")
    print(f"Target height: {target_height} meters")
    
    # Calculate the scaling factor
    scale_factor = target_height / current_height
    print(f"Scaling factor: {scale_factor}")
    
    # Scale the points
    scaled_points = points * scale_factor
    
    # Create a new point cloud with the scaled points
    scaled_cloud = o3d.geometry.PointCloud()
    scaled_cloud.points = o3d.utility.Vector3dVector(scaled_points)
    
    # Copy the original colors
    if has_colors:
        scaled_cloud.colors = o3d.utility.Vector3dVector(colors)
    
    return scaled_cloud, scale_factor, current_height

def main():
    parser = argparse.ArgumentParser(description="Scale a point cloud to have a specific height")
    parser.add_argument("--input", required=True, help="Path to input point cloud file (.ply)")
    parser.add_argument("--output", help="Path to output scaled point cloud file (.ply)")
    parser.add_argument("--output_dir", default="processed_pointclouds", help="Directory to save output files")
    parser.add_argument("--height", type=float, default=2.5, 
                        help="Target height in meters (default: 2.5, typical room height)")
    parser.add_argument("--visualize", action="store_true", help="Visualize before and after scaling")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created output directory: {args.output_dir}")
    
    # Load the point cloud
    point_cloud = load_point_cloud(args.input)
    
    # Get input filename without path
    input_filename = os.path.basename(args.input)
    input_basename = os.path.splitext(input_filename)[0]
    
    # Scale the point cloud
    scaled_cloud, scale_factor, current_height = scale_point_cloud(point_cloud, args.height)
    
    # Visualize if requested
    if args.visualize:
        # Create coordinate frames for visualization
        frame_size = 1.0  # Size of the coordinate frame
        original_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=frame_size)
        scaled_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=frame_size)
        
        # Create copies for visualization (to avoid modifying the original data)
        original_viz = o3d.geometry.PointCloud()
        original_viz.points = o3d.utility.Vector3dVector(np.asarray(point_cloud.points))
        if point_cloud.has_colors():
            original_viz.colors = point_cloud.colors
        original_colored = original_viz.paint_uniform_color([1, 0.706, 0])  # Orange
        
        scaled_viz = o3d.geometry.PointCloud()
        scaled_viz.points = o3d.utility.Vector3dVector(np.asarray(scaled_cloud.points))
        scaled_colored = scaled_viz.paint_uniform_color([0, 0.651, 0.929])  # Blue
        
        # Visualize original point cloud
        print("Visualizing original point cloud (orange) with coordinate frame")
        o3d.visualization.draw_geometries([original_colored, original_frame])
        
        # Visualize scaled point cloud
        print("Visualizing scaled point cloud (blue) with coordinate frame")
        o3d.visualization.draw_geometries([scaled_colored, scaled_frame])
        
        # Now visualize with original colors
        if point_cloud.has_colors():
            print("Visualizing original point cloud with original colors")
            o3d.visualization.draw_geometries([point_cloud, original_frame])
            
            print("Visualizing scaled point cloud with original colors")
            o3d.visualization.draw_geometries([scaled_cloud, scaled_frame])
    
    # Set default output path if not provided
    if args.output:
        if os.path.dirname(args.output):
            # If a full path is provided, use it as is
            output_path = args.output
        else:
            # If only a filename is provided, put it in the output directory
            output_path = os.path.join(args.output_dir, args.output)
    else:
        # If no output path is provided, create one based on the input filename
        output_path = os.path.join(args.output_dir, f"{input_basename}_scaled.ply")
    
    # Save the scaled point cloud
    print(f"Saving scaled point cloud to {output_path}")
    o3d.io.write_point_cloud(output_path, scaled_cloud)
    
    # Save scaling information to a text file
    scale_info_path = os.path.join(args.output_dir, f"{input_basename}_scale_info.txt")
    with open(scale_info_path, 'w') as f:
        f.write(f"Original height: {current_height}\n")
        f.write(f"Target height: {args.height}\n")
        f.write(f"Scaling factor: {scale_factor}\n")
    print(f"Scaling information saved to {scale_info_path}")
    
    print(f"Scaling completed with factor {scale_factor}")
    print("Done!")

if __name__ == "__main__":
    main() 