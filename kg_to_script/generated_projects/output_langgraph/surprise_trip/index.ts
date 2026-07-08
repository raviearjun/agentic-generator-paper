import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const SurpriseTravelCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: Research and find cool things to do at {destination}. Focus on activities and events that match the traveler's interests and age group. Utilize internet search tools and recommendation engines to gather the information.\n\nTraveler's information:\n- origin: {origin}\n- destination: {destination}\n- age of the traveler: {age}\n- hotel localtion: {hotel_location}\n- flight infromation: {flight_information}\n- how long is the trip: {trip_duration}" +
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
        "\n\nYour task: Find highly-rated restaurants and dining experiences at {destination}. Recommend scenic locations and fun activities that align with the traveler's preferences. Use internet search tools, restaurant review sites, and travel guides.\n\nTraveler's information:\n- origin: {origin}\n- destination: {destination}\n- age of the traveler: {age}\n- hotel localtion: {hotel_location}\n- flight infromation: {flight_information}\n- how long is the trip: {trip_duration}" +
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
        "\n\nYour task: Compile all researched information into a comprehensive day-by-day itinerary for the trip to {destination}. Ensure the itinerary integrates flights, hotel information, and all planned activities and dining experiences. Use text formatting and document creation tools to organize the information." +
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
