import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const MastrainstanceworkflowairecruiterAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});




/**
 * Node: gatherCandidateInfoTask
 * Agent: mastra_llm
 */
async function gatherCandidateInfoTask(state: typeof MastrainstanceworkflowairecruiterAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-processor." +
        "\n\nYour task: You are given this resume text: \"\${resumeText}\"" +
        "\nNode: gatherCandidateInfoTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: askAboutSpecialtyTask
 * Agent: mastra_llm
 */
async function askAboutSpecialtyTask(state: typeof MastrainstanceworkflowairecruiterAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-processor." +
        "\n\nYour task: You are a recruiter. Given the resume below, craft a short question for \${candidateName} about how they got into \"\${specialty}\". Resume: \${resumeText}" +
        "\nNode: askAboutSpecialtyTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: askAboutRoleTask
 * Agent: mastra_llm
 */
async function askAboutRoleTask(state: typeof MastrainstanceworkflowairecruiterAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-processor." +
        "\n\nYour task: You are a recruiter. Given the resume below, craft a short question for \${candidateName} asking what interests them most about this role. Resume: \${resumeText}" +
        "\nNode: askAboutRoleTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastrainstanceworkflowairecruiterAnnotation)
  .addNode("gatherCandidateInfoTask", gatherCandidateInfoTask)
  .addNode("askAboutSpecialtyTask", askAboutSpecialtyTask)
  .addNode("askAboutRoleTask", askAboutRoleTask)
  .addEdge(START, "gatherCandidateInfoTask")
  .addEdge("gatherCandidateInfoTask", "askAboutSpecialtyTask")
  .addEdge("gatherCandidateInfoTask", "askAboutRoleTask")
  .addEdge("askAboutSpecialtyTask", END)
  .addEdge("askAboutRoleTask", END)
;

export const graph = workflow.compile();
graph.name = "mastrainstanceworkflowairecruiter";
// Workflow: candidate_workflow_pattern
