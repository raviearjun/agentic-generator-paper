import asyncio

from team import (
    openapi_spec_gen_agent,
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
        # Workflow Step: task_site_crawl_sync
        # Workflow Edge: task_site_crawl_sync -> task_generate_spec
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_site_crawl_sync")
        print("=" * 80)

        task_prompt = """Crawl the provided URL, extract main content as markdown, include sourceURL in metadata. Use provided pathRegex and limit. Exclude nav/header/footer and unrelated tags; return markdown blocks and metadata. """
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
        # Workflow Step: task_generate_spec
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_generate_spec")
        print("=" * 80)

        task_prompt = """I have generated the following Open API specs: <list of fragments>. Merge them into a single spec and ensure the result is a valid OpenAPI YAML document. Remove code fences and unify components/paths to avoid duplicates. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: openapi_spec_gen_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await openapi_spec_gen_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_add_to_github
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_add_to_github")
        print("=" * 80)

        task_prompt = """Can you take this text blob and format it into proper YAML? Ensure valid OpenAPI syntax and remove surrounding code fences. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: openapi_spec_gen_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await openapi_spec_gen_agent.run(task=history)
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