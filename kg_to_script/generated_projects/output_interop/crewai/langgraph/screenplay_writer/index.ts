import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const AICrewforscreenwritingAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: mistral_tool
const mistral_tool = tool(
  async () => {
    return "Result of mistral_tool";
  },
  {
    name: "mistral_tool",
    description: "Official Mistral LLM API endpoint (optional selection in script).",
    schema: z.object({}),
  }
);
// Tool: together_tool
const together_tool = tool(
  async () => {
    return "Result of together_tool";
  },
  {
    name: "together_tool",
    description: "Together.ai models endpoint (optional selection in script).",
    schema: z.object({}),
  }
);
// Tool: anyscale_tool
const anyscale_tool = tool(
  async () => {
    return "Result of anyscale_tool";
  },
  {
    name: "anyscale_tool",
    description: "Anyscale models endpoint (optional selection in script).",
    schema: z.object({}),
  }
);



/**
 * Node: task1
 * Agent: analyst
 */
async function task1(state: typeof AICrewforscreenwritingAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a analyse." +
        "\nNode: task1",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: task2
 * Agent: scriptwriter
 */
async function task2(state: typeof AICrewforscreenwritingAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a scriptwriter." +
        "\nNode: task2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: task3
 * Agent: formatter
 */
async function task3(state: typeof AICrewforscreenwritingAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a formatter." +
        "\nNode: task3",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(AICrewforscreenwritingAnnotation)
  .addNode("task1", task1)
  .addNode("task2", task2)
  .addNode("task3", task3)
  .addEdge(START, "task1")
  .addEdge("task1", "task2")
  .addEdge("task2", "task3")
  .addEdge("task3", END)
;

export const graph = workflow.compile();
graph.name = "AICrewforscreenwriting";
// Workflow: crew_sequential_workflow
