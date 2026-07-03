import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastrainstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: stock_prices_tool
const stock_prices_tool = tool(
  async () => {
    return "Result of stock_prices_tool";
  },
  {
    name: "stock_prices_tool",
    description: "Fetches the last day's closing stock price for a given symbol",
    schema: z.object({}),
  }
);



/**
 * Node: taskInit
 * Agent: stock_agent
 */
async function taskInit(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\nNode: taskInit",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskQuery
 * Agent: stock_agent
 */
async function taskQuery(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\nNode: taskQuery",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskToolCall
 * Agent: stock_agent
 */
async function taskToolCall(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\nNode: taskToolCall",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskEnd
 * Agent: stock_agent
 */
async function taskEnd(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\nNode: taskEnd",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastrainstanceAnnotation)
  .addNode("taskInit", taskInit)
  .addNode("taskQuery", taskQuery)
  .addNode("taskToolCall", taskToolCall)
  .addNode("taskEnd", taskEnd)
  .addEdge(START, "taskInit")
  .addEdge("taskInit", "taskQuery")
  .addEdge("taskQuery", "taskToolCall")
  .addEdge("taskToolCall", "taskEnd")
  .addEdge("taskEnd", END)
;

export const graph = workflow.compile();
graph.name = "mastrainstance";
// Workflow: stock_workflow
