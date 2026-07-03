import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const TradingSystemAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: buy_stock_tool
const buy_stock_tool = tool(
  async () => {
    return "Result of buy_stock_tool";
  },
  {
    name: "buy_stock_tool",
    description: "Executes stock purchase orders when invoked by the UI. Expects a JSON content with purchaseDetails { ticker, quantity, price }.",
    schema: z.object({}),
  }
);



/**
 * Node: openBuyUiTask
 * Agent: trade_agent
 */
async function openBuyUiTask(state: typeof TradingSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a trading_assistant." +
        "\nNode: openBuyUiTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: executePurchaseTask
 * Agent: trade_agent
 */
async function executePurchaseTask(state: typeof TradingSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a trading_assistant." +
        "\nNode: executePurchaseTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: confirmPurchaseTask
 * Agent: trade_agent
 */
async function confirmPurchaseTask(state: typeof TradingSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a trading_assistant." +
        "\nNode: confirmPurchaseTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(TradingSystemAnnotation)
  .addNode("openBuyUiTask", openBuyUiTask)
  .addNode("executePurchaseTask", executePurchaseTask)
  .addNode("confirmPurchaseTask", confirmPurchaseTask)
  .addEdge(START, "openBuyUiTask")
  .addEdge("openBuyUiTask", "executePurchaseTask")
  .addEdge("executePurchaseTask", "confirmPurchaseTask")
  .addEdge("confirmPurchaseTask", END)
;

export const graph = workflow.compile();
graph.name = "TradingSystem";
// Workflow: buy_stock_workflow
