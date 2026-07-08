import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastraInstanceycagentAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: yc_directory_tool
const yc_directory_tool = tool(
  async () => {
    return "Result of yc_directory_tool";
  },
  {
    name: "yc_directory_tool",
    description: "Get data from the 2024 YC directory",
    schema: z.object({}),
  }
);



/**
 * Node: fetchYcDirectoryTask
 * Agent: yc_directory_agent
 */
async function fetchYcDirectoryTask(state: typeof MastraInstanceycagentAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a directory." +
        "\n\nYour task: Invoke the 'yc-directory' tool to retrieve the full 2024 YC directory. Return the array of company objects exactly as provided by the tool." +
        "\nNode: fetchYcDirectoryTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: processYcDataTask
 * Agent: yc_directory_agent
 */
async function processYcDataTask(state: typeof MastraInstanceycagentAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a directory." +
        "\n\nYour task: Format the retrieved YC directory data for user-friendly responses. Ensure each company mentions its batch and includes name, industries, and short summary." +
        "\nNode: processYcDataTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastraInstanceycagentAnnotation)
  .addNode("fetchYcDirectoryTask", fetchYcDirectoryTask)
  .addNode("processYcDataTask", processYcDataTask)
  .addEdge(START, "fetchYcDirectoryTask")
  .addEdge("fetchYcDirectoryTask", "processYcDataTask")
  .addEdge("processYcDataTask", END)
;

export const graph = workflow.compile();
graph.name = "MastraInstanceycagent";
// Workflow: yc_directory_workflow
