import typer
import os
import json
from typing import Optional
from rich.console import Console
from rich.markdown import Markdown

from .components.project_tracking.context_system import ProjectContextManager
from .components.dependency_management.dependency_tracker import DependencyTracker
from .components.code_analysis.code_generator import CodeGenerator
from .utils.onboarding import start_project_onboarding

# Create multiple app instances for more flexible command routing
app = typer.Typer()
context_app = typer.Typer()
deps_app = typer.Typer()
code_app = typer.Typer()
onboard_app = typer.Typer()

app.add_typer(context_app, name="context")
app.add_typer(deps_app, name="deps")
app.add_typer(code_app, name="code")
app.add_typer(onboard_app, name="onboard")

console = Console()

@onboard_app.command(name="init", help="Interactive project initialization")
def onboard_project(
    project_path: str = typer.Argument(default="."),
):
    """Start an interactive project onboarding process."""
    console.print(f"[yellow]🚀 Starting project onboarding for {project_path}[/yellow]")
    start_project_onboarding(project_path)
    console.print("[green]✨ Project onboarding complete![/green]")

@context_app.command(name="track", help="Track project development context")
def track_context(
    project_path: str = typer.Argument(default="."),
    milestone: Optional[str] = typer.Option(None, help="Add a new milestone"),
):
    """Manage and track project development context."""
    context_manager = ProjectContextManager(project_path)
    
    if milestone:
        context_manager.add_milestone(milestone)
        console.print(f"[green]✅ Milestone added: {milestone}[/green]")
    
    # Display current context
    context = context_manager.get_current_context()
    console.print(Markdown("## Current Project Context"))
    console.print(json.dumps(context, indent=2))

@deps_app.command(name="check", help="Check project dependencies")
def check_dependencies(
    project_path: str = typer.Argument(default="."),
):
    """Check and report on project dependencies."""
    dep_tracker = DependencyTracker(project_path)
    
    # Check dependencies
    updates = dep_tracker.check_dependencies()
    
    console.print(Markdown("## Dependency Updates"))
    console.print(json.dumps(updates, indent=2))

@code_app.command(name="generate", help="Generate code boilerplate")
def generate_code(
    template: str = typer.Argument(..., help="Type of code template to generate"),
    output: Optional[str] = typer.Option(None, help="Output file for generated code"),
):
    """Generate boilerplate code for various project types."""
    code_generator = CodeGenerator(os.getcwd())
    
    # Generate code
    generated_code = code_generator.generate_boilerplate(template)
    
    console.print(f"[yellow]🚀 Generating {template} boilerplate[/yellow]")
    console.print(generated_code)
    
    if output:
        with open(output, 'w') as f:
            f.write(generated_code)
        console.print(f"[green]💾 Code saved to {output}[/green]")

def main():
    """Main entry point for the CLI application."""
    app()

if __name__ == "__main__":
    main()
