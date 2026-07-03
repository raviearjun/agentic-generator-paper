import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const JobPostingCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: website_search_tool
const website_search_tool = tool(
  async () => {
    return "Result of website_search_tool";
  },
  {
    name: "website_search_tool",
    description: "A generic website search tool used to look up pages and content.",
    schema: z.object({}),
  }
);
// Tool: serper_dev_tool
const serper_dev_tool = tool(
  async () => {
    return "Result of serper_dev_tool";
  },
  {
    name: "serper_dev_tool",
    description: "Serper.dev integration tool for advanced search queries.",
    schema: z.object({}),
  }
);
// Tool: file_read_tool
const file_read_tool = tool(
  async () => {
    return "Result of file_read_tool";
  },
  {
    name: "file_read_tool",
    description: "A tool to read a local job description example file.",
    schema: z.object({}),
  }
);



/**
 * Node: researchCompanyCultureTask
 * Agent: research_agent
 */
async function researchCompanyCultureTask(state: typeof JobPostingCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Research Analyst." +
        "\nNode: researchCompanyCultureTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: researchRoleRequirementsTask
 * Agent: research_agent
 */
async function researchRoleRequirementsTask(state: typeof JobPostingCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Research Analyst." +
        "\nNode: researchRoleRequirementsTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: draftJobPostingTask
 * Agent: writer_agent
 */
async function draftJobPostingTask(state: typeof JobPostingCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Job Description Writer." +
        "\nNode: draftJobPostingTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: reviewAndEditJobPostingTask
 * Agent: review_agent
 */
async function reviewAndEditJobPostingTask(state: typeof JobPostingCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Review and Editing Specialist." +
        "\nNode: reviewAndEditJobPostingTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: industryAnalysisTask
 * Agent: research_agent
 */
async function industryAnalysisTask(state: typeof JobPostingCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Research Analyst." +
        "\nNode: industryAnalysisTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(JobPostingCrewAnnotation)
  .addNode("researchCompanyCultureTask", researchCompanyCultureTask)
  .addNode("researchRoleRequirementsTask", researchRoleRequirementsTask)
  .addNode("draftJobPostingTask", draftJobPostingTask)
  .addNode("reviewAndEditJobPostingTask", reviewAndEditJobPostingTask)
  .addNode("industryAnalysisTask", industryAnalysisTask)
  .addEdge(START, "researchCompanyCultureTask")
  .addEdge("researchCompanyCultureTask", "researchRoleRequirementsTask")
  .addEdge("researchRoleRequirementsTask", "draftJobPostingTask")
  .addEdge("draftJobPostingTask", "reviewAndEditJobPostingTask")
  .addEdge("reviewAndEditJobPostingTask", "industryAnalysisTask")
  .addEdge("industryAnalysisTask", END)
;

export const graph = workflow.compile();
graph.name = "JobPostingCrew";
// Workflow: job_posting_workflow
