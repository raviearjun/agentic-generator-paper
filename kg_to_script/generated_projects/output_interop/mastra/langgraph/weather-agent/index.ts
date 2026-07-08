import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastrainstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_get_weather
const tool_get_weather = tool(
  async () => {
    return "Result of tool_get_weather";
  },
  {
    name: "tool_get_weather",
    description: "Get current weather for a location",
    schema: z.object({}),
  }
);



/**
 * Node: taskFetchWeather
 * Agent: weather_agent
 */
async function taskFetchWeather(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a weather assistant." +
        "\n\nYour task: Fetches weather forecast for a given city. Use triggerData.city as input to retrieve forecast data from the Open-Meteo APIs and return an array of daily forecast objects." +
        "\nNode: taskFetchWeather",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPlanActivities
 * Agent: weather_agent
 */
async function taskPlanActivities(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a weather assistant." +
        "\n\nYour task: You are a local activities and travel expert who excels at weather-based planning. Analyze the weather data and provide practical activity recommendations.\n\nFor each day in the forecast, structure your response exactly as follows:\n\n📅 [Day, Month Date, Year]\n═══════════════════════════\n\n🌡️ WEATHER SUMMARY\n• Conditions: [brief description]\n• Temperature: [X°C/Y°F to A°C/B°F]\n• Precipitation: [X% chance]\n\n🌅 MORNING ACTIVITIES\nOutdoor:\n• [Activity Name] - [Brief description including specific location/route]\n  Best timing: [specific time range]\n  Note: [relevant weather consideration]\n\n🌞 AFTERNOON ACTIVITIES\nOutdoor:\n• [Activity Name] - [Brief description including specific location/route]\n  Best timing: [specific time range]\n  Note: [relevant weather consideration]\n\n🏠 INDOOR ALTERNATIVES\n• [Activity Name] - [Brief description including specific venue]\n  Ideal for: [weather condition that would trigger this alternative]\n\n⚠️ SPECIAL CONSIDERATIONS\n• [Any relevant weather warnings, UV index, wind conditions, etc.]\n\nGuidelines:\n- Suggest 2-3 time-specific outdoor activities per day\n- Include 1-2 indoor backup options\n- For precipitation >50%, lead with indoor activities\n- All activities must be specific to the location\n- Include specific venues, trails, or locations\n- Consider activity intensity based on temperature\n- Keep descriptions concise but informative\n\nMaintain this exact formatting for consistency, using the emoji and section headers as shown." +
        "\nNode: taskPlanActivities",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastrainstanceAnnotation)
  .addNode("taskFetchWeather", taskFetchWeather)
  .addNode("taskPlanActivities", taskPlanActivities)
  .addEdge(START, "taskFetchWeather")
  .addEdge("taskFetchWeather", "taskPlanActivities")
  .addEdge("taskPlanActivities", END)
;

export const graph = workflow.compile();
graph.name = "mastrainstance";
// Workflow: workflow_weather_workflow
