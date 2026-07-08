import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const CodingandFinancialAnalysisCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_local_cli_executor
const tool_local_cli_executor = tool(
  async () => {
    return "Result of tool_local_cli_executor";
  },
  {
    name: "tool_local_cli_executor",
    description: "Executor used to run code locally with a working directory and timeout; can register functions to be callable during execution.",
    schema: z.object({}),
  }
);
// Tool: tool_get_stock_prices
const tool_get_stock_prices = tool(
  async () => {
    return "Result of tool_get_stock_prices";
  },
  {
    name: "tool_get_stock_prices",
    description: "Function that downloads stock prices using yfinance and returns closing prices for given symbols between start and end dates.",
    schema: z.object({}),
  }
);
// Tool: tool_plot_stock_prices
const tool_plot_stock_prices = tool(
  async () => {
    return "Result of tool_plot_stock_prices";
  },
  {
    name: "tool_plot_stock_prices",
    description: "Function that plots provided stock prices dataframe and saves the figure to a specified filename using matplotlib.",
    schema: z.object({}),
  }
);



/**
 * Node: taskPlotYtdV1
 * Agent: code_executor_agent
 */
async function taskPlotYtdV1(state: typeof CodingandFinancialAnalysisCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Code Executor." +
        "\n\nYour task: 今天是 {today}. 创建图表，显示 NVDA 和 TLSA 的股票收益。确保代码位于标记代码块中，并将图表保存到文件 ytd_stock_gains.png。" +
        "\nNode: taskPlotYtdV1",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPlotYtdV2
 * Agent: code_executor_agent
 */
async function taskPlotYtdV2(state: typeof CodingandFinancialAnalysisCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Code Executor." +
        "\n\nYour task: Today is {today}. Download the stock prices YTD for NVDA and TSLA and create a plot. Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png." +
        "\nNode: taskPlotYtdV2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(CodingandFinancialAnalysisCrewAnnotation)
  .addNode("taskPlotYtdV1", taskPlotYtdV1)
  .addNode("taskPlotYtdV2", taskPlotYtdV2)
  .addEdge(START, "taskPlotYtdV1")
  .addEdge("taskPlotYtdV1", "taskPlotYtdV2")
  .addEdge("taskPlotYtdV2", END)
;

export const graph = workflow.compile();
graph.name = "CodingandFinancialAnalysisCrew";
// Workflow: workflow_l5_coding_and_financial_analysis
