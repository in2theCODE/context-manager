import os
import ast
from typing import Dict, List, Any

class CodeGenerator:
    """
    Provides code generation, analysis, and boilerplate creation capabilities.
    """
    def __init__(self, project_path: str):
        self.project_path = project_path

    def generate_boilerplate(self, template_type: str) -> str:
        """
        Generate boilerplate code for different project types.
        
        :param template_type: Type of boilerplate to generate
        :return: Generated boilerplate code
        """
        templates = {
            'cli_app': self._generate_cli_boilerplate(),
            'fastapi_app': self._generate_fastapi_boilerplate(),
            'ml_model': self._generate_ml_model_boilerplate(),
            'flask_app': self._generate_flask_boilerplate(),
            'pytest_test': self._generate_pytest_boilerplate()
        }
        
        return templates.get(template_type, f"No template found for {template_type}")

    def _generate_cli_boilerplate(self) -> str:
        """Generate CLI application boilerplate."""
        return '''
import typer
from typing import Optional

app = typer.Typer()

@app.command()
def main(
    name: Optional[str] = typer.Option(None, help="Name to greet")
):
    """
    Main CLI entrypoint
    """
    if name:
        print(f"Hello {name}")
    else:
        print("Hello World!")

if __name__ == "__main__":
    app()
'''

    def _generate_fastapi_boilerplate(self) -> str:
        """Generate FastAPI application boilerplate."""
        return '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive")
    return {"item_id": item_id}
'''

    def _generate_ml_model_boilerplate(self) -> str:
        """Generate Machine Learning model boilerplate."""
        return '''
import torch
import torch.nn as nn
import torch.optim as optim

class SimpleModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

def train_model(model, criterion, optimizer, X, y, epochs=100):
    for epoch in range(epochs):
        # Training loop
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
'''

    def _generate_flask_boilerplate(self) -> str:
        """Generate Flask application boilerplate."""
        return '''
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({
        'message': 'Data retrieved successfully',
        'data': []
    })

@app.route('/api/data', methods=['POST'])
def create_data():
    data = request.json
    # Process data here
    return jsonify({
        'message': 'Data created successfully',
        'data': data
    })

if __name__ == '__main__':
    app.run(debug=True)
'''

    def _generate_pytest_boilerplate(self) -> str:
        """Generate Pytest boilerplate."""
        return '''
import pytest

def test_example():
    """
    Example test function
    """
    assert 1 + 1 == 2

def test_another_example():
    """
    Another example test function
    """
    assert len([1, 2, 3]) == 3

@pytest.fixture
def sample_data():
    """
    Example pytest fixture
    """
    return [1, 2, 3, 4, 5]

def test_fixture_example(sample_data):
    """
    Test using a fixture
    """
    assert len(sample_data) == 5
'''

    def analyze_project_structure(self) -> Dict[str, Any]:
        """
        Analyze the current project structure and code organization.
        
        :return: Project structure analysis
        """
        project_structure = {
            'python_files': [],
            'modules': [],
            'packages': []
        }
        
        # Walk through project directory
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, self.project_path)
                    
                    # Analyze Python file
                    with open(full_path, 'r') as f:
                        try:
                            module = ast.parse(f.read())
                            
                            # Collect class and function information
                            classes = [node.name for node in ast.walk(module) if isinstance(node, ast.ClassDef)]
                            functions = [node.name for node in ast.walk(module) if isinstance(node, ast.FunctionDef)]
                            
                            project_structure['python_files'].append({
                                'path': relative_path,
                                'classes': classes,
                                'functions': functions
                            })
                        except SyntaxError:
                            pass
        
        return project_structure

    def suggest_improvements(self) -> List[str]:
        """
        Generate code improvement suggestions based on project analysis.
        
        :return: List of improvement suggestions
        """
        suggestions = []
        
        # Analyze project structure
        structure = self.analyze_project_structure()
        
        # Code organization suggestions
        if len(structure['python_files']) > 10:
            suggestions.append("Consider breaking down large project into multiple packages")
        
        # Complexity and modularity suggestions
        for file in structure['python_files']:
            if len(file['classes']) > 5:
                suggestions.append(f"File {file['path']} might benefit from further modularization")
            
            if len(file['functions']) > 10:
                suggestions.append(f"File {file['path']} has many functions. Consider splitting into smaller modules")
        
        # Best practices suggestions
        suggestions.extend([
            "Ensure consistent type hinting",
            "Add docstrings to all classes and functions",
            "Implement comprehensive error handling",
            "Consider using dataclasses or type annotations",
            "Add logging for better debugging"
        ])
        
        return suggestions
