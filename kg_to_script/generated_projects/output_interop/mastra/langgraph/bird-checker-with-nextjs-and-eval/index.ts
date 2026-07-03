import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const BirdCheckerSystemAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: get_random_image_tool
const get_random_image_tool = tool(
  async () => {
    return "Result of get_random_image_tool";
  },
  {
    name: "get_random_image_tool",
    description: "Gets a random image from unsplash based on the selected option",
    schema: z.object({}),
  }
);



/**
 * Node: getImageTask
 * Agent: bird_agent
 */
async function getImageTask(state: typeof BirdCheckerSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a bird classifier." +
        "\nNode: getImageTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: classifyImageTask
 * Agent: bird_agent
 */
async function classifyImageTask(state: typeof BirdCheckerSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a bird classifier." +
        "\nNode: classifyImageTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(BirdCheckerSystemAnnotation)
  .addNode("getImageTask", getImageTask)
  .addNode("classifyImageTask", classifyImageTask)
  .addEdge(START, "getImageTask")
  .addEdge("getImageTask", "classifyImageTask")
  .addEdge("classifyImageTask", END)
;

export const graph = workflow.compile();
graph.name = "BirdCheckerSystem";
// Workflow: bird_checker_workflow
