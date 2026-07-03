import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const TripPlannerAppTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
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
