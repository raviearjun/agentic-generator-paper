"""
Auto-generated CrewAI Main: BlogCrewIndustryspecializedagentsexample

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import BlogCrewIndustryspecializedagentsexample


def run():
    """Run the BlogCrewIndustryspecializedagentsexample."""
    inputs = {
        'weaviate_feature': '',  # TODO: provide a value
    }
    BlogCrewIndustryspecializedagentsexample().crew().kickoff(inputs=inputs)


def train():
    """Train the BlogCrewIndustryspecializedagentsexample for a given number of iterations."""
    inputs = {
        'weaviate_feature': '',  # TODO: provide a value
    }
    try:
        BlogCrewIndustryspecializedagentsexample().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
