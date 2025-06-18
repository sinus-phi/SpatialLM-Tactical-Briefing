# SpatialLM - 3D Tactical Operations Briefing System

<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="figures/logo_light.png#gh-light-mode-only" width="60%" alt="SpatialLM" />
  <img src="figures/logo_dark.png#gh-dark-mode-only" width="60%" alt="SpatialLM" />
</div>
<hr style="margin-top: 0; margin-bottom: 8px;">
<div align="center" style="margin-top: 0; padding-top: 0; line-height: 1;">
    <a href="https://manycore-research.github.io/SpatialLM" target="_blank" style="margin: 2px;"><img alt="Project"
    src="https://img.shields.io/badge/🌐%20Website-SpatialLM-ffc107?color=42a5f5&logoColor=white" style="display: inline-block; vertical-align: middle;"/></a>
    <a href="https://github.com/sinus-phi/SpatialLM-Tactical-Briefing" target="_blank" style="margin: 2px;"><img alt="GitHub"
    src="https://img.shields.io/badge/GitHub-SpatialLM-24292e?logo=github&logoColor=white" style="display: inline-block; vertical-align: middle;"/></a>
</div>

## Project Overview

**SpatialLM** is an innovative AI system that analyzes 3D point cloud data to generate **tactical operations briefings**. This system provides an integrated platform where users can visually examine 3D reconstructed point cloud information while interacting with LLM agents to plan and establish tactical operations.

**Important Note**: This system currently supports **Korean language only** for the user interface, briefing generation, and AI interactions. All tactical analyses and reports are generated in Korean.

### Key Features

- **3D Spatial Understanding**: Automatic recognition of 3D structures including walls, doors, windows, and furniture from point cloud data
- **Tactical Briefing Generation**: Detailed tactical analysis and operation planning using ChatGPT API
- **Interactive Q&A**: Real-time tactical question answering capabilities
- **Korean UI**: Complete Korean user interface support (Korean only)
- **Real-time 3D Visualization**: Live 3D point cloud and layout visualization through Rerun
- **Code Generation and Execution**: Automatic Python code generation and execution for visualization and analysis

### System Capabilities

1. **Spatial Structure Analysis**: Automatic detection of architectural elements and objects from 3D point clouds
2. **Tactical Assessment**: Analysis of defensive/offensive positions, movement paths, and line of sight
3. **Risk Factor Identification**: Automatic detection of blind spots, bottlenecks, and danger zones
4. **Equipment Recommendations**: Optimal equipment and weapon suggestions based on spatial characteristics
5. **Team Deployment Planning**: Personnel placement and role assignment proposals
6. **Communication Planning**: Wireless communication efficiency and relay position analysis

## Quick Start

### System Requirements

- Python 3.11
- PyTorch 2.4.1
- CUDA 12.4 or higher
- Ubuntu/Linux (recommended)
- 16GB+ RAM
- NVIDIA GPU (8GB+ VRAM recommended)

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/sinus-phi/SpatialLM-Tactical-Briefing.git
cd SpatialLM-Tactical-Briefing
```

#### 2. Conda Environment Setup
```bash
# Create conda environment with CUDA 12.4 support
conda create -n spatiallm python=3.11
conda activate spatiallm
conda install -y nvidia/label/cuda-12.4.0::cuda-toolkit conda-forge::sparsehash
```

#### 3. Dependencies Installation
```bash
# Install dependencies using Poetry
pip install poetry && poetry config virtualenvs.create false --local
poetry install
poe install-torchsparse  # TorchSparse build (takes time)
```

#### 4. Additional Dependencies (for Briefing System)
```bash
# Install PyQt5 and additional packages
pip install PyQt5 markdown requests configparser
```

### Usage

#### 1. Basic Inference (Point Cloud → Layout)
```bash
# Download example point cloud
huggingface-cli download manycore-research/SpatialLM-Testset pcd/scene0000_00.ply --repo-type dataset --local-dir .

# Run layout inference
python inference.py --point_cloud pcd/scene0000_00.ply --output scene0000_00.txt --model_path manycore-research/SpatialLM-Llama-1B
```

#### 2. 3D Visualization
```bash
# Convert predicted layout to Rerun format
python visualize.py --point_cloud pcd/scene0000_00.ply --layout scene0000_00.txt --save scene0000_00.rrd

