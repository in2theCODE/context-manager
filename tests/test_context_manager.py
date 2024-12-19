import os
import pytest
from context_manager.core import ContextManager

@pytest.fixture
def temp_project(tmpdir):
    """Create a temporary git repository for testing."""
    repo_path = tmpdir.mkdir("test_project")
    os.chdir(repo_path)
    os.system("git init")
    return str(repo_path)

def test_initialize_context(temp_project):
    """Test context initialization."""
    context_manager = ContextManager(temp_project)
    context_manager.initialize_context()
    
    assert os.path.exists(os.path.join(temp_project, 'CONTEXT.md'))
    assert os.path.exists(os.path.join(temp_project, 'USER_CONTEXT.md'))

def test_update_context(temp_project):
    """Test context update with git changes."""
    # Create some dummy files and commits
    os.system("touch test_file.txt")
    os.system("git add test_file.txt")
    os.system("git commit -m 'Add test file'")
    
    context_manager = ContextManager(temp_project)
    context_manager.initialize_context()
    context_manager.update_context()
    
    with open(os.path.join(temp_project, 'CONTEXT.md'), 'r') as f:
        content = f.read()
        assert 'Recent Changes' in content
        assert 'Add test file' in content
