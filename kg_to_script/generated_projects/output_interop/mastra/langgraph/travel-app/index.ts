import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastraInstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_search_flights
const tool_search_flights = tool(
  async () => {
    return "Result of tool_search_flights";
  },
  {
    name: "tool_search_flights",
    description: "Fetches flight information for a given date range, origin and destination. Origin and Destination are Airport codes like DFW.AIRPORT or SEA.AIRPORT",
    schema: z.object({}),
  }
);
// Tool: tool_search_hotels
const tool_search_hotels = tool(
  async () => {
    return "Result of tool_search_hotels";
  },
  {
    name: "tool_search_hotels",
    description: "Searches for hotels in a specified location. Destination is a cityId like 20015732 for 20015733",
    schema: z.object({}),
  }
);
// Tool: tool_search_attractions
const tool_search_attractions = tool(
  async () => {
    return "Result of tool_search_attractions";
  },
  {
    name: "tool_search_attractions",
    description: "Searches for attractions in a specified location. Destination is a cityId like 20015732 for 20015733",
    schema: z.object({}),
  }
);
// Tool: tool_search_airbnb_location
const tool_search_airbnb_location = tool(
  async () => {
    return "Result of tool_search_airbnb_location";
  },
  {
    name: "tool_search_airbnb_location",
    description: "Searches for Airbnb places in a specified location. Place is a city name like New York, NY",
    schema: z.object({}),
  }
);
// Tool: tool_search_airbnb
const tool_search_airbnb = tool(
  async () => {
    return "Result of tool_search_airbnb";
  },
  {
    name: "tool_search_airbnb",
    description: "Searches for Airbnb in a specified location. Place is a cityId like 20015732 for 20015733",
    schema: z.object({}),
  }
);



/**
 * Node: taskOutboundFlight
 * Agent: travel_analyzer
 */
async function taskOutboundFlight(state: typeof MastraInstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a travel analyzer." +
        "\nNode: taskOutboundFlight",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskReturnFlight
 * Agent: travel_analyzer
 */
async function taskReturnFlight(state: typeof MastraInstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a travel analyzer." +
        "\nNode: taskReturnFlight",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskAccommodationHotels
 * Agent: travel_analyzer
 */
async function taskAccommodationHotels(state: typeof MastraInstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a travel analyzer." +
        "\nNode: taskAccommodationHotels",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskAttraction
 * Agent: travel_analyzer
 */
async function taskAttraction(state: typeof MastraInstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a travel analyzer." +
        "\nNode: taskAttraction",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskAirbnbLocation
 * Agent: travel_analyzer
 */
async function taskAirbnbLocation(state: typeof MastraInstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a travel analyzer." +
        "\nNode: taskAirbnbLocation",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskAccommodationAirbnb
 * Agent: travel_analyzer
 */
async function taskAccommodationAirbnb(state: typeof MastraInstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a travel analyzer." +
        "\nNode: taskAccommodationAirbnb",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskSyncCsvData
 * Agent: travel_analyzer
 */
async function taskSyncCsvData(state: typeof MastraInstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a travel analyzer." +
        "\nNode: taskSyncCsvData",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastraInstanceAnnotation)
  .addNode("taskOutboundFlight", taskOutboundFlight)
  .addNode("taskReturnFlight", taskReturnFlight)
  .addNode("taskAccommodationHotels", taskAccommodationHotels)
  .addNode("taskAttraction", taskAttraction)
  .addNode("taskAirbnbLocation", taskAirbnbLocation)
  .addNode("taskAccommodationAirbnb", taskAccommodationAirbnb)
  .addNode("taskSyncCsvData", taskSyncCsvData)
  .addEdge(START, "taskOutboundFlight")
  .addEdge("taskReturnFlight", "taskAccommodationHotels")
  .addEdge("taskAccommodationHotels", "taskAttraction")
  .addEdge("taskAttraction", "taskAirbnbLocation")
  .addEdge("taskAirbnbLocation", "taskAccommodationAirbnb")
  .addEdge("taskOutboundFlight", END)
  .addEdge("taskAccommodationAirbnb", END)
  .addEdge("taskSyncCsvData", END)
;

export const graph = workflow.compile();
graph.name = "MastraInstance";
// Workflow: workflow_travel_submission
// Workflow: workflow_sync_csv_data
