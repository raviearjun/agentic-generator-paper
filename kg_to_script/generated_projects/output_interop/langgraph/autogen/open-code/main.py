import asyncio

from team import (
    langgraph_agent,
    human_user,
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
        # Workflow Step: task_propose_change
        # Workflow Edge: task_propose_change -> task_user_decision
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_propose_change")
        print("=" * 80)

        task_prompt = """Render the proposed change (code diff / description) to the user and request an explicit accept or reject decision. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: langgraph_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await langgraph_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_user_decision
        # Workflow Edge: task_user_decision -> task_handle_reject
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_user_decision")
        print("=" * 80)

        task_prompt = """User evaluates the proposed change and selects accept or reject; the selection drives subsequent tool calls and UI state. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_handle_reject
        # Workflow Edge: task_handle_reject -> task_finalize_ui
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_handle_reject")
        print("=" * 80)

        task_prompt = """On reject: call the update_file tool with REJECTED_CHANGE_CONTENT (or do not apply change) and submit a human message 'Rejected change.'. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: langgraph_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await langgraph_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_finalize_ui
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_finalize_ui")
        print("=" * 80)

        task_prompt = """Render final accepted or rejected status in the UI and present an artifact view of the proposed change. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: langgraph_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await langgraph_agent.run(task=history)
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