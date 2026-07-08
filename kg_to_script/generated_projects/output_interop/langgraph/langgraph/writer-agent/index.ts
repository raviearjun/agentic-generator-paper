import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const WriterStateGraphTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: Prepare a text document for the user with a short title and short description for browsing purposes. Can be also used when creating a new version of the document." +
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
        "\n\nYour task: Write a text document based on the user's request. Only output the content, do not ask any additional questions. If there is selected text in state.context.writer.selected, include that context in the generation." +
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
        "\n\nYour task: Invoke the model on the conversation messages (including tool finished signals) to produce the finish/suggestions message; append the resulting model output to the message stream." +
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
