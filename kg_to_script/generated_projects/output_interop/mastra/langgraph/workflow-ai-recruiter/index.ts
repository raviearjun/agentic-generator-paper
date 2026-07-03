import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const MastrainstanceworkflowairecruiterAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
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
