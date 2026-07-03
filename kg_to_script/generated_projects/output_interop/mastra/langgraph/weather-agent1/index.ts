import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const UnnamedProjectAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
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
