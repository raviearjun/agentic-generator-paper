import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const TripPlannerAppTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: book_accommodation_tool
const book_accommodation_tool = tool(
  async () => {
    return "Result of book_accommodation_tool";
  },
  {
    name: "book_accommodation_tool",
    description: "Tool invoked to create an accommodation booking using provided order details (accommodation, tripDetails). Tool call originates from LangGraph thread.submit messages in the UI.",
    schema: z.object({}),
  }
);



/**
 * Node: viewAccommodationsTask
 * Agent: trip_planner_agent
 */
async function viewAccommodationsTask(state: typeof TripPlannerAppTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Used by the trip planner LLM to format messages and construct tool calls for bookings." +
        "\n\nYour task: List available accommodations with images, ratings, price, and brief details. Allow the user to open details of an accommodation." +
        "\nNode: viewAccommodationsTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: selectAccommodationTask
 * Agent: trip_planner_agent
 */
async function selectAccommodationTask(state: typeof TripPlannerAppTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Used by the trip planner LLM to format messages and construct tool calls for bookings." +
        "\n\nYour task: When a user selects an accommodation, present full details (name, rating, price, dates, guests) and provide a booking action trigger." +
        "\nNode: selectAccommodationTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: confirmBookingTask
 * Agent: trip_planner_agent
 */
async function confirmBookingTask(state: typeof TripPlannerAppTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Used by the trip planner LLM to format messages and construct tool calls for bookings." +
        "\n\nYour task: Construct a JSON payload with fields { accommodation, tripDetails } and call the 'book-accommodation' tool. After tool invocation, provide a human-facing confirmation message describing the booked accommodation and trip summary." +
        "\nNode: confirmBookingTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: bookedConfirmationTask
 * Agent: trip_planner_agent
 */
async function bookedConfirmationTask(state: typeof TripPlannerAppTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Used by the trip planner LLM to format messages and construct tool calls for bookings." +
        "\n\nYour task: Show booked accommodation summary including dates, guest count, address/name, rating and total price. If tool response includes booking reference, display it." +
        "\nNode: bookedConfirmationTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(TripPlannerAppTeamAnnotation)
  .addNode("viewAccommodationsTask", viewAccommodationsTask)
  .addNode("selectAccommodationTask", selectAccommodationTask)
  .addNode("confirmBookingTask", confirmBookingTask)
  .addNode("bookedConfirmationTask", bookedConfirmationTask)
  .addEdge(START, "viewAccommodationsTask")
  .addEdge("viewAccommodationsTask", "selectAccommodationTask")
  .addEdge("selectAccommodationTask", "confirmBookingTask")
  .addEdge("confirmBookingTask", "bookedConfirmationTask")
  .addEdge("bookedConfirmationTask", END)
;

export const graph = workflow.compile();
graph.name = "TripPlannerAppTeam";
// Workflow: trip_planner_workflow
