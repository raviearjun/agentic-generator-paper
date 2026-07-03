import asyncio

from team import (
    mastra_llm,
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
        # Workflow Step: gather_candidate_info_task
        # Workflow Edge: gather_candidate_info_task -> ask_about_specialty_task
        # Workflow Edge: gather_candidate_info_task -> ask_about_role_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: gather_candidate_info_task")
        print("=" * 80)

        task_prompt = """You are given this resume text: "${resumeText}" """
        # Execute via the assigned agent: mastra_llm
        result = await mastra_llm.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: ask_about_specialty_task
        # Workflow Edge: ask_about_specialty_task -> ask_about_role_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: ask_about_specialty_task")
        print("=" * 80)

        task_prompt = """You are a recruiter. Given the resume below, craft a short question for ${candidateName} about how they got into "${specialty}". Resume: ${resumeText} """
        # Execute via the assigned agent: mastra_llm
        result = await mastra_llm.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: ask_about_role_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: ask_about_role_task")
        print("=" * 80)

        task_prompt = """You are a recruiter. Given the resume below, craft a short question for ${candidateName} asking what interests them most about this role. Resume: ${resumeText} """
        # Execute via the assigned agent: mastra_llm
        result = await mastra_llm.run(task=task_prompt)

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