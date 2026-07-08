import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const CopyCrewagentsforcopygenerationAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: Analyze the given product website: {product_website}.\nExtra details provided by the customer: {product_details}.\nFocus on identifying unique features, benefits, and the overall narrative. Provide a final report articulating key selling points, market appeal, and suggestions for enhancement or positioning. Attention to detail and up-to-date (2024) context required." +
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
        "\n\nYour task: Explore competitors of: {product_website}.\nExtra details provided by the customer: {product_details}.\nIdentify the top 3 competitors and analyze their strategies, market positioning, and customer perception. Include context about the target website and detailed comparison." +
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
        "\n\nYour task: Create a targeted marketing campaign for: {product_website}.\nExtra details provided by the customer: {product_details}.\nProduce strategy and creative content ideas designed to captivate the target audience. Provide ideas that resonate with the audience and include all available product/context information." +
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
        "\n\nYour task: Craft an engaging Instagram post copy. The copy should be punchy, captivating, concise, and aligned with the product marketing strategy. Focus on creating a message that resonates with the target audience and highlights the product's unique selling points." +
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
        "\n\nYour task: You MUST take the most amazing photo ever for an instagram post regarding the product. Provided ad copy: {copy}\nProduct: {product_website}\nExtra details: {product_details}\nImagine the photograph and describe it in a paragraph. Follow examples (professional wide shot, soft lighting, 4k, crisp, etc.). Do not show the actual product in photos." +
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
        "\n\nYour task: Review the photos from the senior photographer. Ensure alignment with product goals; review, approve, ask clarifying questions or delegate follow-up work as necessary. When delegating, include the full draft as part of the information.\nProduct: {product_website}\nExtra details: {product_details}\nExamples: (high tech airplane in a beautiful blue sky ...; the last supper ...; a bearded old man in the snows ...)." +
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
