import sys
from job_posting.crew import JobPostingCrew

def run():
    inputs = {
        'company_domain': 'openai.com',
        'company_description': 'OpenAI is an AI research and deployment company that develops advanced language models and AI tools for consumers, developers, and enterprises.',
        'hiring_needs': 'Software Engineers, Research Engineers, Machine Learning Engineers, Product Designers, and Technical Program Managers.',
        'specific_benefits': 'Competitive salary, equity, comprehensive health insurance, flexible work arrangements, generous parental leave, learning and development budget, and retirement benefits.'
    }
    JobPostingCrew().crew().kickoff(inputs=inputs)



def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'company_domain': 'openai.com',
        'company_description': 'OpenAI is an AI research and deployment company that develops advanced language models and AI tools for consumers, developers, and enterprises.',
        'hiring_needs': 'Software Engineers, Research Engineers, Machine Learning Engineers, Product Designers, and Technical Program Managers.',
        'specific_benefits': 'Competitive salary, equity, comprehensive health insurance, flexible work arrangements, generous parental leave, learning and development budget, and retirement benefits.'
    }
    try:
        JobPostingCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
