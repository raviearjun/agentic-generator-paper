import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const StockAnalysisCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_calculator_tool
const tool_calculator_tool = tool(
  async () => {
    return "Result of tool_calculator_tool";
  },
  {
    name: "tool_calculator_tool",
    description: "Performs safe mathematical expression evaluation (add, sub, mul, div, pow, mod).",
    schema: z.object({}),
  }
);
// Tool: tool_scrape_website_tool
const tool_scrape_website_tool = tool(
  async () => {
    return "Result of tool_scrape_website_tool";
  },
  {
    name: "tool_scrape_website_tool",
    description: "Tool to scrape website content and convert to text for summarization.",
    schema: z.object({}),
  }
);
// Tool: tool_website_search_tool
const tool_website_search_tool = tool(
  async () => {
    return "Result of tool_website_search_tool";
  },
  {
    name: "tool_website_search_tool",
    description: "Tool to search the web for relevant pages and summaries.",
    schema: z.object({}),
  }
);
// Tool: tool_txt_search_tool
const tool_txt_search_tool = tool(
  async () => {
    return "Result of tool_txt_search_tool";
  },
  {
    name: "tool_txt_search_tool",
    description: "Text search tool for searching indexed textual data.",
    schema: z.object({}),
  }
);
// Tool: tool_sec10_k_tool_generic
const tool_sec10_k_tool_generic = tool(
  async () => {
    return "Result of tool_sec10_k_tool_generic";
  },
  {
    name: "tool_sec10_k_tool_generic",
    description: "A tool to semantically search a company's latest 10-K SEC filing content.",
    schema: z.object({}),
  }
);
// Tool: tool_sec10_q_tool_generic
const tool_sec10_q_tool_generic = tool(
  async () => {
    return "Result of tool_sec10_q_tool_generic";
  },
  {
    name: "tool_sec10_q_tool_generic",
    description: "A tool to semantically search a company's latest 10-Q SEC filing content.",
    schema: z.object({}),
  }
);
// Tool: tool_sec10_k_tool_amzn
const tool_sec10_k_tool_amzn = tool(
  async () => {
    return "Result of tool_sec10_k_tool_amzn";
  },
  {
    name: "tool_sec10_k_tool_amzn",
    description: "SEC10KTool initialized with stock_name=AMZN to pre-load AMZN latest 10-K content.",
    schema: z.object({}),
  }
);
// Tool: tool_sec10_q_tool_amzn
const tool_sec10_q_tool_amzn = tool(
  async () => {
    return "Result of tool_sec10_q_tool_amzn";
  },
  {
    name: "tool_sec10_q_tool_amzn",
    description: "SEC10QTool initialized with stock_name=AMZN to pre-load AMZN latest 10-Q content.",
    schema: z.object({}),
  }
);



/**
 * Node: taskFinancialAnalysis
 * Agent: financial_analyst_agent
 */
async function taskFinancialAnalysis(state: typeof StockAnalysisCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a The Best Financial Analyst." +
        "\nNode: taskFinancialAnalysis",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskResearch
 * Agent: research_analyst_agent
 */
async function taskResearch(state: typeof StockAnalysisCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Staff Research Analyst." +
        "\nNode: taskResearch",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskFilingsAnalysis
 * Agent: financial_analyst_agent
 */
async function taskFilingsAnalysis(state: typeof StockAnalysisCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a The Best Financial Analyst." +
        "\nNode: taskFilingsAnalysis",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskRecommend
 * Agent: investment_advisor_agent
 */
async function taskRecommend(state: typeof StockAnalysisCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Private Investment Advisor." +
        "\nNode: taskRecommend",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(StockAnalysisCrewAnnotation)
  .addNode("taskFinancialAnalysis", taskFinancialAnalysis)
  .addNode("taskResearch", taskResearch)
  .addNode("taskFilingsAnalysis", taskFilingsAnalysis)
  .addNode("taskRecommend", taskRecommend)
  .addEdge(START, "taskFinancialAnalysis")
  .addEdge("taskFinancialAnalysis", "taskResearch")
  .addEdge("taskResearch", "taskFilingsAnalysis")
  .addEdge("taskFilingsAnalysis", "taskRecommend")
  .addEdge("taskRecommend", END)
;

export const graph = workflow.compile();
graph.name = "StockAnalysisCrew";
// Workflow: workflow_stock_analysis
