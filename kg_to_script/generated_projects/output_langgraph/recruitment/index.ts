import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const RecruitmentCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_serperdev
const tool_serperdev = tool(
  async () => {
    return "Result of tool_serperdev";
  },
  {
    name: "tool_serperdev",
    description: "Search API tool for retrieving web search results.",
    schema: z.object({}),
  }
);
// Tool: tool_scrape_website
const tool_scrape_website = tool(
  async () => {
    return "Result of tool_scrape_website";
  },
  {
    name: "tool_scrape_website",
    description: "Tool for scraping and extracting structured information from websites.",
    schema: z.object({}),
  }
);
// Tool: tool_linkedin
const tool_linkedin = tool(
  async () => {
    return "Result of tool_linkedin";
  },
  {
    name: "tool_linkedin",
    description: "Custom LinkedIn retrieval tool that uses an authenticated browser session to find candidate profiles.",
    schema: z.object({}),
  }
);



/**
 * Node: taskResearchCandidates
 * Agent: researcher
 */
async function taskResearchCandidates(state: typeof RecruitmentCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Job Candidate Researcher." +
        "\n\nYour task: Conduct thorough research to find potential candidates for the specified job. Utilize various online resources and databases to gather a comprehensive list of potential candidates. Ensure that the candidates meet the job requirements provided.\n\nJob Requirements: {job_requirements}" +
        "\nNode: taskResearchCandidates",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskMatchAndScoreCandidates
 * Agent: matcher
 */
async function taskMatchAndScoreCandidates(state: typeof RecruitmentCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Candidate Matcher and Scorer." +
        "\n\nYour task: Evaluate and match the candidates to the best job positions based on their qualifications and suitability. Score each candidate to reflect their alignment with the job requirements. Don't try to scrape people's linkedin, since you don't have access to it.\n\nJob Requirements: {job_requirements}" +
        "\nNode: taskMatchAndScoreCandidates",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskOutreachStrategy
 * Agent: communicator
 */
async function taskOutreachStrategy(state: typeof RecruitmentCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Candidate Outreach Strategist." +
        "\n\nYour task: Develop a comprehensive strategy to reach out to the selected candidates. Create effective outreach methods and templates that can engage the candidates and encourage them to consider the job opportunity.\n\nJob Requirements: {job_requirements}" +
        "\nNode: taskOutreachStrategy",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskReportCandidates
 * Agent: reporter
 */
async function taskReportCandidates(state: typeof RecruitmentCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Candidate Reporting Specialist." +
        "\n\nYour task: Compile a comprehensive report for recruiters on the best candidates to put forward. Summarize the findings from the previous tasks and provide clear recommendations based on the job requirements." +
        "\nNode: taskReportCandidates",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(RecruitmentCrewAnnotation)
  .addNode("taskResearchCandidates", taskResearchCandidates)
  .addNode("taskMatchAndScoreCandidates", taskMatchAndScoreCandidates)
  .addNode("taskOutreachStrategy", taskOutreachStrategy)
  .addNode("taskReportCandidates", taskReportCandidates)
  .addEdge(START, "taskResearchCandidates")
  .addEdge("taskResearchCandidates", "taskMatchAndScoreCandidates")
  .addEdge("taskMatchAndScoreCandidates", "taskOutreachStrategy")
  .addEdge("taskOutreachStrategy", "taskReportCandidates")
  .addEdge("taskReportCandidates", END)
;

export const graph = workflow.compile();
graph.name = "RecruitmentCrew";
// Workflow: workflow_recruitment
