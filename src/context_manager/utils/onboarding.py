import os
import yaml
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
import anthropic

class ProjectOnboarding:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.console = Console()
        self.anthropic_client = anthropic.Anthropic()
        self.onboarding_file = os.path.join(project_path, 'PROJECT_BLUEPRINT.yaml')

    def start_onboarding(self):
        """Initiate interactive project onboarding process."""
        self.console.print("[bold cyan]🚀 Welcome to Project Initialization[/bold cyan]")
        
        # Gather initial project details
        project_details = self._gather_project_details()
        
        # Generate development strategy with Claude
        development_strategy = self._generate_development_strategy(project_details)
        
        # Create project blueprint
        self._create_project_blueprint(project_details, development_strategy)
        
        # Provide development standards guidance
        self._provide_development_standards()

    def _gather_project_details(self) -> dict:
        """Interactively gather project details."""
        details = {}
        
        details['name'] = Prompt.ask("🏷️  Project Name", default="MyProject")
        details['description'] = Prompt.ask("📝 Project Description", default="A new software project")
        details['domain'] = Prompt.ask("🌐 Project Domain/Industry", default="General")
        
        # Project type selection
        project_types = ["Web Application", "Mobile App", "Desktop App", "CLI Tool", "Library/Package", "Machine Learning", "Other"]
        details['type'] = Prompt.ask("🔧 Project Type", choices=project_types, default="Other")
        
        # Technology stack preferences
        details['primary_language'] = Prompt.ask("💻 Primary Programming Language", default="Python")
        details['frameworks'] = Prompt.ask("🔬 Preferred Frameworks/Libraries", default="")
        
        return details

    def _generate_development_strategy(self, project_details: dict) -> dict:
        """Use Claude to generate a tailored development strategy."""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Help create a comprehensive development strategy for a new software project with these characteristics:
                        
                        Project Name: {project_details['name']}
                        Project Type: {project_details['type']}
                        Primary Language: {project_details['primary_language']}
                        Domain: {project_details['domain']}

                        Please provide:
                        1. Phased development roadmap
                        2. Key milestones
                        3. Potential technical challenges
                        4. Recommended best practices
                        5. Initial architectural considerations
                        """
                    }
                ]
            )
            
            strategy_text = response.content[0].text
            
            # Parse strategy into structured format
            return {
                "roadmap": self._extract_roadmap(strategy_text),
                "milestones": self._extract_milestones(strategy_text),
                "challenges": self._extract_challenges(strategy_text),
                "best_practices": self._extract_best_practices(strategy_text)
            }
        
        except Exception as e:
            self.console.print(f"[red]Error generating strategy: {e}[/red]")
            return {}

    def _create_project_blueprint(self, project_details: dict, strategy: dict):
        """Create a comprehensive project blueprint YAML file."""
        blueprint = {
            "project": project_details,
            "development_strategy": strategy
        }
        
        with open(self.onboarding_file, 'w') as f:
            yaml.dump(blueprint, f, default_flow_style=False)
        
        self.console.print(f"[green]📋 Project blueprint created at {self.onboarding_file}[/green]")

    def _provide_development_standards(self):
        """Offer guidance on development standards and best practices."""
        standards = [
            "🔒 Follow SOLID principles",
            "🧪 Implement comprehensive testing (unit, integration, e2e)",
            "📝 Maintain clear, concise documentation",
            "🔄 Use semantic versioning",
            "🌿 Adopt a branching strategy (e.g., GitFlow)",
            "🤝 Code review and pair programming",
            "🔍 Static code analysis",
            "🚀 Continuous Integration/Continuous Deployment (CI/CD)"
        ]
        
        self.console.print("\n[bold]🏆 Recommended Development Standards:[/bold]")
        for standard in standards:
            self.console.print(standard)

    def _extract_roadmap(self, strategy_text: str) -> list:
        """Extract development roadmap from strategy text."""
        roadmap_lines = [line.strip() for line in strategy_text.split('\n') if 'Phase' in line or 'Stage' in line]
        return roadmap_lines[:5]  # Limit to first 5 phases

    def _extract_milestones(self, strategy_text: str) -> list:
        """Extract key milestones from strategy text."""
        milestone_keywords = ['milestone', 'key deliverable', 'major goal']
        milestones = []
        for line in strategy_text.split('\n'):
            if any(keyword in line.lower() for keyword in milestone_keywords):
                milestones.append(line.strip())
        return milestones[:5]  # Limit to first 5 milestones

    def _extract_challenges(self, strategy_text: str) -> list:
        """Extract potential technical challenges."""
        challenge_keywords = ['challenge', 'potential issue', 'complexity']
        challenges = []
        for line in strategy_text.split('\n'):
            if any(keyword in line.lower() for keyword in challenge_keywords):
                challenges.append(line.strip())
        return challenges[:5]  # Limit to first 5 challenges

    def _extract_best_practices(self, strategy_text: str) -> list:
        """Extract recommended best practices."""
        practice_keywords = ['best practice', 'recommendation', 'should']
        practices = []
        for line in strategy_text.split('\n'):
            if any(keyword in line.lower() for keyword in practice_keywords):
                practices.append(line.strip())
        return practices[:5]  # Limit to first 5 practices

def start_project_onboarding(project_path: str):
    """CLI-friendly function to start project onboarding."""
    onboarding = ProjectOnboarding(project_path)
    onboarding.start_onboarding()
