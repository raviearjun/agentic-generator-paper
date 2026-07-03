import asyncio

from team import (
    lead_market_analyst,
    chief_marketing_strategist,
    creative_content_creator,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution
        # ==================================================
        # Workflow Step: task_research
        # Workflow Edge: task_research -> task_project_understanding
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_research")
        print("=" * 80)

        task_prompt = """Conduct a thorough research about the customer and competitors in the context of {customer_domain}.
Make sure you find any interesting and relevant information given the current year is 2024.
We are working with them on the following project: {project_description}. """
        # Execute via the assigned agent: lead_market_analyst
        result = await lead_market_analyst.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_project_understanding
        # Workflow Edge: task_project_understanding -> task_marketing_strategy
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_project_understanding")
        print("=" * 80)

        task_prompt = """Understand the project details and the target audience for {project_description}.
Review any provided materials and gather additional information as needed. """
        # Execute via the assigned agent: chief_marketing_strategist
        result = await chief_marketing_strategist.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_marketing_strategy
        # Workflow Edge: task_marketing_strategy -> task_campaign_idea
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_marketing_strategy")
        print("=" * 80)

        task_prompt = """Formulate a comprehensive marketing strategy for the project {project_description} of the customer {customer_domain}.
Use the insights from the research task and the project understanding task to create a high-quality strategy. """
        # Execute via the assigned agent: chief_marketing_strategist
        result = await chief_marketing_strategist.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_campaign_idea
        # Workflow Edge: task_campaign_idea -> task_copy_creation
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_campaign_idea")
        print("=" * 80)

        task_prompt = """Develop creative marketing campaign ideas for {project_description}.
Ensure the ideas are innovative, engaging, and aligned with the overall marketing strategy. """
        # Execute via the assigned agent: creative_content_creator
        result = await creative_content_creator.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_copy_creation
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_copy_creation")
        print("=" * 80)

        task_prompt = """Create marketing copies based on the approved campaign ideas for {project_description}.
Ensure the copies are compelling, clear, and tailored to the target audience. """
        # Execute via the assigned agent: creative_content_creator
        result = await creative_content_creator.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        print("\n" + "=" * 80)
        print("DONE")
        print("=" * 80)

    except Exception as e:
        print("\n" + "=" * 80)
        print("ERROR")
        print("=" * 80)
        print(type(e).__name__)
        print(str(e))



if __name__ == "__main__":
    asyncio.run(main())