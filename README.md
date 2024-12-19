# Context Manager: Intelligent Project Development Assistant

## 🚀 Project Overview

Context Manager is an AI-powered development assistant designed to provide comprehensive project tracking, dependency management, and strategic insights.

## 🖥️ Environment Setup

### Prerequisites
- Conda (Recommended)
- Python 3.10+

### Conda Environment Setup
```bash
# Create Conda environment
conda create -n context-manager python=3.12
conda activate context-manager

# Install dependencies
conda install pytorch torchvision torchaudio -c pytorch
pip install -r requirements.txt
```

### 🍎 Apple Silicon (M1/M2/M3) Special Instructions

#### Important Note for Mac Users with Apple Silicon Chips
Due to complex dependencies, especially for machine learning libraries, we **strongly recommend using Conda** for environment management.

#### Why Conda for Apple Silicon?
- Provides pre-compiled wheels for ARM64 architecture
- Handles complex library dependencies
- Ensures compatibility with machine learning libraries

## 📦 Packaging and Distribution

### Using Poetry (Optional)
Poetry is used only for packaging and distribution, not for local development.

```bash
# Install Poetry (if not already installed)
pip install poetry

# Build package
poetry build

# Install optional ML dependencies
poetry install -E ml
```

## 🛠️ Development

### Running the Project
```bash
# Activate Conda environment
conda activate context-manager

# Run the CLI
python -m context_manager
```

## 📦 Dependencies
- Core dependencies managed via Conda
- Python 3.10+ recommended
- Machine learning libraries require special attention on Apple Silicon

## 🌟 Key Features

- **Intelligent Context Tracking**
- **Dependency Management**
- **Code Analysis**
- **AI-Powered Insights**
- **GitHub Integration**

## 📂 Project Structure

```
context-manager/
│
├── src/context_manager/
│   ├── components/
│   │   ├── dependency_management/
│   │   ├── code_analysis/
│   │   ├── ai_insights/
│   │   └── project_tracking/
│   │
│   ├── integrations/
│   │   └── github_integration.py
│   │
│   ├── cli.py
│   └── core.py
│
└── .context/
    ├── GLOBAL_CONTEXT.yaml
    └── logs/
```

## 🔧 Components

### Dependency Management
- Track project dependencies
- Check for updates
- Manage package versions

### Code Analysis
- Analyze project structure
- Generate improvement suggestions
- Create boilerplate code

### AI Insights
- Strategic recommendations
- Development trajectory analysis
- Predictive insights

### Project Tracking
- Comprehensive context management
- Milestone tracking
- Development phase monitoring

## 🌐 Integrations

- GitHub Repository Tracking
- AI-Powered Insight Generation

## 🚀 Quick Start

```bash
# Install dependencies
pip install -e .

# Initialize project context
context-manager context init

# Check project status
context-manager context report
```

## 🤝 Contributing
- Use Conda for environment management
- Use Poetry only for packaging
- Ensure compatibility with Python 3.10+

## 🚨 Important Notes
- Machine learning dependencies are optional
- Conda is the recommended environment management tool
- Poetry is used only for packaging

## 📄 License

[Your License Here]
