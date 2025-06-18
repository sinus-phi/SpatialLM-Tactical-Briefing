#!/bin/bash

# SpatialLM Point Cloud Processing Pipeline Runner

# Ensure script fails on error
set -e

# Determine script directory for relative paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate conda environment
echo "Activating spatiallm conda environment..."
# Try different methods to activate conda
if [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    . "$HOME/anaconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    . "$HOME/miniconda3/etc/profile.d/conda.sh"
else
    # Fallback to eval method
    eval "$(conda shell.bash hook)"
fi

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda command not found. Please make sure conda is installed."
    exit 1
fi

# Activate the environment
conda activate spatiallm || { echo "Error: Failed to activate spatiallm environment"; exit 1; }

# Verify Python environment
echo "Using Python: $(which python)"
echo "Python version: $(python --version)"

# Set default parameters
INPUT_FILE="inputPLY/scene0020_00.ply"
OUTPUT_DIR="processed_results"
LANGUAGE="korean"
VISUALIZE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --input)
      INPUT_FILE="$2"
      shift 2
      ;;
    --output_dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --language)
      LANGUAGE="$2"
      shift 2
      ;;
    --visualize)
      VISUALIZE="--visualize"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Ensure the input file exists
if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: Input file '$INPUT_FILE' does not exist."
  exit 1
fi

# Check for required Python modules and files
echo "Checking for required files and modules..."
if [ ! -f "align_pointcloud.py" ]; then
  echo "Warning: align_pointcloud.py not found in current directory"
fi

if [ ! -f "scale_pointcloud.py" ]; then
  echo "Warning: scale_pointcloud.py not found in current directory"
fi

echo "========================================================"
echo "Starting SpatialLM Point Cloud Processing Pipeline"
echo "========================================================"
echo "Input file: $INPUT_FILE"
echo "Output directory: $OUTPUT_DIR"
echo "Language: $LANGUAGE"
echo "Visualization: ${VISUALIZE:+Enabled}"
echo "========================================================"

# Run the Python pipeline script
echo "Launching pipeline script..."
python process_point_cloud_pipeline.py --input "$INPUT_FILE" --output_dir "$OUTPUT_DIR" --language "$LANGUAGE" $VISUALIZE

# Check the exit status
PIPELINE_STATUS=$?
if [ $PIPELINE_STATUS -ne 0 ]; then
  echo "Pipeline script exited with error status: $PIPELINE_STATUS"
  exit $PIPELINE_STATUS
fi

echo "Pipeline script completed successfully."
exit 0 