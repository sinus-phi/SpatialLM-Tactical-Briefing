#!/bin/bash

# Check if input arguments are provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input.ply> [output_name] [model_path] [language]"
    echo ""
    echo "Arguments:"
    echo "  input.ply        - Path to the input point cloud file (.ply)"
    echo "  output_name      - (Optional) Base name for the output file without extension (default: derived from PLY file)"
    echo "  model_path       - (Optional) Path to the SpatialLM model (default: manycore-research/SpatialLM-Llama-1B)"
    echo "  language         - (Optional) Language for the output (english/korean, default: korean)"
    echo ""
    echo "Example: $0 scene0002_00.ply livingroom"
    exit 1
fi

# Set default values
INPUT_PLY=$1
PLY_BASENAME=$(basename "$INPUT_PLY" .ply)
OUTPUT_NAME=${2:-$PLY_BASENAME}
MODEL_PATH=${3:-"manycore-research/SpatialLM-Llama-1B"}
LANGUAGE=${4:-"korean"}

# Create briefings directory if it doesn't exist
BRIEFINGS_DIR="briefings"
mkdir -p "$BRIEFINGS_DIR"

# Create temp directory for layouts if it doesn't exist
LAYOUTS_DIR="layouts"
mkdir -p "$LAYOUTS_DIR"

# Generate layout filename and output briefing filename
LAYOUT_FILE="$LAYOUTS_DIR/${PLY_BASENAME}.txt"
DATE_STAMP=$(date +"%Y%m%d")
OUTPUT_BRIEFING="$BRIEFINGS_DIR/${OUTPUT_NAME}_${LANGUAGE}_${DATE_STAMP}.txt"

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate spatiallm

echo "====================== COMPLETE TACTICAL BRIEFING PIPELINE ======================"
echo "Input PLY file: $INPUT_PLY"
echo "Layout output: $LAYOUT_FILE"
echo "Final briefing: $OUTPUT_BRIEFING"
echo "Model path: $MODEL_PATH"
echo "Language: $LANGUAGE"
echo "=============================================================================="

# Step 1: Run inference.py to generate layout from PLY
echo ""
echo "STEP 1: Generating layout from point cloud..."
echo "-----------------------------------------------------------------------------"
python inference.py -p "$INPUT_PLY" -o "$LAYOUT_FILE" -m "$MODEL_PATH"

# Check if layout generation was successful
if [ ! -f "$LAYOUT_FILE" ]; then
    echo "Error: Failed to generate layout file from point cloud."
    exit 1
fi

echo ""
echo "Layout generation complete! Layout saved to: $LAYOUT_FILE"
echo ""

# Step 2: Generate tactical briefing from layout
echo "STEP 2: Generating tactical briefing from layout..."
echo "-----------------------------------------------------------------------------"
python layout_based_briefing.py -l "$LAYOUT_FILE" -o "$OUTPUT_BRIEFING" -m "$MODEL_PATH" -d high -s tactical -g "$LANGUAGE"

# Check if briefing generation was successful
if [ ! -f "$OUTPUT_BRIEFING" ]; then
    echo "Error: Failed to generate tactical briefing."
    exit 1
fi

echo ""
echo "====================== PIPELINE COMPLETE ======================"
echo "Tactical briefing successfully generated at: $OUTPUT_BRIEFING"
echo "Language: $LANGUAGE"
echo "To view the briefing: cat $OUTPUT_BRIEFING"
echo "=============================================================="

# Print the first few lines of the briefing
echo ""
echo "Briefing Preview:"
echo "----------------------------------------------------------------------"
head -n 20 "$OUTPUT_BRIEFING"
echo "----------------------------------------------------------------------"
echo "..."
echo "View the complete briefing with: cat $OUTPUT_BRIEFING" 