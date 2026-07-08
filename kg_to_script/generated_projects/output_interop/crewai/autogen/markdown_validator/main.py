import asyncio

from team import (
    requirements_manager,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)
from autogen_agentchat.messages import BaseChatMessage, TextMessage

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution.
        #
        # `history` accumulates every step's real conversation so far and is
        # threaded into each subsequent step's .run() call. Without this,
        # each step only ever sees its own task prompt in isolation - later
        # steps (e.g. "review the draft") have no way to see what an earlier
        # step (e.g. "draft the posting") actually produced.
        history: list[BaseChatMessage] = []
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
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: requirements_manager, passing the
        # accumulated history so this step can see every prior step's output.
        result = await requirements_manager.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

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