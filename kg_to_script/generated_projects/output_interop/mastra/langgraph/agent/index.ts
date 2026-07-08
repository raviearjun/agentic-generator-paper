import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastraInstancelocalAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: my_tool
const my_tool = tool(
  async () => {
    return "Result of my_tool";
  },
  {
    name: "my_tool",
    description: "My tool description",
    schema: z.object({}),
  }
);



/**
 * Node: taskQueryPantry
 * Agent: chef_agent
 */
async function taskQueryPantry(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make?" +
        "\nNode: taskQueryPantry",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGenerateText
 * Agent: chef_agent
 */
async function taskGenerateText(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make?" +
        "\nNode: taskGenerateText",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTextStream
 * Agent: chef_agent
 */
async function taskTextStream(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder." +
        "\nNode: taskTextStream",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGenerateStream
 * Agent: chef_agent
 */
async function taskGenerateStream(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder." +
        "\nNode: taskGenerateStream",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTextObject
 * Agent: chef_agent
 */
async function taskTextObject(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: I want to make lasagna, can you generate a lasagna recipe for me?" +
        "\nNode: taskTextObject",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskTextObjectJsonschema
 * Agent: chef_agent
 */
async function taskTextObjectJsonschema(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: I want to make lasagna, can you generate a lasagna recipe for me?" +
        "\nNode: taskTextObjectJsonschema",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGenerateObject
 * Agent: chef_agent
 */
async function taskGenerateObject(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: I want to make lasagna, can you generate a lasagna recipe for me?" +
        "\nNode: taskGenerateObject",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStreamObject
 * Agent: chef_agent
 */
async function taskStreamObject(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: I want to make lasagna, can you generate a lasagna recipe for me?" +
        "\nNode: taskStreamObject",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGenerateStreamObject
 * Agent: chef_agent
 */
async function taskGenerateStreamObject(state: typeof MastraInstancelocalAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chef." +
        "\n\nYour task: I want to make lasagna, can you generate a lasagna recipe for me?" +
        "\nNode: taskGenerateStreamObject",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastraInstancelocalAnnotation)
  .addNode("taskQueryPantry", taskQueryPantry)
  .addNode("taskGenerateText", taskGenerateText)
  .addNode("taskTextStream", taskTextStream)
  .addNode("taskGenerateStream", taskGenerateStream)
  .addNode("taskTextObject", taskTextObject)
  .addNode("taskTextObjectJsonschema", taskTextObjectJsonschema)
  .addNode("taskGenerateObject", taskGenerateObject)
  .addNode("taskStreamObject", taskStreamObject)
  .addNode("taskGenerateStreamObject", taskGenerateStreamObject)
  .addEdge(START, "taskQueryPantry")
  .addEdge("taskQueryPantry", "taskGenerateText")
  .addEdge("taskGenerateText", "taskTextStream")
  .addEdge("taskTextStream", "taskGenerateStream")
  .addEdge("taskGenerateStream", "taskTextObject")
  .addEdge("taskTextObject", "taskTextObjectJsonschema")
  .addEdge("taskTextObjectJsonschema", "taskGenerateObject")
  .addEdge("taskGenerateObject", "taskStreamObject")
  .addEdge("taskStreamObject", "taskGenerateStreamObject")
  .addEdge("taskGenerateStreamObject", END)
;

export const graph = workflow.compile();
graph.name = "MastraInstancelocal";
// Workflow: chef_workflow
