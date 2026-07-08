import asyncio

from team import (
    weather_agent,
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
        # Workflow Step: task_fetch_current_weather
        # Workflow Edge: task_fetch_current_weather -> task_fetch_current_weather
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_fetch_current_weather")
        print("=" * 80)

        task_prompt = """Fetch current weather data for the specified location using the weatherTool. If no location is provided, ask the user to supply one. Translate non-English location names to English before querying. Return concise but informative output including temperature, humidity, wind conditions, and precipitation. If asked for activity suggestions and forecast is available, include activity recommendations appropriate to the forecast. """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: weather_agent, passing the
        # accumulated history so this step can see every prior step's output.
        result = await weather_agent.run(task=history)
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