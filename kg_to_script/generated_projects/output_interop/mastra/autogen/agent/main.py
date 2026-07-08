import asyncio

from team import (
    chef_agent,
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
        # Workflow Step: task_query_pantry
        # Workflow Edge: task_query_pantry -> task_generate_text
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_query_pantry")
        print("=" * 80)

        task_prompt = """In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make? """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_generate_text
        # Workflow Edge: task_generate_text -> task_text_stream
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_generate_text")
        print("=" * 80)

        task_prompt = """In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make? """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_text_stream
        # Workflow Edge: task_text_stream -> task_generate_stream
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_text_stream")
        print("=" * 80)

        task_prompt = """Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_generate_stream
        # Workflow Edge: task_generate_stream -> task_text_object
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_generate_stream")
        print("=" * 80)

        task_prompt = """Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_text_object
        # Workflow Edge: task_text_object -> task_text_object_jsonschema
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_text_object")
        print("=" * 80)

        task_prompt = """I want to make lasagna, can you generate a lasagna recipe for me? """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_text_object_jsonschema
        # Workflow Edge: task_text_object_jsonschema -> task_generate_object
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_text_object_jsonschema")
        print("=" * 80)

        task_prompt = """I want to make lasagna, can you generate a lasagna recipe for me? """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_generate_object
        # Workflow Edge: task_generate_object -> task_stream_object
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_generate_object")
        print("=" * 80)

        task_prompt = """I want to make lasagna, can you generate a lasagna recipe for me? """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_stream_object
        # Workflow Edge: task_stream_object -> task_generate_stream_object
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_stream_object")
        print("=" * 80)

        task_prompt = """I want to make lasagna, can you generate a lasagna recipe for me? """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_generate_stream_object
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_generate_stream_object")
        print("=" * 80)

        task_prompt = """I want to make lasagna, can you generate a lasagna recipe for me? """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chef_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chef_agent.run(task=history)
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