"""
Auto-generated CrewAI Main: RecruitmentCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import RecruitmentCrew


def run():
    """Run the RecruitmentCrew."""
    inputs = {
        'job_requirements': '',  # TODO: provide a value
    }
    RecruitmentCrew().crew().kickoff(inputs=inputs)


def train():
    """Train the RecruitmentCrew for a given number of iterations."""
    inputs = {
        'job_requirements': '',  # TODO: provide a value
    }
    try:
        RecruitmentCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
