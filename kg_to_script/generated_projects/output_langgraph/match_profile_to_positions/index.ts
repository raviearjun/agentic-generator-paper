import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MatchToProposalCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_file_read
const tool_file_read = tool(
  async () => {
    return "Result of tool_file_read";
  },
  {
    name: "tool_file_read",
    description: "Tool to read file contents (used to read CV and other files).",
    schema: z.object({}),
  }
);
// Tool: tool_csv_search
const tool_csv_search = tool(
  async () => {
    return "Result of tool_csv_search";
  },
  {
    name: "tool_csv_search",
    description: "Tool to search and query CSV files for matching job opportunities.",
    schema: z.object({}),
  }
);



/**
 * Node: taskReadCv
 * Agent: cv_reader
 */
async function taskReadCv(state: typeof MatchToProposalCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a CV Reader." +
        "\n\nYour task: Extract relevant information from the given CV. Focus on skills, experience, education, and key achievements.\nEnsure to capture the candidate's professional summary, technical skills, work history, and educational background.\n\nCV file: {path_to_cv}" +
        "\nNode: taskReadCv",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskMatchCv
 * Agent: matcher
 */
async function taskMatchCv(state: typeof MatchToProposalCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Matcher." +
        "\n\nYour task: Match the CV to the job opportunities based on skills, experience, and key achievements.\nEvaluate how well the candidate's profile fits each job description, focusing on the alignment of skills, work history, and key achievements with the job requirements.\n\nJobs CSV file: {path_to_jobs_csv}\n\nCV file: {path_to_cv}" +
        "\nNode: taskMatchCv",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MatchToProposalCrewAnnotation)
  .addNode("taskReadCv", taskReadCv)
  .addNode("taskMatchCv", taskMatchCv)
  .addEdge(START, "taskReadCv")
  .addEdge("taskReadCv", "taskMatchCv")
  .addEdge("taskMatchCv", END)
;

export const graph = workflow.compile();
graph.name = "MatchToProposalCrew";
// Workflow: workflow_sequential
