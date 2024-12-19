import os
import json
import subprocess
import requests
from typing import Dict, List, Any
from packaging import version

class DependencyTracker:
    """
    Manages project dependencies, tracking versions, updates, and compatibility.
    """
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.pypi_url = "https://pypi.org/pypi"

    def check_dependencies(self) -> Dict[str, Any]:
        """
        Check current project dependencies and potential updates.
        
        :return: Dictionary of dependency information
        """
        try:
            # Get installed packages
            result = subprocess.run(
                ['pip', 'list', '--format=json'], 
                capture_output=True, 
                text=True
            )
            installed_packages = json.loads(result.stdout)
            
            # Check for updates
            updates = {}
            for pkg in installed_packages:
                name, current_version = pkg['name'], pkg['version']
                
                try:
                    # Get latest version from PyPI
                    response = requests.get(f"{self.pypi_url}/{name}/json")
                    latest_version = response.json()['info']['version']
                    
                    # Compare versions
                    if version.parse(latest_version) > version.parse(current_version):
                        updates[name] = {
                            'current': current_version,
                            'latest': latest_version
                        }
                except Exception as e:
                    # Skip if unable to fetch version
                    pass
            
            return {
                'installed_packages': installed_packages,
                'updates_available': updates
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'details': 'Unable to check dependencies'
            }

    def update_dependencies(self, dependencies: List[str]) -> Dict[str, str]:
        """
        Update specified dependencies.
        
        :param dependencies: List of dependencies to update
        :return: Update results
        """
        results = {}
        for dep in dependencies:
            try:
                # Use pip to update specific package
                result = subprocess.run(
                    ['pip', 'install', '--upgrade', dep],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    results[dep] = 'Successfully updated'
                else:
                    results[dep] = f'Update failed: {result.stderr}'
            
            except Exception as e:
                results[dep] = f'Error updating: {str(e)}'
        
        return results

    def generate_requirements(self, output_path: str = None) -> str:
        """
        Generate a requirements.txt file for the project.
        
        :param output_path: Optional path to save requirements file
        :return: Requirements file content
        """
        try:
            result = subprocess.run(
                ['pip', 'freeze'], 
                capture_output=True, 
                text=True
            )
            requirements = result.stdout
            
            if output_path:
                with open(output_path, 'w') as f:
                    f.write(requirements)
            
            return requirements
        
        except Exception as e:
            return f"Error generating requirements: {str(e)}"
