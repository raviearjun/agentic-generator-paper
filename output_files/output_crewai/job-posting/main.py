"""
Auto-generated CrewAI Main: JobPostingCrewTeam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import JobPostingCrewTeam


def run():
    """Run the JobPostingCrewTeam."""
    inputs = {
        'company_domain': 'careers.wbd.com',
        'company_description': 'Warner Bros. Discovery is a premier global media and entertainment company, offering audiences the world’s most differentiated and complete portfolio of content, brands and franchises across television, film, sports, news, streaming and gaming. We\'re home to the world’s best storytellers, creating world-class products for consumers',
        'hiring_needs': 'Production Assistant, for a TV production set in Los Angeles in June 2025',
        'specific_benefits': 'Weekly Pay, Employee Meals, healthcare',
    }
    JobPostingCrewTeam().crew().kickoff(inputs=inputs)


def train():
    """Train the JobPostingCrewTeam for a given number of iterations."""
    inputs = {
        'company_domain': 'careers.wbd.com',
        'company_description': 'Warner Bros. Discovery is a premier global media and entertainment company, offering audiences the world’s most differentiated and complete portfolio of content, brands and franchises across television, film, sports, news, streaming and gaming. We\'re home to the world’s best storytellers, creating world-class products for consumers',
        'hiring_needs': 'Production Assistant, for a TV production set in Los Angeles in June 2025',
        'specific_benefits': 'Weekly Pay, Employee Meals, healthcare',
    }
    try:
        JobPostingCrewTeam().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
