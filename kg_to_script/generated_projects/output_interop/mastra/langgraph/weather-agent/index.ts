import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastrainstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
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
