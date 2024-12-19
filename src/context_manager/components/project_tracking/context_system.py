import os
import yaml
from datetime import datetime
from typing import Dict, Any, Optional

class ProjectContextManager:
    """
    Manages comprehensive project context, tracking development progress, milestones, and metadata.
    """
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.context_dir = os.path.join(project_path, '.context')
        self.context_file = os.path.join(self.context_dir, 'GLOBAL_CONTEXT.yaml')
        
        # Ensure context directory exists
        os.makedirs(self.context_dir, exist_ok=True)
        
        # Initialize context if not exists
        self._initialize_context()

    def _initialize_context(self):
        """
        Initialize the project context file with default structure.
        """
        if not os.path.exists(self.context_file):
            initial_context = {
                'project': {
                    'name': os.path.basename(self.project_path),
                    'created_at': datetime.now().isoformat(),
                    'last_updated': datetime.now().isoformat()
                },
                'development': {
                    'current_phase': 'initialization',
                    'milestones': [],
                    'completed_milestones': []
                }
            }
            
            with open(self.context_file, 'w') as f:
                yaml.safe_dump(initial_context, f, default_flow_style=False)

    def add_milestone(self, milestone: str):
        """
        Add a new milestone to the project context.
        
        :param milestone: Milestone description
        """
        # Load current context
        with open(self.context_file, 'r') as f:
            context = yaml.safe_load(f)
        
        # Add milestone
        context['development']['milestones'].append({
            'description': milestone,
            'added_at': datetime.now().isoformat(),
            'status': 'pending'
        })
        
        # Update last updated timestamp
        context['project']['last_updated'] = datetime.now().isoformat()
        
        # Save updated context
        with open(self.context_file, 'w') as f:
            yaml.safe_dump(context, f, default_flow_style=False)

    def get_current_context(self) -> Dict[str, Any]:
        """
        Retrieve the current project context.
        
        :return: Current project context
        """
        with open(self.context_file, 'r') as f:
            return yaml.safe_load(f)

    def update_context(self, update_type: str, details: Dict[str, Any]):
        """
        Update the project context with new information.
        
        :param update_type: Type of update (e.g., 'milestone', 'phase')
        :param details: Details of the update
        """
        # Load current context
        with open(self.context_file, 'r') as f:
            context = yaml.safe_load(f)
        
        # Update timestamp
        context['project']['last_updated'] = datetime.now().isoformat()
        
        # Perform specific updates based on update type
        if update_type == 'milestone':
            context['development']['milestones'].append(details)
        elif update_type == 'phase':
            context['development']['current_phase'] = details.get('phase', context['development']['current_phase'])
        
        # Save updated context
        with open(self.context_file, 'w') as f:
            yaml.safe_dump(context, f, default_flow_style=False)
