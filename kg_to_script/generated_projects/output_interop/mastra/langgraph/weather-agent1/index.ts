import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const UnnamedProjectAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_weather_tool
const tool_weather_tool = tool(
  async () => {
    return "Result of tool_weather_tool";
  },
  {
    name: "tool_weather_tool",
    description: "Tool to fetch current weather data for a specified location (current conditions: temperature, humidity, wind, precipitation).",
    schema: z.object({}),
  }
);



/**
 * Node: taskFetchCurrentWeather
 * Agent: weather_agent
 */
async function taskFetchCurrentWeather(state: typeof UnnamedProjectAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Weather Assistant." +
        "\n\nYour task: Fetch current weather data for the specified location using the weatherTool. If no location is provided, ask the user to supply one. Translate non-English location names to English before querying. Return concise but informative output including temperature, humidity, wind conditions, and precipitation. If asked for activity suggestions and forecast is available, include activity recommendations appropriate to the forecast." +
        "\nNode: taskFetchCurrentWeather",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(UnnamedProjectAnnotation)
  .addNode("taskFetchCurrentWeather", taskFetchCurrentWeather)
  .addEdge(START, "taskFetchCurrentWeather")
  .addEdge("taskFetchCurrentWeather", "taskFetchCurrentWeather")
;

export const graph = workflow.compile();
graph.name = "UnnamedProject";
// Workflow: workflow_weather_agent
