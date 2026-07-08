import { ChatAnthropic } from "@langchain/anthropic";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const OrderPizzaGraphTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: find_pizza_tool
const find_pizza_tool = tool(
  async () => {
    return "Result of find_pizza_tool";
  },
  {
    name: "find_pizza_tool",
    description: "Tool invoked to search for a pizza shop and return address and phone number.",
    schema: z.object({}),
  }
);
// Tool: place_order_tool
const place_order_tool = tool(
  async () => {
    return "Result of place_order_tool";
  },
  {
    name: "place_order_tool",
    description: "Tool invoked to place a pizza order and confirm success.",
    schema: z.object({}),
  }
);



/**
 * Node: findStoreTask
 * Agent: langgraph_anthropic_agent
 */
async function findStoreTask(state: typeof OrderPizzaGraphTeamAnnotation.State) {
  const model = new ChatAnthropic({ model: "claude-3-5-sonnet-latest" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: You are a helpful AI assistant, tasked with extracting information from the conversation between you, and the user, in order to find a pizza shop for them." +
        "\nNode: findStoreTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: orderPizzaTask
 * Agent: langgraph_anthropic_agent
 */
async function orderPizzaTask(state: typeof OrderPizzaGraphTeamAnnotation.State) {
  const model = new ChatAnthropic({ model: "claude-3-5-sonnet-latest" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\n\nYour task: You are a helpful AI assistant, tasked with placing an order for a pizza for the user." +
        "\nNode: orderPizzaTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(OrderPizzaGraphTeamAnnotation)
  .addNode("findStoreTask", findStoreTask)
  .addNode("orderPizzaTask", orderPizzaTask)
  .addEdge(START, "findStoreTask")
  .addEdge("findStoreTask", "orderPizzaTask")
  .addEdge("orderPizzaTask", END)
;

export const graph = workflow.compile();
graph.name = "OrderPizzaGraphTeam";
// Workflow: order_pizza_state_graph
