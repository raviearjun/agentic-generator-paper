import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastravnextAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_site_crawl
const tool_site_crawl = tool(
  async () => {
    return "Result of tool_site_crawl";
  },
  {
    name: "tool_site_crawl",
    description: "Crawl a website and extract the markdown content",
    schema: z.object({}),
  }
);
// Tool: tool_generate_spec
const tool_generate_spec = tool(
  async () => {
    return "Result of tool_generate_spec";
  },
  {
    name: "tool_generate_spec",
    description: "Generate a spec from a website",
    schema: z.object({}),
  }
);
// Tool: tool_add_to_github
const tool_add_to_github = tool(
  async () => {
    return "Result of tool_add_to_github";
  },
  {
    name: "tool_add_to_github",
    description: "Commit the spec to GitHub and create a PR",
    schema: z.object({}),
  }
);



/**
 * Node: taskSiteCrawlSync
 * Agent: openapi_spec_gen_agent
 */
async function taskSiteCrawlSync(state: typeof MastravnextAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a openapi-spec-writer." +
        "\nNode: taskSiteCrawlSync",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGenerateSpec
 * Agent: openapi_spec_gen_agent
 */
async function taskGenerateSpec(state: typeof MastravnextAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a openapi-spec-writer." +
        "\nNode: taskGenerateSpec",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskAddToGithub
 * Agent: openapi_spec_gen_agent
 */
async function taskAddToGithub(state: typeof MastravnextAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a openapi-spec-writer." +
        "\nNode: taskAddToGithub",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastravnextAnnotation)
  .addNode("taskSiteCrawlSync", taskSiteCrawlSync)
  .addNode("taskGenerateSpec", taskGenerateSpec)
  .addNode("taskAddToGithub", taskAddToGithub)
  .addEdge(START, "taskSiteCrawlSync")
  .addEdge("taskSiteCrawlSync", "taskGenerateSpec")
  .addEdge("taskGenerateSpec", END)
  .addEdge("taskAddToGithub", END)
;

export const graph = workflow.compile();
graph.name = "mastravnext";
// Workflow: wp_open_api_spec_gen_workflow
// Workflow: wp_make_pr_to_mastra
