import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const TripPlannerCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: Analyze and select the best city for the trip based\non specific criteria such as weather patterns, seasonal\nevents, and travel costs. This task involves comparing\nmultiple cities, considering factors like current weather\nconditions, upcoming cultural or seasonal events, and\noverall travel expenses.\n\nYour final answer must be a detailed\nreport on the chosen city, and everything you found out\nabout it, including the actual flight costs, weather\nforecast and attractions.\nIf you do your BEST WORK, I'll tip you $100!\n\nTraveling from: {origin}\nCity Options: {cities}\nTrip Date: {range}\nTraveler Interests: {interests}" +
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
        "\n\nYour task: As a local expert on this city you must compile an\nin-depth guide for someone traveling there and wanting\nto have THE BEST trip ever!\nGather information about key attractions, local customs,\nspecial events, and daily activity recommendations.\nFind the best spots to go to, the kind of place only a\nlocal would know.\nThis guide should provide a thorough overview of what\nthe city has to offer, including hidden gems, cultural\nhotspots, must-visit landmarks, weather forecasts, and\nhigh level costs.\n\nThe final answer must be a comprehensive city guide,\nrich in cultural insights and practical tips,\ntailored to enhance the travel experience.\nIf you do your BEST WORK, I'll tip you $100!\n\nTrip Date: {range}\nTraveling from: {origin}\nTraveler Interests: {interests}" +
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
        "\n\nYour task: Expand this guide into a full 7-day travel\nitinerary with detailed per-day plans, including\nweather forecasts, places to eat, packing suggestions,\nand a budget breakdown.\n\nYou MUST suggest actual places to visit, actual hotels\nto stay and actual restaurants to go to.\n\nThis itinerary should cover all aspects of the trip,\nfrom arrival to departure, integrating the city guide\ninformation with practical travel logistics.\n\nYour final answer MUST be a complete expanded travel plan,\nformatted as markdown, encompassing a daily schedule,\nanticipated weather conditions, recommended clothing and\nitems to pack, and a detailed budget, ensuring THE BEST\nTRIP EVER. Be specific and give it a reason why you picked\neach place, what makes them special! If you do your BEST WORK, I'll tip you $100!\n\nTrip Date: {range}\nTraveling from: {origin}\nTraveler Interests: {interests}" +
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
