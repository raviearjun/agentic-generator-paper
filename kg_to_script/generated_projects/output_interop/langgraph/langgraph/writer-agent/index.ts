import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const WriterStateGraphTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_draft_text_document
const tool_draft_text_document = tool(
  async () => {
    return "Result of tool_draft_text_document";
  },
  {
    name: "tool_draft_text_document",
    description: "Prepare a text document for the user with a short title and short description for browsing purposes. Can be also used when creating a new version of the document.",
    schema: z.object({}),
  }
);



/**
 * Node: taskPrepare
 * Agent: writer_agent
 */
async function taskPrepare(state: typeof WriterStateGraphTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a writer." +
        "\nNode: taskPrepare",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskWriter
 * Agent: writer_agent
 */
async function taskWriter(state: typeof WriterStateGraphTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a writer." +
        "\nNode: taskWriter",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskSuggestions
 * Agent: writer_agent
 */
async function taskSuggestions(state: typeof WriterStateGraphTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a writer." +
        "\nNode: taskSuggestions",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(WriterStateGraphTeamAnnotation)
  .addNode("taskPrepare", taskPrepare)
  .addNode("taskWriter", taskWriter)
  .addNode("taskSuggestions", taskSuggestions)
  .addEdge(START, "taskPrepare")
  .addEdge("taskPrepare", "taskWriter")
  .addEdge("taskWriter", "taskSuggestions")
  .addEdge("taskSuggestions", END)
;

export const graph = workflow.compile();
graph.name = "WriterStateGraphTeam";
// Workflow: writer_state_graph_pattern
