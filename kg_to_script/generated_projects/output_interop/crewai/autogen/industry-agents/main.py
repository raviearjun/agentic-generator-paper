import asyncio

from team import (
    biomedical_marketing_agent,
    healthcare_marketing_agent,
    financial_marketing_agent,
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
        # Workflow Step: task_biomedical_research
        # Workflow Edge: task_biomedical_research -> task_healthcare_research
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_biomedical_research")
        print("=" * 80)

        task_prompt = """Conduct a thorough research about {weaviate_feature}. Make sure you find any interesting and relevant information using the web and Weaviate blogs. """
        # Execute via the assigned agent: biomedical_marketing_agent
        result = await biomedical_marketing_agent.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_healthcare_research
        # Workflow Edge: task_healthcare_research -> task_financial_research
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_healthcare_research")
        print("=" * 80)

        task_prompt = """Conduct a thorough research about {weaviate_feature}. Make sure you find any interesting and relevant information using the web and Weaviate blogs. """
        # Execute via the assigned agent: healthcare_marketing_agent
        result = await healthcare_marketing_agent.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_financial_research
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_financial_research")
        print("=" * 80)

        task_prompt = """Conduct a thorough research about {weaviate_feature}. Make sure you find any interesting and relevant information using the web and Weaviate blogs. """
        # Execute via the assigned agent: financial_marketing_agent
        result = await financial_marketing_agent.run(task=task_prompt)

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