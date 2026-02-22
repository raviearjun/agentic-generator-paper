"""
Auto-generated CrewAI Main: ExpandIdeaCrewteam

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import ExpandIdeaCrewteam


def run():
    """Run the ExpandIdeaCrewteam."""
    inputs = {
        'idea': '',  # TODO: provide a value
        'component': '',  # TODO: provide a value
        'expanded_idea': '',  # TODO: provide a value
        'file_content': '',  # TODO: provide a value
    }
    ExpandIdeaCrewteam().crew().kickoff(inputs=inputs)


def train():
    """Train the ExpandIdeaCrewteam for a given number of iterations."""
    inputs = {
        'idea': '',  # TODO: provide a value
        'component': '',  # TODO: provide a value
        'expanded_idea': '',  # TODO: provide a value
        'file_content': '',  # TODO: provide a value
    }
    try:
        ExpandIdeaCrewteam().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
