import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const BlogcrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
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
