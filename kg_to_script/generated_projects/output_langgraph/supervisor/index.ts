import { StateGraph, START, END } from "@langchain/langgraph";
import { SupervisorAnnotation, type SupervisorState } from "./types";
import { router } from "./nodes/router";
import { generalInput } from "./nodes/general-input";
import { ChatOpenAI } from "@langchain/openai";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

// Tool: tool_stockbroker
const tool_stockbroker = tool(
  async () => {
    return "Result of tool_stockbroker";
  },
  {
    name: "tool_stockbroker",
    description: "can fetch the price of a ticker, purchase/sell a ticker, or get the user's portfolio",
    schema: z.object({}),
  }
);
// Tool: tool_trip_planner
const tool_trip_planner = tool(
  async () => {
    return "Result of tool_trip_planner";
  },
  {
    name: "tool_trip_planner",
    description: "helps the user plan their trip; can suggest restaurants and places to stay in any given location.",
    schema: z.object({}),
  }
);
// Tool: tool_open_code
const tool_open_code = tool(
  async () => {
    return "Result of tool_open_code";
  },
  {
    name: "tool_open_code",
    description: "can write a React TODO app for the user. Only call this tool if they request a TODO app.",
    schema: z.object({}),
  }
);
// Tool: tool_order_pizza
const tool_order_pizza = tool(
  async () => {
    return "Result of tool_order_pizza";
  },
  {
    name: "tool_order_pizza",
    description: "can order a pizza for the user",
    schema: z.object({}),
  }
);
// Tool: tool_writer_agent
const tool_writer_agent = tool(
  async () => {
    return "Result of tool_writer_agent";
  },
  {
    name: "tool_writer_agent",
    description: "can write a text document for the user. Only call this tool if they request a text document.",
    schema: z.object({}),
  }
);
// Tool: tool_router
const tool_router = tool(
  async () => {
    return "Result of tool_router";
  },
  {
    name: "tool_router",
    description: "A tool to route the user's query to the appropriate tool. (Used as a tool schema bound to the routing model)",
    schema: z.object({}),
  }
);


/**
 * Route Target Node: taskStockbroker
 * Agent: supervisor
 */
async function taskStockbroker(state: SupervisorState) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Route: taskStockbroker. You are a supervisor." +
        "",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Route Target Node: taskTripPlanner
 * Agent: supervisor
 */
async function taskTripPlanner(state: SupervisorState) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Route: taskTripPlanner. You are a supervisor." +
        "",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Route Target Node: taskOpenCode
 * Agent: supervisor
 */
async function taskOpenCode(state: SupervisorState) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Route: taskOpenCode. You are a supervisor." +
        "",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Route Target Node: taskOrderPizza
 * Agent: supervisor
 */
async function taskOrderPizza(state: SupervisorState) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Route: taskOrderPizza. You are a supervisor." +
        "",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Route Target Node: taskWriterAgent
 * Agent: supervisor
 */
async function taskWriterAgent(state: SupervisorState) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "Route: taskWriterAgent. You are a supervisor." +
        "",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

function handleRoute(state: SupervisorState):
  | "taskStockbroker"
  | "taskTripPlanner"
  | "taskOpenCode"
  | "taskOrderPizza"
  | "taskGeneralInput"
  | "taskWriterAgent"
{
  return state.next as
    | "taskStockbroker"
    | "taskTripPlanner"
    | "taskOpenCode"
    | "taskOrderPizza"
    | "taskGeneralInput"
    | "taskWriterAgent"
  ;
}

const builder = new StateGraph(SupervisorAnnotation)
  .addNode("taskRouter", router)
  .addNode("taskStockbroker", taskStockbroker)
  .addNode("taskTripPlanner", taskTripPlanner)
  .addNode("taskOpenCode", taskOpenCode)
  .addNode("taskOrderPizza", taskOrderPizza)
  .addNode("taskGeneralInput", generalInput)
  .addNode("taskWriterAgent", taskWriterAgent)
  .addConditionalEdges("taskRouter", handleRoute, [
    "taskStockbroker",
    "taskTripPlanner",
    "taskOpenCode",
    "taskOrderPizza",
    "taskGeneralInput",
    "taskWriterAgent",
  ])
  .addEdge(START, "taskRouter")
  .addEdge("taskStockbroker", END)
  .addEdge("taskTripPlanner", END)
  .addEdge("taskOpenCode", END)
  .addEdge("taskOrderPizza", END)
  .addEdge("taskGeneralInput", END)
  .addEdge("taskWriterAgent", END)
;

export const graph = builder.compile();
graph.name = "GenerativeUIAgent";
// Workflow: stategraph_workflow
