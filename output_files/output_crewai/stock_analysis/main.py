"""
Auto-generated CrewAI Main: StockAnalysisCrew

Source  : AgentO Knowledge Graph → SPARQL → Pydantic → Jinja2
Pipeline: 3-Layer Conversion Pipeline
"""

import sys
from dotenv import load_dotenv

# Load .env from this directory BEFORE importing crew (which triggers crewai init)
load_dotenv()

from crew import StockAnalysisCrew


def run():
    """Run the StockAnalysisCrew."""
    inputs = {
        'company_stock': '',  # TODO: provide a value
    }
    StockAnalysisCrew().crew().kickoff(inputs=inputs)


def train():
    """Train the StockAnalysisCrew for a given number of iterations."""
    inputs = {
        'company_stock': '',  # TODO: provide a value
    }
    try:
        StockAnalysisCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


if __name__ == "__main__":
    result = run()
    print(result)
