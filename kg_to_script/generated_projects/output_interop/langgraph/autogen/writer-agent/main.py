import asyncio

from team import (
    writer_agent,
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
        # Workflow Step: task_prepare
        # Workflow Edge: task_prepare -> task_writer
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_prepare")
        print("=" * 80)

        task_prompt = """Prepare a text document for the user with a short title and short description for browsing purposes. Can be also used when creating a new version of the document. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: writer_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await writer_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_writer
        # Workflow Edge: task_writer -> task_suggestions
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_writer")
        print("=" * 80)

        task_prompt = """Write a text document based on the user's request. Only output the content, do not ask any additional questions. If there is selected text in state.context.writer.selected, include that context in the generation. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: writer_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await writer_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_suggestions
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_suggestions")
        print("=" * 80)

        task_prompt = """Invoke the model on the conversation messages (including tool finished signals) to produce the finish/suggestions message; append the resulting model output to the message stream. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: writer_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await writer_agent.run(task=history)
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