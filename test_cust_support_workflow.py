"""
Test Script for Customer Support Workflow (AutoGen)
Alternative workflow for testing generated AutoGen scripts
"""

import autogen
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read API key from environment
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set. Please create a .env file with your API key.")

config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": api_key
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
}

# Support Ticket Analyzer Agent
ticket_analyzer = autogen.AssistantAgent(
    name="TicketAnalyzer",
    system_message="""You are a customer support ticket analyzer. Your role is to:
    1. Analyze incoming support tickets
    2. Extract key information (issue type, severity, customer details)
    3. Categorize the ticket (technical, billing, general inquiry)
    4. Determine urgency level (high, medium, low)
    
    You have extensive experience in customer support and can quickly identify patterns and priorities.""",
    llm_config=llm_config,
)

# Solution Provider Agent
solution_provider = autogen.AssistantAgent(
    name="SolutionProvider",
    system_message="""You are a technical solution provider. Your role is to:
    1. Review analyzed ticket information
    2. Provide step-by-step solutions or troubleshooting steps
    3. Suggest relevant documentation or resources
    4. Escalate to specialized teams if needed
    
    You have deep technical knowledge and excellent problem-solving skills.""",
    llm_config=llm_config,
)

# Quality Assurance Agent
qa_agent = autogen.AssistantAgent(
    name="QualityAssurance",
    system_message="""You are a quality assurance specialist. Your role is to:
    1. Review the proposed solution
    2. Verify completeness and accuracy
    3. Ensure customer-friendly language
    4. Approve or request revisions
    
    You ensure all responses meet company quality standards.""",
    llm_config=llm_config,
)

# User Proxy (simulates human interaction)
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",  # Automated for testing
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
)

# Create Group Chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, ticket_analyzer, solution_provider, qa_agent],
    messages=[],
    max_round=12
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

if __name__ == "__main__":
    print("=" * 70)
    print("Starting Customer Support Workflow (AutoGen)")
    print("=" * 70)
    print()
    
    # Simulate support ticket
    support_ticket = """
    New Support Ticket #12345
    
    Customer: John Smith (Premium Plan)
    Email: john.smith@company.com
    Subject: Database connection keeps timing out
    
    Description:
    Our application has been experiencing database connection timeouts for the past 3 hours. 
    This is affecting our production environment and impacting approximately 500 users.
    We're getting "Connection timeout after 30 seconds" errors consistently.
    
    Steps already tried:
    - Restarted application server
    - Checked network connectivity
    - Verified database is running
    
    Priority: HIGH
    Time logged: 2024-01-15 14:30 UTC
    
    Please analyze this ticket, provide a solution, and ensure quality before responding to the customer.
    """
    
    try:
        # Initiate the conversation
        user_proxy.initiate_chat(
            manager,
            message=support_ticket
        )
        
        print()
        print("=" * 70)
        print("Workflow Completed Successfully!")
        print("=" * 70)
        
    except Exception as e:
        print()
        print("=" * 70)
        print("Error during workflow execution:")
        print("=" * 70)
        print(f"{type(e).__name__}: {str(e)}")