import os
import pytest
import yaml
from context_manager.components.project_tracking.project_context_manager import ProjectContextManager

def test_project_context_initialization(tmp_path):
    """
    Test that the ProjectContextManager initializes correctly.
    """
    context_manager = ProjectContextManager(str(tmp_path))
    
    # Check context directory was created
    assert os.path.exists(os.path.join(str(tmp_path), '.context'))
    
    # Check context file was created
    context_file = os.path.join(str(tmp_path), '.context', 'GLOBAL_CONTEXT.yaml')
    assert os.path.exists(context_file)
    
    # Verify context file contents
    with open(context_file, 'r') as f:
        context = yaml.safe_load(f)
    
    assert 'project' in context
    assert 'development' in context
    assert context['project']['name'] == tmp_path.name

def test_get_current_context(tmp_path):
    """
    Test retrieving the current project context.
    """
    context_manager = ProjectContextManager(str(tmp_path))
    context = context_manager.get_current_context()
    
    assert isinstance(context, dict)
    assert 'project' in context
    assert 'development' in context
