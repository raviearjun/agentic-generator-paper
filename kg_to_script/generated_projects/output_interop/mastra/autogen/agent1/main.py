import asyncio

from team import (
    mastra_agent_client,
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
        # Workflow Step: task_process_request
        # Workflow Edge: task_process_request -> task_execute_client_tool
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_process_request")
        print("=" * 80)

        task_prompt = """Process incoming generate/stream request: validate params, prepare requestContext and clientTools, and forward to server endpoints (/agents/{agentId}/generate or /agents/{agentId}/stream). """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: mastra_agent_client, passing the
        # accumulated history so this step can see every prior step's output.
        result = await mastra_agent_client.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_execute_client_tool
        # Workflow Edge: task_execute_client_tool -> task_return_response
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_execute_client_tool")
        print("=" * 80)

        task_prompt = """Handle tool-call finish reason: locate pending client tool calls, execute `clientTool.execute`, attach observability data, synthesize tool-result chunks, and continue the stream/recursion as needed. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: mastra_agent_client, passing the
        # accumulated history so this step can see every prior step's output.
        result = await mastra_agent_client.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_return_response
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_return_response")
        print("=" * 80)

        task_prompt = """Finalize and return the response stream to the client; close controller when no client-tool continuation is required, or recursively continue the stream if client-tools were executed. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: mastra_agent_client, passing the
        # accumulated history so this step can see every prior step's output.
        result = await mastra_agent_client.run(task=history)
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