# Launch 3D visualization
rerun scene0000_00.rrd
```

#### 3. **Tactical Briefing System Execution (Main Feature)**
```bash
# Launch integrated briefing system (final complete version)
python qt_rerun_briefing.py -i scene0000_00.rrd
```

When executing this command:
- 3D point cloud automatically opens in Rerun viewer
- Korean UI briefing window displays
- Detailed tactical analysis is automatically generated via ChatGPT
- Real-time Q&A enables additional tactical inquiries

## Core Components

### Essential Files

- **`qt_rerun_briefing.py`**: **Main System** - Complete tactical operations system integrating 3D visualization and AI briefing
- **`inference.py`**: 3D layout structure inference from point clouds
- **`visualize.py`**: 3D visualization and Rerun file generation
- **`spatiallm/`**: SpatialLM model and related utilities

### Briefing System Features

1. **Automatic Spatial Analysis**: Automatic identification of tactically important elements from point clouds
2. **ChatGPT Integration**: Detailed tactical briefing generation using OpenAI GPT models
3. **Real-time Interaction**: Real-time tactical advice through question-answer interface
4. **Visualization Code Generation**: Automatic analysis code generation and execution via special keywords ("IIFA")
5. **Korean Language Support**: Complete Korean UI and Korean font support

## Supported Analysis Categories

### Tactical Analysis Areas
- **Spatial Structure Analysis**: Wall positions, entrance/exit dimensions and locations
- **Access Point Analysis**: Entry difficulty and risk assessment for all access points
- **Movement and Visibility Analysis**: Movement paths, viewing angles, and blind spot analysis
- **Object and Obstacle Analysis**: Cover assessment, defense ratings, and ballistic protection evaluation
- **Tactical Position Assessment**: Optimal defensive/offensive positions and control points
- **Environmental Analysis**: Lighting, acoustic, and communication condition evaluation
- **Equipment Recommendations**: Weapon and equipment suggestions optimized for spatial characteristics
- **Operation Planning**: Team composition, role assignment, and timeline proposals

## User Interface

### Korean UI Characteristics
- **Complete Korean Support**: All menus, buttons, and messages displayed in Korean
- **Automatic Korean Font Setup**: Automatic loading of Korean fonts like NanumGothic
- **Intuitive Layout**: Modern UI separated into briefing and Q&A areas
- **Real-time Streaming**: Real-time streaming display of ChatGPT responses
- **Markdown Rendering**: Clean display of structured briefing information

### UI Components
1. **3D Viewer**: Point cloud 3D visualization through Rerun
2. **Briefing Panel**: AI-generated tactical briefing display
3. **Q&A Panel**: Real-time question-answer interface
4. **Settings Panel**: API key configuration and model selection
5. **Toolbar**: Font size, view mode, and other settings

## Configuration and Setup

### ChatGPT API Configuration
1. Obtain OpenAI API key (https://platform.openai.com/api-keys)
2. Enter key in API settings dialog when launching briefing system
3. Supported models: GPT-4o as default. This can be modified in 'qt_rerun_briefing.py'

### Model Configuration
```bash
# Use different SpatialLM model
python qt_rerun_briefing.py -i scene.rrd -m manycore-research/SpatialLM-Qwen-0.5B
```

## Project Structure

```
SpatialLM/
├── qt_rerun_briefing.py        # Main briefing system
├── inference.py                # Point cloud inference
├── visualize.py               # 3D visualization
├── spatiallm/                 # Model library
│   ├── model/                 # AI models
│   ├── layout/                # Layout processing
│   └── pcd/                   # Point cloud processing
├── fonts/                     # Korean fonts
├── figures/                   # Logos and images
├── SpatialLM-Testset/        # Test dataset
└── processed_results/         # Processing results
```

## Testing and Evaluation

### Test Dataset Download
```bash
huggingface-cli download manycore-research/SpatialLM-Testset --repo-type dataset --local-dir SpatialLM-Testset
```

### Performance Evaluation
```bash
# Run inference on entire test set
python inference.py --point_cloud SpatialLM-Testset/pcd --output SpatialLM-Testset/pred --model_path manycore-research/SpatialLM-Llama-1B

