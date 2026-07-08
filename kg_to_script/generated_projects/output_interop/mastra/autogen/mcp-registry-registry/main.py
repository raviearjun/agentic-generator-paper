import asyncio

from team import (
    registry_registry_server,
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
        # Workflow Step: task_fetch_servers_from_registry
        # Workflow Edge: task_fetch_servers_from_registry -> task_post_process_servers
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_fetch_servers_from_registry")
        print("=" * 80)

        task_prompt = """Fetch servers from the registry by locating the registry entry in local registryData, verifying servers_url, performing HTTP GET, and returning raw response for post-processing. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: registry_registry_server, passing the
        # accumulated history so this step can see every prior step's output.
        result = await registry_registry_server.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_post_process_servers
        # Workflow Edge: task_post_process_servers -> task_filter_servers
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_post_process_servers")
        print("=" * 80)

        task_prompt = """Normalize registry-specific response formats into canonical ServerEntry objects with id, name, description, createdAt, updatedAt using the registry's postProcessServers function when available. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: registry_registry_server, passing the
        # accumulated history so this step can see every prior step's output.
        result = await registry_registry_server.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_filter_servers
        # Workflow Edge: task_filter_servers -> task_get_servers_from_registry
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_filter_servers")
        print("=" * 80)

        task_prompt = """Apply search filtering on server name or description; support tag-based filtering when server metadata includes tags. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: registry_registry_server, passing the
        # accumulated history so this step can see every prior step's output.
        result = await registry_registry_server.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_get_servers_from_registry
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_get_servers_from_registry")
        print("=" * 80)

        task_prompt = """Orchestrate fetching, post-processing, and filtering of servers for a given registryId and optional filters; return final server list or throw on error. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: registry_registry_server, passing the
        # accumulated history so this step can see every prior step's output.
        result = await registry_registry_server.run(task=history)
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