import os
import json
from typing import Dict, List, Any
import anthropic
from datetime import datetime

class AIInsightGenerator:
    """
    Generates AI-powered insights and recommendations for project development.
    """
    def __init__(self, api_key: str = None):
        """
        Initialize the AI Insight Generator.
        
        :param api_key: Optional Anthropic API key
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-opus-20240229"

    def generate_strategic_recommendations(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate strategic recommendations based on project context.
        
        :param project_context: Current project context
        :return: AI-generated strategic insights
        """
        try:
            # Convert project context to a formatted string
            context_summary = json.dumps(project_context, indent=2)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Analyze the following project context and provide strategic insights:
                        
                        {context_summary}
                        
                        Please provide:
                        1. Strategic development recommendations
                        2. Potential architectural improvements
                        3. Risk assessment and mitigation strategies
                        4. Technology stack optimization suggestions
                        5. Development process enhancements
                        """
                    }
                ]
            )
            
            # Parse AI response
            insights = response.content[0].text
            
            return {
                'strategic_recommendations': self._parse_insights(insights),
                'raw_response': insights,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def analyze_development_trajectory(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """
        Analyze project development trajectory and predict potential challenges.
        
        :param historical_data: Historical project development data
        :return: Development trajectory analysis
        """
        try:
            # Convert historical data to a formatted string
            history_summary = json.dumps(historical_data, indent=2)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Analyze the following project development history:
                        
                        {history_summary}
                        
                        Please provide:
                        1. Development pattern analysis
                        2. Potential future challenges
                        3. Productivity trend insights
                        4. Recommendations for process improvement
                        5. Predictive development trajectory
                        """
                    }
                ]
            )
            
            # Parse AI response
            trajectory_analysis = response.content[0].text
            
            return {
                'trajectory_insights': self._parse_insights(trajectory_analysis),
                'raw_response': trajectory_analysis,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _parse_insights(self, insights_text: str) -> List[str]:
        """
        Parse AI-generated insights into a list of actionable recommendations.
        
        :param insights_text: Raw insights text
        :return: List of parsed insights
        """
        # Simple parsing strategy
        insights = []
        for line in insights_text.split('\n'):
            line = line.strip()
            if line and (line.startswith('1.') or line.startswith('•') or line.startswith('-')):
                insights.append(line)
        
        return insights[:10]  # Limit to top 10 insights

def main(project_path: str):
    """
    Main function to generate AI insights for a project.
    
    :param project_path: Path to the project
    """
    # Example usage
    insight_generator = AIInsightGenerator()
    
    # Load project context (you'd replace this with actual context loading)
    project_context = {
        'name': os.path.basename(project_path),
        'type': 'Software Project',
        'current_phase': 'Development'
    }
    
    # Generate strategic recommendations
    recommendations = insight_generator.generate_strategic_recommendations(project_context)
    print("Strategic Recommendations:")
    for rec in recommendations.get('strategic_recommendations', []):
        print(rec)
