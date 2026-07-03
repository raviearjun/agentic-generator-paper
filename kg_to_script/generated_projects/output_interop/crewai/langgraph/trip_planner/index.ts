import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const TripPlannerCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_search
const tool_search = tool(
  async () => {
    return "Result of tool_search";
  },
  {
    name: "tool_search",
    description: "Search the internet using Serper (google.serper.dev) and return top results.",
    schema: z.object({}),
  }
);
// Tool: tool_browser
const tool_browser = tool(
  async () => {
    return "Result of tool_browser";
  },
  {
    name: "tool_browser",
    description: "Scrape website content via browserless and summarize chunks using an internal Agent/Task.",
    schema: z.object({}),
  }
);
// Tool: tool_calculator
const tool_calculator = tool(
  async () => {
    return "Result of tool_calculator";
  },
  {
    name: "tool_calculator",
    description: "Safe mathematical expression evaluator implemented with ast and restricted operators.",
    schema: z.object({}),
  }
);



/**
 * Node: taskIdentifyCity
 * Agent: city_selection_agent
 */
async function taskIdentifyCity(state: typeof TripPlannerCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a City Selection Expert." +
        "\nNode: taskIdentifyCity",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGatherCityInfo
 * Agent: local_expert_agent
 */
async function taskGatherCityInfo(state: typeof TripPlannerCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Local Expert at this city." +
        "\nNode: taskGatherCityInfo",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPlanItinerary
 * Agent: travel_concierge_agent
 */
async function taskPlanItinerary(state: typeof TripPlannerCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Amazing Travel Concierge." +
        "\nNode: taskPlanItinerary",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(TripPlannerCrewAnnotation)
  .addNode("taskIdentifyCity", taskIdentifyCity)
  .addNode("taskGatherCityInfo", taskGatherCityInfo)
  .addNode("taskPlanItinerary", taskPlanItinerary)
  .addEdge(START, "taskIdentifyCity")
  .addEdge("taskIdentifyCity", "taskGatherCityInfo")
  .addEdge("taskGatherCityInfo", "taskPlanItinerary")
  .addEdge("taskPlanItinerary", END)
;

export const graph = workflow.compile();
graph.name = "TripPlannerCrew";
// Workflow: pattern_trip_planning
