#!/bin/bash

# Default parameters
DIR="FinalResults"
RADIUS=0.01
MAX_POINTS=1000000

# Print usage information
function print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Generate .rrd files for all point cloud files in a directory"
    echo ""
    echo "Options:"
    echo "  --dir DIR           Directory containing .ply and .txt files (default: FinalResults)"
    echo "  --radius RADIUS     Point radius for visualization (default: 0.01)"
    echo "  --max_points NUM    Maximum number of points for visualization (default: 1000000)"
    echo "  --help              Display this help message and exit"
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dir)
            DIR="$2"
            shift 2
            ;;
        --radius)
            RADIUS="$2"
            shift 2
            ;;
        --max_points)
            MAX_POINTS="$2"
            shift 2
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate spatiallm

# Get all .ply files in the directory
PLY_FILES=$(find "$DIR" -name "*.ply")
FILE_COUNT=$(echo "$PLY_FILES" | wc -l)
echo "Found $FILE_COUNT .ply files in $DIR"

# Initialize counters
SUCCESS_COUNT=0
SKIPPED_COUNT=0
ERROR_COUNT=0

# Process each file
for PLY_FILE in $PLY_FILES; do
    # Get base filename without extension
    BASE_NAME=$(basename "$PLY_FILE" .ply)
    TXT_FILE="$DIR/$BASE_NAME.txt"
    RRD_FILE="$DIR/$BASE_NAME.rrd"
    
    # Skip if .rrd file already exists
    if [ -f "$RRD_FILE" ]; then
        echo "Skipping $BASE_NAME - .rrd file already exists"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi
    
    # Check if the corresponding .txt file exists
    if [ ! -f "$TXT_FILE" ]; then
        echo "Error: Layout file $TXT_FILE not found for $PLY_FILE"
        ERROR_COUNT=$((ERROR_COUNT + 1))
        continue
    fi
    
    # Run the visualization command
    echo "Processing $BASE_NAME..."
    python visualize.py --point_cloud "$PLY_FILE" --layout "$TXT_FILE" --save "$RRD_FILE" --radius "$RADIUS" --max_points "$MAX_POINTS"
    
    # Check if command was successful
    if [ $? -eq 0 ]; then
        echo "Successfully generated $RRD_FILE"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "Error processing $BASE_NAME"
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
done

# Print summary
echo ""
echo "Processing Summary:"
echo "Total files: $FILE_COUNT"
echo "Successfully processed: $SUCCESS_COUNT"
echo "Skipped (already exist): $SKIPPED_COUNT"
echo "Errors: $ERROR_COUNT" 