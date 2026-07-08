import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastrainstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: mastra_runtime
const mastra_runtime = tool(
  async () => {
    return "Result of mastra_runtime";
  },
  {
    name: "mastra_runtime",
    description: "Runtime engine that executes workflow step code (non-LLM execution).",
    schema: z.object({}),
  }
);



/**
 * Node: taskLogCatName
 * Agent: cat_one
 */
async function taskLogCatName(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline expert." +
        "\\n\\nYour task: Log the cat name provided in the trigger: console.log(\`Hello, \${name} 🐈\`)" +
        "\\nNode: taskLogCatName",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastrainstanceAnnotation)
  .addNode("taskLogCatName", taskLogCatName)
  .addEdge(START, "taskLogCatName")
  .addEdge("taskLogCatName", END)
;

export const graph = workflow.compile();
graph.name = "mastrainstance";
// Workflow: log_cat_workflow
