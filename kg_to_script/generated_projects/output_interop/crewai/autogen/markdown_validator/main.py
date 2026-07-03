import asyncio

from team import (
    requirements_manager,
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
        # Workflow Step: syntax_review_task
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: syntax_review_task")
        print("=" * 80)

        task_prompt = """Use the markdown_validation_tool to review the file(s) at this path: {filename}.
Be sure to pass only the file path to the markdown_validation_tool.
Use the following format to call the markdown_validation_tool:
Do I need to use a tool? Yes
Action: markdown_validation_tool
Action Input: {filename}

Get the validation results from the tool and then summarize it into a list of changes
the developer should make to the document.
DO NOT recommend ways to update the document.
DO NOT change any of the content of the document or add content to it.
It is critical to your task to only respond with a list of changes.

If you already know the answer or if you do not need to use a tool,
return it as your Final Answer. """
        # Execute via the assigned agent: requirements_manager
        result = await requirements_manager.run(task=task_prompt)

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