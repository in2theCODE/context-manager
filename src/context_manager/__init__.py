# Version information
__version__ = "0.2.0"

# Import key components for easy access
from .components.project_tracking.context_system import ProjectContextManager
from .components.dependency_management.dependency_tracker import DependencyTracker
from .components.code_analysis.code_generator import CodeGenerator
from .components.ai_insights.insight_generator import AIInsightGenerator
from .utils.onboarding import start_project_onboarding
from .cli import main

# Expose key classes and functions
__all__ = [
    'ProjectContextManager',
    'DependencyTracker', 
    'CodeGenerator',
    'AIInsightGenerator',
    'start_project_onboarding',
    'main',
    '__version__'
]

# Add project root to Python path to help with imports
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
