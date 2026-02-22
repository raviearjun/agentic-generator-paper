"""
Auto-generated CrewAI Main: MyCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import MyCrew


def run():
    """Run the MyCrew."""
    inputs = {
        'origin': '',  # TODO: provide a value
        'cities': '',  # TODO: provide a value
        'range': '',  # TODO: provide a value
        'interests': '',  # TODO: provide a value
    }
    MyCrew().crew().kickoff(inputs=inputs)


def train():
    """Train the MyCrew for a given number of iterations."""
    inputs = {
        'origin': '',  # TODO: provide a value
        'cities': '',  # TODO: provide a value
        'range': '',  # TODO: provide a value
        'interests': '',  # TODO: provide a value
    }
    try:
        MyCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
