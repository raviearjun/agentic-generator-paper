import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const BlogcrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_weaviate_vector_search_tool
const tool_weaviate_vector_search_tool = tool(
  async () => {
    return "Result of tool_weaviate_vector_search_tool";
  },
  {
    name: "tool_weaviate_vector_search_tool",
    description: "Vector search tool using Weaviate for semantic retrieval from collection 'WeaviateBlogChunk'.",
    schema: z.object({}),
  }
);
// Tool: tool_serper_dev_tool
const tool_serper_dev_tool = tool(
  async () => {
    return "Result of tool_serper_dev_tool";
  },
  {
    name: "tool_serper_dev_tool",
    description: "Web search tool backed by Serper.dev.",
    schema: z.object({}),
  }
);



/**
 * Node: taskBiomedicalResearch
 * Agent: biomedical_marketing_agent
 */
async function taskBiomedicalResearch(state: typeof BlogcrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Industry researcher focused on biomedical trends and their applications in AI." +
        "\n\nYour task: Conduct a thorough research about {weaviate_feature}\nMake sure you find any interesting and relevant information using the web and Weaviate blogs." +
        "\nNode: taskBiomedicalResearch",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskHealthcareResearch
 * Agent: healthcare_marketing_agent
 */
async function taskHealthcareResearch(state: typeof BlogcrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a AI-savvy marketer specializing in healthcare systems, digital health, and patient engagement.." +
        "\n\nYour task: Conduct a thorough research about {weaviate_feature}\nMake sure you find any interesting and relevant information using the web and Weaviate blogs." +
        "\nNode: taskHealthcareResearch",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskFinancialResearch
 * Agent: financial_marketing_agent
 */
async function taskFinancialResearch(state: typeof BlogcrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Insight analyst exploring innovations in finance, wealth tech, and regulatory tech." +
        "\n\nYour task: Conduct a thorough research about {weaviate_feature}\nMake sure you find any interesting and relevant information using the web and Weaviate blogs." +
        "\nNode: taskFinancialResearch",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(BlogcrewAnnotation)
  .addNode("taskBiomedicalResearch", taskBiomedicalResearch)
  .addNode("taskHealthcareResearch", taskHealthcareResearch)
  .addNode("taskFinancialResearch", taskFinancialResearch)
  .addEdge(START, "taskBiomedicalResearch")
  .addEdge("taskBiomedicalResearch", "taskHealthcareResearch")
  .addEdge("taskHealthcareResearch", "taskFinancialResearch")
  .addEdge("taskFinancialResearch", END)
;

export const graph = workflow.compile();
graph.name = "blogcrew";
// Workflow: workflow_blog_crew
