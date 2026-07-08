import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastraInstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: Available outboundFlight items will be provided. Select a single outbound flight based on travelForm (departureLocation, arrivalLocation, startDate, endDate) and flightPriority. ALWAYS pass entire date timestamps for departureTime and arrivalTime. Return ids (or flightNumber) and a short reasoning." +
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
        "\n\nYour task: Available returnFlight items will be provided. Select a single return flight based on travelForm and flightPriority. ALWAYS return full flight objects for outbound and return flights and timestamps." +
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
        "\n\nYour task: Given available hotels and the travelForm (arrivalCityId, hotelPriceRange), select up to 3 hotel options. Ignore 'reviewScore' and extract numeric rating from description/accessibility fields. Provide ids and reasoning." +
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
        "\n\nYour task: Given a set of attractions for the arrival city and the user's interests, select three attractions, provide brief reasoning, and include price, duration, and rating where available." +
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
        "\n\nYour task: Search for Airbnb location matches for the arrival city and select up to 3 unique place ids to be used in the subsequent Airbnb search. Provide ids and reasoning." +
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
        "\n\nYour task: Given Airbnb search results and travelForm (typeOfPlace, startDate, endDate), select up to 3 Airbnb options, then pick the top result to return. Provide ids and reasoning." +
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
        "\n\nYour task: Sync data from City CSV (src/data/city-data.csv). Read CSV rows, map columns to CityData, and call mastra.engine.syncRecords to sync City records. This step is executed by the Mastra engine runtime." +
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
