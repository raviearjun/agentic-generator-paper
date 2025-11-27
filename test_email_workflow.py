"""
Test Script for Email Auto-Responder Flow (CrewAI)
Modified to include OpenAI LLM configuration with environment variable
"""

from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set. Please create a .env file with your API key.")

# Configure OpenAI LLM with API key from environment
llm = LLM(
    model="gpt-4o-mini",
    api_key=api_key
)

# Email Classifier Agent
email_classifier = Agent(
    role="Email Classifier",
    goal="Accurately classify incoming emails by priority (urgent, normal, low) and type (support, sales, info)",
    backstory="You are an experienced email triage specialist who can quickly assess the importance and category of incoming messages. You have years of experience in customer service and understand the nuances of business communication.",
    llm=llm,
    verbose=True
)

# Response Generator Agent
response_generator = Agent(
    role="Response Generator",
    goal="Generate contextual and professional email responses based on email content and classification",
    backstory="You are a skilled communication professional who crafts clear, polite, and helpful email responses. You understand tone, context, and how to address different types of inquiries appropriately.",
    llm=llm,
    verbose=True
)

# Human Reviewer Agent (simulated)
human_reviewer = Agent(
    role="Human Reviewer",
    goal="Review generated responses for quality, accuracy, and appropriateness before sending",
    backstory="You are a quality assurance specialist who ensures all outgoing communications meet company standards. You check for tone, accuracy, and completeness in every response.",
    llm=llm,
    verbose=True
)

# Task 1: Monitor and identify new email (simulated)
task_monitoring = Task(
    description="""Simulate monitoring the inbox. For this demo, assume you have received a new email with the following content:
    
    From: customer@example.com
    Subject: Urgent: Cannot access my account
    Body: Hello, I've been trying to log into my account for the past 2 hours but keep getting an error message. This is urgent as I need to access important documents for a meeting tomorrow morning. Please help!
    
    Extract and summarize the key details from this email.""",
    expected_output="Summary of the email including sender, subject, main issue, and urgency level",
    agent=email_classifier
)

# Task 2: Classify the email
task_classification = Task(
    description="Based on the email monitoring results, classify this email by priority (urgent, normal, or low) and type (support, sales, or info). Provide reasoning for your classification.",
    expected_output="Classification result with priority level, email type, and reasoning",
    agent=email_classifier
)

# Task 3: Generate response
task_generate = Task(
    description="Based on the email classification, generate a professional and helpful response email. The response should: 1) Acknowledge the urgency, 2) Provide immediate troubleshooting steps, 3) Offer alternative support channels, 4) Set expectations for resolution time.",
    expected_output="Complete draft email response ready for review, including greeting, body, and closing",
    agent=response_generator
)

# Task 4: Review and approve
task_approval = Task(
    description="Review the generated email response for: 1) Professional tone, 2) Accuracy and helpfulness, 3) Appropriate urgency acknowledgment, 4) Clear action items. Either approve the response or suggest specific improvements.",
    expected_output="Final approval with either 'APPROVED' status or list of required modifications",
    agent=human_reviewer
)

# Create Crew with sequential process
email_workflow_crew = Crew(
    agents=[email_classifier, response_generator, human_reviewer],
    tasks=[task_monitoring, task_classification, task_generate, task_approval],
    verbose=True
)

if __name__ == "__main__":
    print("=" * 70)
    print("Starting Email Auto-Responder Workflow (CrewAI + OpenAI)")
    print("=" * 70)
    print()
    
    try:
        # Run the workflow
        result = email_workflow_crew.kickoff()
        
        print()
        print("=" * 70)
        print("Workflow Completed Successfully!")
        print("=" * 70)
        print()
        print("Final Result:")
        print(result)
        
    except Exception as e:
        print()
        print("=" * 70)
        print("Error during workflow execution:")
        print("=" * 70)
        print(f"{type(e).__name__}: {str(e)}")