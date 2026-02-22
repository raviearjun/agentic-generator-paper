"""
Auto-generated CrewAI Main: CopyCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import CopyCrew


def run():
    """Run the CopyCrew."""
    inputs = {
        'product_website': '',  # TODO: provide a value
        'product_details': '',  # TODO: provide a value
        'copy': '',  # TODO: provide a value
    }
    CopyCrew().crew().kickoff(inputs=inputs)


def train():
    """Train the CopyCrew for a given number of iterations."""
    inputs = {
        'product_website': '',  # TODO: provide a value
        'product_details': '',  # TODO: provide a value
        'copy': '',  # TODO: provide a value
    }
    try:
        CopyCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
