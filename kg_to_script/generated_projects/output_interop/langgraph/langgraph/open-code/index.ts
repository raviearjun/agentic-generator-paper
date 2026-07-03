import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const ProposedChangeUITeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_update_file
const tool_update_file = tool(
  async () => {
    return "Result of tool_update_file";
  },
  {
    name: "tool_update_file",
    description: "Tool used to apply an accepted proposed change to files (invoked via tool call messages).",
    schema: z.object({}),
  }
);



/**
 * Node: taskProposeChange
 * Agent: langgraph_agent
 */
async function taskProposeChange(state: typeof ProposedChangeUITeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\nNode: taskProposeChange",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskUserDecision
 * Agent: langgraph_agent
 */
async function taskUserDecision(state: typeof ProposedChangeUITeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\nNode: taskUserDecision",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskHandleReject
 * Agent: langgraph_agent
 */
async function taskHandleReject(state: typeof ProposedChangeUITeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\nNode: taskHandleReject",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskFinalizeUi
 * Agent: langgraph_agent
 */
async function taskFinalizeUi(state: typeof ProposedChangeUITeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant." +
        "\nNode: taskFinalizeUi",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(ProposedChangeUITeamAnnotation)
  .addNode("taskProposeChange", taskProposeChange)
  .addNode("taskUserDecision", taskUserDecision)
  .addNode("taskHandleReject", taskHandleReject)
  .addNode("taskFinalizeUi", taskFinalizeUi)
  .addEdge(START, "taskProposeChange")
  .addEdge("taskProposeChange", "taskUserDecision")
  .addEdge("taskUserDecision", "taskHandleReject")
  .addEdge("taskHandleReject", "taskFinalizeUi")
  .addEdge("taskFinalizeUi", END)
;

export const graph = workflow.compile();
graph.name = "ProposedChangeUITeam";
// Workflow: workflow_proposed_change
