import asyncio

from team import (
    unnamed_writer,
    unnamed_critic,
    unnamed_seo,
    unnamed_legal,
    unnamed_ethics,
    unnamed_meta,
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
        # Workflow Step: task_write_blog
        # Workflow Edge: task_write_blog -> task_critic_initiate_1
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_write_blog")
        print("=" * 80)

        task_prompt = """撰写一篇简洁但引人入胜的博客，内容涉及
       DeepLearning.AI. 确保博客100 字以内。 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed_writer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed_writer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_critic_initiate_1
        # Workflow Edge: task_critic_initiate_1 -> task_nested_seo_review
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_critic_initiate_1")
        print("=" * 80)

        task_prompt = """撰写一篇简洁但引人入胜的博客，内容涉及
       DeepLearning.AI. 确保博客100 字以内。 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed_critic, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed_critic.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_nested_seo_review
        # Workflow Edge: task_nested_seo_review -> task_nested_legal_review
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_nested_seo_review")
        print("=" * 80)

        task_prompt = """仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}. 这里的 审查员 应该是你自己的角色 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed_seo, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed_seo.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_nested_legal_review
        # Workflow Edge: task_nested_legal_review -> task_nested_ethics_review
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_nested_legal_review")
        print("=" * 80)

        task_prompt = """仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed_legal, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed_legal.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_nested_ethics_review
        # Workflow Edge: task_nested_ethics_review -> task_meta_aggregate
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_nested_ethics_review")
        print("=" * 80)

        task_prompt = """仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed_ethics, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed_ethics.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_meta_aggregate
        # Workflow Edge: task_meta_aggregate -> task_critic_initiate_2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_meta_aggregate")
        print("=" * 80)

        task_prompt = """对所有审查员的反馈意见进行汇总，并对写作提出最终建议。 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed_meta, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed_meta.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_critic_initiate_2
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_critic_initiate_2")
        print("=" * 80)

        task_prompt = """撰写一篇简洁但引人入胜的博客，内容涉及
       DeepLearning.AI. 确保博客100 字以内。 """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: unnamed_critic, passing the
        # accumulated history so this step can see every prior step's output.
        result = await unnamed_critic.run(task=history)
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