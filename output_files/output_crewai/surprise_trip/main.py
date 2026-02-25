"""
Auto-generated CrewAI Main: SurpriseTravelCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import SurpriseTravelCrew


def run():
    """Run the SurpriseTravelCrew."""
    inputs = {
        'destination': '',  # TODO: provide a value
        'origin': '',  # TODO: provide a value
        'age': '',  # TODO: provide a value
        'hotel_location': '',  # TODO: provide a value
        'flight_information': '',  # TODO: provide a value
        'trip_duration': '',  # TODO: provide a value
    }
    SurpriseTravelCrew().crew().kickoff(inputs=inputs)


def train():
    """Train the SurpriseTravelCrew for a given number of iterations."""
    inputs = {
        'destination': '',  # TODO: provide a value
        'origin': '',  # TODO: provide a value
        'age': '',  # TODO: provide a value
        'hotel_location': '',  # TODO: provide a value
        'flight_information': '',  # TODO: provide a value
        'trip_duration': '',  # TODO: provide a value
    }
    try:
        SurpriseTravelCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
