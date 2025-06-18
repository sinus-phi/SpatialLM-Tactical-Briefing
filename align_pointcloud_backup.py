import numpy as np
import open3d as o3d
import argparse
from pathlib import Path
import os
from sklearn.decomposition import PCA

def load_point_cloud(file_path):
    print(f"Loading point cloud from {file_path}")
    point_cloud = o3d.io.read_point_cloud(file_path)
    return point_cloud

def align_to_manhattan(point_cloud, visualize=True):
    """
    Perform a simple alignment of the point cloud to Manhattan world axes:
    - Use PCA to find principal axes
    - Align the principal axes with world coordinate system
    - Make Z-axis point upward
    
    Parameters:
    -----------
    point_cloud: o3d.geometry.PointCloud
        Input point cloud to align
    visualize: bool, default=True
        Whether to visualize the result
    """
    points = np.asarray(point_cloud.points)
    has_colors = point_cloud.has_colors()
    if has_colors:
        original_colors = np.asarray(point_cloud.colors).copy()
    
    # Simple outlier removal
    cl, _ = point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    points = np.asarray(cl.points)
    
    # Calculate centroid
    centroid = np.mean(points, axis=0)
    print(f"Centroid: {centroid}")
    
    # Use PCA to find principal axes
    pca = PCA(n_components=3)
    pca.fit(points)
    principal_axes = pca.components_
    variances = pca.explained_variance_
    
    print("PCA Variances:", variances)
    print("Principal Axes:")
    print(principal_axes)
    
    # For indoor scenes, typically the axis with smallest variance is vertical (Z)
    up_idx = np.argmin(variances)
    z_axis = principal_axes[up_idx]
    
    # Ensure Z-axis points upward (positive Z)
    if z_axis[2] < 0:
        z_axis = -z_axis
    
    # Find other axes
    other_indices = [i for i in range(3) if i != up_idx]
    x_idx = other_indices[0]
    y_idx = other_indices[1]
    x_axis = principal_axes[x_idx]
    y_axis = principal_axes[y_idx]
    
    # Ensure orthogonality to z-axis using Gram-Schmidt
    x_axis = x_axis - np.dot(x_axis, z_axis) * z_axis
    x_axis = x_axis / np.linalg.norm(x_axis)
    
    # Compute y-axis using cross product to ensure right-handed system
    y_axis = np.cross(z_axis, x_axis)
    y_axis = y_axis / np.linalg.norm(y_axis)
    
    # Create rotation matrix
    R = np.vstack([x_axis, y_axis, z_axis])
    
    # Ensure it's a valid rotation (orthogonal, determinant = 1)
    u, _, vh = np.linalg.svd(R)
    R = u @ vh
    if np.linalg.det(R) < 0:  # Ensure right-handed
        R[1] = -R[1]  # Flip y-axis
    
    # Apply transformation
    aligned_points = (points - centroid) @ R.T + centroid
    
    # Create result point cloud
    aligned_result = o3d.geometry.PointCloud()
    aligned_result.points = o3d.utility.Vector3dVector(aligned_points)
    
    # Copy colors if present
    if has_colors:
        aligned_result.colors = o3d.utility.Vector3dVector(original_colors)
    
    # Visualize if requested
    if visualize:
        # Create coordinate frames
        original_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
        aligned_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
        
        # Create colored point clouds for visualization
        original_viz = o3d.geometry.PointCloud()
        original_viz.points = o3d.utility.Vector3dVector(points)
        if has_colors:
            original_viz.colors = o3d.utility.Vector3dVector(original_colors)
        else:
            original_viz = original_viz.paint_uniform_color([1, 0.706, 0])  # Orange
        
        aligned_viz = o3d.geometry.PointCloud()
        aligned_viz.points = o3d.utility.Vector3dVector(aligned_points)
        if has_colors:
            aligned_viz.colors = o3d.utility.Vector3dVector(original_colors)
        else:
            aligned_viz = aligned_viz.paint_uniform_color([0, 0.651, 0.929])  # Blue
        
        # Visualize original point cloud
        print("Visualizing original point cloud with coordinate frame")
        o3d.visualization.draw_geometries([original_viz, original_frame])
        
        # Visualize aligned point cloud
        print("Visualizing aligned point cloud with coordinate frame")
        o3d.visualization.draw_geometries([aligned_viz, aligned_frame])
    
    return aligned_result, R, centroid

def save_transformation(R, centroid, output_file):
    """Save the transformation parameters to a file"""
    # Ensure the directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(output_file, 'w') as f:
        f.write("# Rotation matrix (R.T, for transforming points: aligned = (original - centroid) @ R.T + centroid)\n")
        R_save = R.T  # Save the transpose which is used for transforming points
        for row in R_save:
            f.write(" ".join([f"{x:.8f}" for x in row]) + "\n")
        f.write("# Centroid\n")
        f.write(" ".join([f"{x:.8f}" for x in centroid]) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Simple alignment of a point cloud to Manhattan world axes")
    parser.add_argument("--input", required=True, help="Path to input point cloud file (.ply)")
    parser.add_argument("--output", help="Path to output aligned point cloud file (.ply)")
    parser.add_argument("--output_dir", default="processed_pointclouds", help="Directory to save output files")
    parser.add_argument("--visualize", action="store_true", help="Visualize before and after alignment")
    parser.add_argument("--transform_file", help="Path to save transformation parameters")
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print(f"SIMPLE MANHATTAN ALIGNMENT PROCESSING")
    print("="*50)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created output directory: {args.output_dir}")
    
    # Load the point cloud
    point_cloud = load_point_cloud(args.input)
    points = np.asarray(point_cloud.points)
    print(f"Loaded point cloud with {len(points)} points")
    
    # Get input filename without path
    input_filename = os.path.basename(args.input)
    input_basename = os.path.splitext(input_filename)[0]
    
    # Align the point cloud
    print("\nStarting simple alignment...")
    aligned_cloud, R, centroid = align_to_manhattan(
        point_cloud, 
        visualize=args.visualize
    )
    
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
        output_path = os.path.join(args.output_dir, f"{input_basename}_aligned.ply")
    
    # Save the aligned point cloud
    print(f"\nSaving aligned point cloud to {output_path}")
    o3d.io.write_point_cloud(output_path, aligned_cloud)
    
    # Set default transform file path if not provided
    if args.transform_file:
        if os.path.dirname(args.transform_file):
            # If a full path is provided, use it as is
            transform_path = args.transform_file
        else:
            # If only a filename is provided, put it in the output directory
            transform_path = os.path.join(args.output_dir, args.transform_file)
    else:
        # If no transform file path is provided, create one based on the input filename
        transform_path = os.path.join(args.output_dir, f"{input_basename}_alignment_transform.txt")
    
    # Save the transformation
    save_transformation(R, centroid, transform_path)
    print(f"Transformation matrix saved to {transform_path}")
    
    # Print transformation details
    print("\nRotation Matrix (rows are the principal axes):")
    for row in R:
        print(f"  {row}")
    print(f"Centroid: {centroid}")
    
    print("\nAlignment complete!")

if __name__ == "__main__":
    main() 