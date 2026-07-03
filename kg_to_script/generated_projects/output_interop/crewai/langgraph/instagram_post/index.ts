import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const CopyCrewagentsforcopygenerationAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_scrape_website
const tool_scrape_website = tool(
  async () => {
    return "Result of tool_scrape_website";
  },
  {
    name: "tool_scrape_website",
    description: "Scrapes a webpage via Browserless API and summarizes chunks using an LLM.",
    schema: z.object({}),
  }
);
// Tool: tool_search_internet
const tool_search_internet = tool(
  async () => {
    return "Result of tool_search_internet";
  },
  {
    name: "tool_search_internet",
    description: "Performs web searches using the Serper (google.serper.dev) API and returns top results.",
    schema: z.object({}),
  }
);
// Tool: tool_search_instagram
const tool_search_instagram = tool(
  async () => {
    return "Result of tool_search_instagram";
  },
  {
    name: "tool_search_instagram",
    description: "Performs targeted Instagram site searches (site:instagram.com ...) via Serper API.",
    schema: z.object({}),
  }
);



/**
 * Node: taskProductAnalysis
 * Agent: product_competitor_agent
 */
async function taskProductAnalysis(state: typeof CopyCrewagentsforcopygenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Lead Market Analyst." +
        "\nNode: taskProductAnalysis",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCompetitorAnalysis
 * Agent: product_competitor_agent
 */
async function taskCompetitorAnalysis(state: typeof CopyCrewagentsforcopygenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Lead Market Analyst." +
        "\nNode: taskCompetitorAnalysis",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCampaignDevelopment
 * Agent: strategy_planner_agent
 */
async function taskCampaignDevelopment(state: typeof CopyCrewagentsforcopygenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chief Marketing Strategist." +
        "\nNode: taskCampaignDevelopment",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskInstagramAdCopy
 * Agent: creative_content_creator_agent
 */
async function taskInstagramAdCopy(state: typeof CopyCrewagentsforcopygenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Creative Content Creator." +
        "\nNode: taskInstagramAdCopy",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTakePhotograph
 * Agent: senior_photographer_agent
 */
async function taskTakePhotograph(state: typeof CopyCrewagentsforcopygenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior Photographer." +
        "\nNode: taskTakePhotograph",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskReviewPhoto
 * Agent: chief_creative_diretor_agent
 */
async function taskReviewPhoto(state: typeof CopyCrewagentsforcopygenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chief Creative Director." +
        "\nNode: taskReviewPhoto",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(CopyCrewagentsforcopygenerationAnnotation)
  .addNode("taskProductAnalysis", taskProductAnalysis)
  .addNode("taskCompetitorAnalysis", taskCompetitorAnalysis)
  .addNode("taskCampaignDevelopment", taskCampaignDevelopment)
  .addNode("taskInstagramAdCopy", taskInstagramAdCopy)
  .addNode("taskTakePhotograph", taskTakePhotograph)
  .addNode("taskReviewPhoto", taskReviewPhoto)
  .addEdge(START, "taskProductAnalysis")
  .addEdge("taskProductAnalysis", "taskCompetitorAnalysis")
  .addEdge("taskCompetitorAnalysis", "taskCampaignDevelopment")
  .addEdge("taskCampaignDevelopment", "taskInstagramAdCopy")
  .addEdge("taskTakePhotograph", "taskReviewPhoto")
  .addEdge("taskInstagramAdCopy", END)
  .addEdge("taskReviewPhoto", END)
;

export const graph = workflow.compile();
graph.name = "CopyCrewagentsforcopygeneration";
// Workflow: workflow_copy_crew
// Workflow: workflow_image_crew
