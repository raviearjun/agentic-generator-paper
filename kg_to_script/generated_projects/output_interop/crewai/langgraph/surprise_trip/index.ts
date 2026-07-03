import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const SurpriseTravelCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_serper_dev_tool
const tool_serper_dev_tool = tool(
  async () => {
    return "Result of tool_serper_dev_tool";
  },
  {
    name: "tool_serper_dev_tool",
    description: "Web search tool (Serper.dev) used to search the web for activities, restaurants, and general information.",
    schema: z.object({}),
  }
);
// Tool: tool_scrape_website_tool
const tool_scrape_website_tool = tool(
  async () => {
    return "Result of tool_scrape_website_tool";
  },
  {
    name: "tool_scrape_website_tool",
    description: "Tool used to scrape website content for details about venues, restaurants and events.",
    schema: z.object({}),
  }
);



/**
 * Node: taskPersonalizedActivityPlanningTask
 * Agent: personalized_activity_planner
 */
async function taskPersonalizedActivityPlanningTask(state: typeof SurpriseTravelCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Activity Planner." +
        "\nNode: taskPersonalizedActivityPlanningTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskRestaurantScenicLocationScoutTask
 * Agent: restaurant_scout
 */
async function taskRestaurantScenicLocationScoutTask(state: typeof SurpriseTravelCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Restaurant Scout." +
        "\nNode: taskRestaurantScenicLocationScoutTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskItineraryCompilationTask
 * Agent: itinerary_compiler
 */
async function taskItineraryCompilationTask(state: typeof SurpriseTravelCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Itinerary Compiler." +
        "\nNode: taskItineraryCompilationTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(SurpriseTravelCrewAnnotation)
  .addNode("taskPersonalizedActivityPlanningTask", taskPersonalizedActivityPlanningTask)
  .addNode("taskRestaurantScenicLocationScoutTask", taskRestaurantScenicLocationScoutTask)
  .addNode("taskItineraryCompilationTask", taskItineraryCompilationTask)
  .addEdge(START, "taskPersonalizedActivityPlanningTask")
  .addEdge("taskPersonalizedActivityPlanningTask", "taskRestaurantScenicLocationScoutTask")
  .addEdge("taskRestaurantScenicLocationScoutTask", "taskItineraryCompilationTask")
  .addEdge("taskItineraryCompilationTask", END)
;

export const graph = workflow.compile();
graph.name = "SurpriseTravelCrew";
// Workflow: workflow_sequential
