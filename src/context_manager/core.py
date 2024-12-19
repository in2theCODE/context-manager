import os
import git
import yaml
import json
from typing import Dict, Optional, Any, List
from jinja2 import Environment, FileSystemLoader
import anthropic
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

class ContextManager:
    def __init__(self, project_path: str):
        self.project_path = os.path.abspath(project_path)
        self.repo = git.Repo(project_path)
        self.context_file = os.path.join(project_path, 'CONTEXT.md')
        self.milestones_file = os.path.join(project_path, 'MILESTONES.yaml')
        self.user_context_file = os.path.join(project_path, 'USER_CONTEXT.md')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Initialize files if they don't exist
        self._initialize_context_files()

    def _initialize_context_files(self):
        """Ensure context and milestone tracking files exist."""
        # Create context file if not exists
        if not os.path.exists(self.context_file):
            with open(self.context_file, 'w') as f:
                f.write("# Project Context\n")
        
        # Create milestones file if not exists
        if not os.path.exists(self.milestones_file):
            with open(self.milestones_file, 'w') as f:
                yaml.dump({
                    'milestones': [],
                    'completed_milestones': []
                }, f)

    def initialize_context(self, template: Optional[str] = None):
        """Initialize project context with optional template."""
        # Default template if none provided
        if not template:
            template = """
# Project Context

## Overview
- Project Name: 
- Description: 
- Start Date: {start_date}

## Development Strategy
1. Initial Setup
2. Core Feature Development
3. Testing and Refinement
4. Documentation
5. Deployment

## Key Stakeholders
- 

## Current Status
- Phase: Initial Setup
- Progress: 0%
"""
        
        # Write context with current date
        with open(self.context_file, 'w') as f:
            f.write(template.format(start_date=datetime.now().strftime("%Y-%m-%d")))

    def update_context(self, ai_insights: bool = False):
        """Update project context, optionally with AI-generated insights."""
        # Gather git-based insights
        commits = list(self.repo.iter_commits())
        recent_commits = commits[:5]  # Last 5 commits
        
        context_update = f"""
## Recent Changes
{len(commits)} total commits

### Last 5 Commits:
{chr(10).join([f"- {commit.summary}" for commit in recent_commits])}

### Repository Statistics
- Total Branches: {len(self.repo.branches)}
- Active Branch: {self.repo.active_branch.name}
"""
        
        # Optional AI-powered insights
        if ai_insights and self.anthropic_api_key:
            context_update += self._generate_ai_insights()
        
        # Append to context file
        with open(self.context_file, 'a') as f:
            f.write(context_update)

    def _generate_ai_insights(self) -> str:
        """Generate AI-powered project insights."""
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=300,
                messages=[
                    {
                        "role": "user", 
                        "content": f"Analyze the development context of this project based on its recent git commits and provide strategic insights for improvement."
                    }
                ]
            )
            return f"\n### AI Development Insights\n{response.content[0].text}"
        except Exception as e:
            return f"\n### AI Insights Error\n{str(e)}"

    def generate_documentation(self, output_format: str = "markdown") -> str:
        """Generate comprehensive project documentation."""
        with open(self.context_file, 'r') as f:
            context = f.read()
        
        output_path = os.path.join(self.project_path, f"PROJECT_DOCS.{output_format}")
        
        with open(output_path, 'w') as f:
            f.write(context)
        
        return output_path

    def get_project_status(self) -> Dict[str, Any]:
        """Retrieve comprehensive project status."""
        commits = list(self.repo.iter_commits())
        
        return {
            "Total Commits": len(commits),
            "Active Branch": self.repo.active_branch.name,
            "Last Commit": commits[0].committed_datetime.strftime("%Y-%m-%d %H:%M:%S") if commits else "No commits",
            "Days Since Start": (datetime.now() - datetime.fromtimestamp(os.path.getctime(self.project_path))).days
        }

    def track_milestone(self, milestone: str):
        """Add a new milestone to track."""
        with open(self.milestones_file, 'r') as f:
            milestones_data = yaml.safe_load(f)
        
        milestones_data['milestones'].append({
            'name': milestone,
            'created_at': datetime.now().isoformat(),
            'status': 'in_progress'
        })
        
        with open(self.milestones_file, 'w') as f:
            yaml.dump(milestones_data, f)

    def complete_milestone(self, milestone: str):
        """Mark a milestone as complete."""
        with open(self.milestones_file, 'r') as f:
            milestones_data = yaml.safe_load(f)
        
        # Move milestone from active to completed
        for m in milestones_data['milestones']:
            if m['name'] == milestone:
                m['status'] = 'completed'
                m['completed_at'] = datetime.now().isoformat()
                milestones_data['completed_milestones'].append(m)
                milestones_data['milestones'].remove(m)
                break
        
        with open(self.milestones_file, 'w') as f:
            yaml.dump(milestones_data, f)

    def list_milestones(self) -> List[str]:
        """List all active milestones."""
        with open(self.milestones_file, 'r') as f:
            milestones_data = yaml.safe_load(f)
        
        return [m['name'] for m in milestones_data.get('milestones', [])]

def main():
    # Example usage
    context_manager = ContextManager('.')
    context_manager.initialize_context()
    context_manager.update_context(ai_insights=True)

if __name__ == "__main__":
    main()
