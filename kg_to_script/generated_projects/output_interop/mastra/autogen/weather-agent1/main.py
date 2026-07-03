import asyncio

from team import (
    weather_agent,
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
        # Workflow Step: task_fetch_current_weather
        # Workflow Edge: task_fetch_current_weather -> task_fetch_current_weather
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_fetch_current_weather")
        print("=" * 80)

        task_prompt = """Fetch current weather data for the specified location using the weatherTool. If no location is provided, ask the user to supply one. Translate non-English location names to English before querying. Return concise but informative output including temperature, humidity, wind conditions, and precipitation. If asked for activity suggestions and forecast is available, include activity recommendations appropriate to the forecast. """
        # Execute via the assigned agent: weather_agent
        result = await weather_agent.run(task=task_prompt)

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