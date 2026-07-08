import asyncio

from team import (
    product_competitor_agent,
    strategy_planner_agent,
    creative_content_creator_agent,
    senior_photographer_agent,
    chief_creative_diretor_agent,
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
        # Workflow Step: task_product_analysis
        # Workflow Edge: task_product_analysis -> task_competitor_analysis
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_product_analysis")
        print("=" * 80)

        task_prompt = """Analyze the given product website: {product_website}.
Extra details provided by the customer: {product_details}.
Focus on identifying unique features, benefits, and the overall narrative. Provide a final report articulating key selling points, market appeal, and suggestions for enhancement or positioning. Attention to detail and up-to-date (2024) context required. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: product_competitor_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await product_competitor_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_competitor_analysis
        # Workflow Edge: task_competitor_analysis -> task_campaign_development
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_competitor_analysis")
        print("=" * 80)

        task_prompt = """Explore competitors of: {product_website}.
Extra details provided by the customer: {product_details}.
Identify the top 3 competitors and analyze their strategies, market positioning, and customer perception. Include context about the target website and detailed comparison. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: product_competitor_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await product_competitor_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_campaign_development
        # Workflow Edge: task_campaign_development -> task_instagram_ad_copy
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_campaign_development")
        print("=" * 80)

        task_prompt = """Create a targeted marketing campaign for: {product_website}.
Extra details provided by the customer: {product_details}.
Produce strategy and creative content ideas designed to captivate the target audience. Provide ideas that resonate with the audience and include all available product/context information. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: strategy_planner_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await strategy_planner_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_instagram_ad_copy
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_instagram_ad_copy")
        print("=" * 80)

        task_prompt = """Craft an engaging Instagram post copy. The copy should be punchy, captivating, concise, and aligned with the product marketing strategy. Focus on creating a message that resonates with the target audience and highlights the product's unique selling points. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: creative_content_creator_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await creative_content_creator_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_take_photograph
        # Workflow Edge: task_take_photograph -> task_review_photo
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_take_photograph")
        print("=" * 80)

        task_prompt = """You MUST take the most amazing photo ever for an instagram post regarding the product. Provided ad copy: {copy}
Product: {product_website}
Extra details: {product_details}
Imagine the photograph and describe it in a paragraph. Follow examples (professional wide shot, soft lighting, 4k, crisp, etc.). Do not show the actual product in photos. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_photographer_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_photographer_agent.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_review_photo
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_review_photo")
        print("=" * 80)

        task_prompt = """Review the photos from the senior photographer. Ensure alignment with product goals; review, approve, ask clarifying questions or delegate follow-up work as necessary. When delegating, include the full draft as part of the information.
Product: {product_website}
Extra details: {product_details}
Examples: (high tech airplane in a beautiful blue sky ...; the last supper ...; a bearded old man in the snows ...). """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: chief_creative_diretor_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await chief_creative_diretor_agent.run(task=history)
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