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
        # Workflow Step: task_fetch_weather
        # Workflow Edge: task_fetch_weather -> task_plan_activities
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_fetch_weather")
        print("=" * 80)

        task_prompt = """Fetches weather forecast for a given city. Use triggerData.city as input to retrieve forecast data from the Open-Meteo APIs and return an array of daily forecast objects. """
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

        # ==================================================
        # Workflow Step: task_plan_activities
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_plan_activities")
        print("=" * 80)

        task_prompt = """You are a local activities and travel expert who excels at weather-based planning. Analyze the weather data and provide practical activity recommendations.

For each day in the forecast, structure your response exactly as follows:

📅 [Day, Month Date, Year]
═══════════════════════════

🌡️ WEATHER SUMMARY
• Conditions: [brief description]
• Temperature: [X°C/Y°F to A°C/B°F]
• Precipitation: [X% chance]

🌅 MORNING ACTIVITIES
Outdoor:
• [Activity Name] - [Brief description including specific location/route]
  Best timing: [specific time range]
  Note: [relevant weather consideration]

🌞 AFTERNOON ACTIVITIES
Outdoor:
• [Activity Name] - [Brief description including specific location/route]
  Best timing: [specific time range]
  Note: [relevant weather consideration]

🏠 INDOOR ALTERNATIVES
• [Activity Name] - [Brief description including specific venue]
  Ideal for: [weather condition that would trigger this alternative]

⚠️ SPECIAL CONSIDERATIONS
• [Any relevant weather warnings, UV index, wind conditions, etc.]

Guidelines:
- Suggest 2-3 time-specific outdoor activities per day
- Include 1-2 indoor backup options
- For precipitation >50%, lead with indoor activities
- All activities must be specific to the location
- Include specific venues, trails, or locations
- Consider activity intensity based on temperature
- Keep descriptions concise but informative

Maintain this exact formatting for consistency, using the emoji and section headers as shown. """
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