"""
Auto-generated CrewAI Main: MeetingPreparationCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import MeetingPreparationCrew


def run():
    """Run the MeetingPreparationCrew."""
    inputs = {
        'participants': '',  # TODO: provide a value
        'context': '',  # TODO: provide a value
        'objective': '',  # TODO: provide a value
    }
    MeetingPreparationCrew().crew().kickoff(inputs=inputs)


def train():
    """Train the MeetingPreparationCrew for a given number of iterations."""
    inputs = {
        'participants': '',  # TODO: provide a value
        'context': '',  # TODO: provide a value
        'objective': '',  # TODO: provide a value
    }
    try:
        MeetingPreparationCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
