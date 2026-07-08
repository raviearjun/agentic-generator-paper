import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const BirdCheckerSystemAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
    description: "Gets a random image from Unsplash based on the selected option",
    schema: z.object({}),
  }
);



/**
 * Node: getRandomImageTask
 * Agent: bird_checker
 */
async function getRandomImageTask(state: typeof BirdCheckerSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a bird-checker." +
        "\n\nYour task: Fetch a random image from Unsplash matching the provided query parameter (wildlife | bird | feathers | flying). Return imageUrl, photographerName, and photographerProfile." +
        "\nNode: getRandomImageTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: imageMetadataTask
 * Agent: bird_checker
 */
async function imageMetadataTask(state: typeof BirdCheckerSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a bird-checker." +
        "\n\nYour task: View this image and let me know if it's a bird or not, and the scientific name of the bird without any explanation. Also summarize the location for this picture in one or two short sentences understandable by a high school student." +
        "\nNode: imageMetadataTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(BirdCheckerSystemAnnotation)
  .addNode("getRandomImageTask", getRandomImageTask)
  .addNode("imageMetadataTask", imageMetadataTask)
  .addEdge(START, "getRandomImageTask")
  .addEdge("getRandomImageTask", "imageMetadataTask")
  .addEdge("imageMetadataTask", END)
;

export const graph = workflow.compile();
graph.name = "BirdCheckerSystem";
// Workflow: bird_check_workflow
