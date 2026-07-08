import asyncio

from team import (
    player_white,
    player_black,
    board_proxy,
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
        # Workflow Step: task_initiate_chat
        # Workflow Edge: task_initiate_chat -> task_board_proxy_summary_to_white
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_initiate_chat")
        print("=" * 80)

        task_prompt = """让我们下棋吧，该你走了！ """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: player_black, passing the
        # accumulated history so this step can see every prior step's output.
        result = await player_black.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_board_proxy_summary_to_white
        # Workflow Edge: task_board_proxy_summary_to_white -> task_get_legal_moves
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_board_proxy_summary_to_white")
        print("=" * 80)

        task_prompt = """Summary of last board state and last move (provided by board proxy). """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: board_proxy, passing the
        # accumulated history so this step can see every prior step's output.
        result = await board_proxy.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_get_legal_moves
        # Workflow Edge: task_get_legal_moves -> task_make_move
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_get_legal_moves")
        print("=" * 80)

        task_prompt = """调用 get_legal_moves() 获取当前合法走法列表（UCI 格式）。 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: player_white, passing the
        # accumulated history so this step can see every prior step's output.
        result = await player_white.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_make_move
        # Workflow Edge: task_make_move -> task_check_made_move
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_make_move")
        print("=" * 80)

        task_prompt = """选择一个合法走法并调用 make_move(move) 来执行该步棋。 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: player_white, passing the
        # accumulated history so this step can see every prior step's output.
        result = await player_white.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_check_made_move
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_check_made_move")
        print("=" * 80)

        task_prompt = """Call check_made_move(msg) to determine if a move has been executed; if true, end nested chat iteration. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: board_proxy, passing the
        # accumulated history so this step can see every prior step's output.
        result = await board_proxy.run(task=history)
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