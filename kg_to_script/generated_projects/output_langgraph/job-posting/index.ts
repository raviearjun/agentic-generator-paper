import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const JobPostingCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: Analyze the provided company website and the hiring manager's company's domain {company_domain}, description {company_description}. Focus on understanding the company's culture, values, and mission. Identify unique selling points and specific projects or achievements highlighted on the site. Compile a report summarizing these insights, specifically how they can be leveraged in a job posting to attract the right candidates." +
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
        "\n\nYour task: Based on the hiring manager's needs: {hiring_needs}, identify the key skills, experiences, and qualities the ideal candidate should possess for the role. Consider the company's current projects, its competitive landscape, and industry trends. Prepare a list of recommended job requirements and qualifications that align with the company's needs and values." +
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
        "\n\nYour task: Draft a job posting for the role described by the hiring manager: {hiring_needs}. Use the insights on {company_description} to start with a compelling introduction, followed by a detailed role description, responsibilities, and required skills and qualifications. Ensure the tone aligns with the company's culture and incorporate any unique benefits or opportunities offered by the company. Specific benefits: {specific_benefits}." +
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
        "\n\nYour task: Review the draft job posting for the role {hiring_needs}. Check for clarity, engagement, grammatical accuracy, and alignment with the company's culture and values. Edit and refine the content, ensuring it speaks directly to the desired candidates and accurately reflects the role's unique benefits and opportunities. Provide feedback for any necessary revisions." +
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
        "\n\nYour task: Conduct an in-depth analysis of the industry related to the company's domain {company_domain}. Investigate current trends, challenges, and opportunities within the industry, utilizing market reports, recent developments, and expert opinions. Assess how these factors could impact the role being hired for and the overall attractiveness of the position to potential candidates." +
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
