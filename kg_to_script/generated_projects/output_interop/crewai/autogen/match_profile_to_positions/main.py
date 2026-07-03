import asyncio

from team import (
    cv_reader,
    matcher,
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
        # Workflow Step: task_read_cv
        # Workflow Edge: task_read_cv -> task_match_cv
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_read_cv")
        print("=" * 80)

        task_prompt = """Extract relevant information from the given CV: professional summary, technical skills, work history, education, key achievements. """
        # Execute via the assigned agent: cv_reader
        result = await cv_reader.run(task=task_prompt)

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_match_cv
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_match_cv")
        print("=" * 80)

        task_prompt = """Match the CV to the job opportunities based on skills, experience, and key achievements; produce a ranked list. """
        # Execute via the assigned agent: matcher
        result = await matcher.run(task=task_prompt)

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