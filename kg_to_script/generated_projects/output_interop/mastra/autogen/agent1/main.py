import asyncio

from team import (
    mastra_agent_client,
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
        # Workflow Step: task_process_request
        # Workflow Edge: task_process_request -> task_execute_client_tool
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_process_request")
        print("=" * 80)

        task_prompt = """Process incoming generate/stream request: validate params, prepare requestContext and clientTools, and forward to server endpoints (/agents/{agentId}/generate or /agents/{agentId}/stream). """
        # Execute via the assigned agent: mastra_agent_client
        result = await mastra_agent_client.run(task=task_prompt)

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
        # Execute via the assigned agent: mastra_agent_client
        result = await mastra_agent_client.run(task=task_prompt)

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
        # Execute via the assigned agent: mastra_agent_client
        result = await mastra_agent_client.run(task=task_prompt)

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