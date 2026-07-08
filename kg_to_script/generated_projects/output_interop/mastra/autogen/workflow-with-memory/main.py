import asyncio

from team import (
    cat_one,
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
        # Workflow Step: task_step_one
        # Workflow Edge: task_step_one -> task_step_two
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_step_one")
        print("=" * 80)

        task_prompt = """Doubles the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_step_two
        # Workflow Edge: task_step_two -> task_step_three
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_step_two")
        print("=" * 80)

        task_prompt = """Adds 1 to the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_step_three
        # Workflow Edge: task_step_three -> task_step_four
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_step_three")
        print("=" * 80)

        task_prompt = """Squares the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_step_four
        # Workflow Edge: task_step_four -> task_step_five
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_step_four")
        print("=" * 80)

        task_prompt = """Gives the square root of the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_step_five
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_step_five")
        print("=" * 80)

        task_prompt = """Triples the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_par_step_one
        # Workflow Edge: task_par_step_one -> task_par_step_six
        # Workflow Edge: task_par_step_one -> task_par_step_two
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_par_step_one")
        print("=" * 80)

        task_prompt = """Doubles the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_par_step_six
        # Workflow Edge: task_par_step_six -> task_par_step_two
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_par_step_six")
        print("=" * 80)

        task_prompt = """Logs the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_par_step_two
        # Workflow Edge: task_par_step_two -> task_par_step_three
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_par_step_two")
        print("=" * 80)

        task_prompt = """Adds 1 to the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_par_step_three
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_par_step_three")
        print("=" * 80)

        task_prompt = """Squares the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_br_step_one
        # Workflow Edge: task_br_step_one -> task_br_step_two
        # Workflow Edge: task_br_step_one -> task_br_step_three
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_br_step_one")
        print("=" * 80)

        task_prompt = """Doubles the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_br_step_two
        # Workflow Edge: task_br_step_two -> task_br_step_four
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_br_step_two")
        print("=" * 80)

        task_prompt = """Adds 1 to the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_br_step_four
        # Workflow Edge: task_br_step_four -> task_br_step_three
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_br_step_four")
        print("=" * 80)

        task_prompt = """Gives the square root of the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_br_step_three
        # Workflow Edge: task_br_step_three -> task_br_step_five
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_br_step_three")
        print("=" * 80)

        task_prompt = """Squares the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_br_step_five
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_br_step_five")
        print("=" * 80)

        task_prompt = """Triples the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_cyc_step_one
        # Workflow Edge: task_cyc_step_one -> task_cyc_step_two
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_cyc_step_one")
        print("=" * 80)

        task_prompt = """Doubles the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_cyc_step_two
        # Workflow Edge: task_cyc_step_two -> task_cyc_step_three
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_cyc_step_two")
        print("=" * 80)

        task_prompt = """Adds 1 to the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_cyc_step_three
        # Workflow Edge: task_cyc_step_three -> task_cyc_step_one_loop
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_cyc_step_three")
        print("=" * 80)

        task_prompt = """Squares the input value """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_cyc_step_one_loop
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_cyc_step_one_loop")
        print("=" * 80)

        task_prompt = """Doubles the input value (loop invocation) """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: cat_one, passing the
        # accumulated history so this step can see every prior step's output.
        result = await cat_one.run(task=history)
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