# Evaluate performance
python eval.py --metadata SpatialLM-Testset/test.csv --gt_dir SpatialLM-Testset/layout --pred_dir SpatialLM-Testset/pred --label_mapping SpatialLM-Testset/benchmark_categories.tsv
```

## Troubleshooting

### Common Issues

#### GPU Memory Shortage
```bash
# GPU memory optimization settings are already applied
# Memory efficiency settings in inference.py:
# - torch.float16 usage
# - 90% GPU memory limit
# - expandable_segments activation
```

#### PyQt5 Installation Error
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt5

# CentOS/RHEL
sudo yum install python3-qt5
```

#### Korean Font Issues
If fonts don't display properly, NanumGothic fonts from the `fonts/` directory are automatically loaded.

## Performance Benchmarks

Performance on SpatialLM-Testset:

| **Method**       | **SpatialLM-Llama-1B** | **SpatialLM-Qwen-0.5B** |
| ---------------- | ---------------------- | ----------------------- |
| **Floorplan**    | **mean IoU**           |                         |
| wall             | 78.62                  | 74.81                   |
| **Objects**      | **F1 @.25 IoU (3D)**   |                         |
| bed              | 95.24                  | 93.75                   |
| sofa             | 65.50                  | 66.15                   |
| dining table     | 54.26                  | 56.10                   |

## License

- **SpatialLM-Llama-1B**: Licensed under Llama3.2 license
- **SpatialLM-Qwen-0.5B**: Licensed under Apache 2.0 license
- **SceneScript Point Cloud Encoder**: CC-BY-NC-4.0 license
- **TorchSparse**: MIT license

This project is based on the following open source projects:

[Llama3.2](https://github.com/meta-llama) | [Qwen2.5](https://github.com/QwenLM/Qwen2.5) | [Transformers](https://github.com/huggingface/transformers) | [SceneScript](https://github.com/facebookresearch/scenescript) | [TorchSparse](https://github.com/mit-han-lab/torchsparse) | [Rerun](https://rerun.io/)

---

## Advanced Features

### Tactical Analysis Depth

The system provides detailed tactical analysis including:

- **Quantitative Risk Assessment**: Numerical exposure probability and risk scoring for each position
- **Optimal Pathfinding**: Optimal route suggestions considering movement time and risk factors
- **Equipment Efficiency Analysis**: Equipment effectiveness evaluation based on spatial characteristics
- **Communication Quality Prediction**: Wireless communication efficiency analysis based on spatial structure
- **Team Deployment Optimization**: Optimal placement suggestions based on personnel count and roles

### Special Keywords and Commands

The system supports special interaction modes:

- **"IIFA" Keyword**: Activates visualization/code generation mode when included in questions
- **Streaming Responses**: Real-time display of AI-generated responses
- **Code Execution**: Automatic execution of generated Python analysis code
- **Multi-modal Analysis**: Integration of 3D spatial data with AI language processing

### Technical Architecture

#### AI Pipeline
1. **Point Cloud Processing**: TorchSparse-based 3D feature extraction
2. **Layout Generation**: Transformer-based architectural element detection
3. **Tactical Analysis**: GPT-4 powered strategic assessment
4. **Visualization**: Rerun-based real-time 3D rendering

#### Performance Optimizations
- **Memory Management**: Automatic GPU memory optimization
- **Batch Processing**: Efficient handling of large point clouds
- **Streaming Interface**: Real-time response generation
- **Caching System**: Optimized repeated analysis operations

### Security and Privacy

- **Local Processing**: Point cloud analysis performed locally
- **API Security**: Secure OpenAI API key management
- **Data Privacy**: No automatic cloud data transmission
- **Access Control**: Configurable API usage limits

### Future Development

Planned enhancements include:
- **Multi-language Support**: English UI and analysis capabilities
- **Enhanced Models**: Improved tactical analysis algorithms
- **Real-time Collaboration**: Multi-user briefing sessions
- **Mobile Integration**: Tablet and mobile device support
- **Advanced Visualization**: AR/VR integration capabilities

This system represents a unique fusion of 3D spatial AI and tactical intelligence, specifically designed for Korean-speaking users requiring sophisticated tactical analysis capabilities.
