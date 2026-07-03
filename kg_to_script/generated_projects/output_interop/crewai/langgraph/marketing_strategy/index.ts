import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MarketingPostsCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_serper_dev_tool
const tool_serper_dev_tool = tool(
  async () => {
    return "Result of tool_serper_dev_tool";
  },
  {
    name: "tool_serper_dev_tool",
    description: "Tool for performing web/search queries via Serper.dev (used to find up-to-date information).",
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
    description: "Tool to scrape website content for extracting information about customers and competitors.",
    schema: z.object({}),
  }
);



/**
 * Node: taskResearch
 * Agent: lead_market_analyst
 */
async function taskResearch(state: typeof MarketingPostsCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Lead Market Analyst." +
        "\nNode: taskResearch",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskProjectUnderstanding
 * Agent: chief_marketing_strategist
 */
async function taskProjectUnderstanding(state: typeof MarketingPostsCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chief Marketing Strategist." +
        "\nNode: taskProjectUnderstanding",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskMarketingStrategy
 * Agent: chief_marketing_strategist
 */
async function taskMarketingStrategy(state: typeof MarketingPostsCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chief Marketing Strategist." +
        "\nNode: taskMarketingStrategy",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCampaignIdea
 * Agent: creative_content_creator
 */
async function taskCampaignIdea(state: typeof MarketingPostsCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Creative Content Creator." +
        "\nNode: taskCampaignIdea",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCopyCreation
 * Agent: creative_content_creator
 */
async function taskCopyCreation(state: typeof MarketingPostsCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Creative Content Creator." +
        "\nNode: taskCopyCreation",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MarketingPostsCrewAnnotation)
  .addNode("taskResearch", taskResearch)
  .addNode("taskProjectUnderstanding", taskProjectUnderstanding)
  .addNode("taskMarketingStrategy", taskMarketingStrategy)
  .addNode("taskCampaignIdea", taskCampaignIdea)
  .addNode("taskCopyCreation", taskCopyCreation)
  .addEdge(START, "taskResearch")
  .addEdge("taskResearch", "taskProjectUnderstanding")
  .addEdge("taskProjectUnderstanding", "taskMarketingStrategy")
  .addEdge("taskMarketingStrategy", "taskCampaignIdea")
  .addEdge("taskCampaignIdea", "taskCopyCreation")
  .addEdge("taskCopyCreation", END)
;

export const graph = workflow.compile();
graph.name = "MarketingPostsCrew";
// Workflow: wp_sequential
