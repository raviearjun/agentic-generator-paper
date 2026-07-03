import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastraClientSystemAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: voice_provider_tool
const voice_provider_tool = tool(
  async () => {
    return "Result of voice_provider_tool";
  },
  {
    name: "voice_provider_tool",
    description: "Voice provider used by the agent for text-to-speech (speak) and speech-to-text (listen) operations via agent.voice endpoints.",
    schema: z.object({}),
  }
);
// Tool: client_tools_tool
const client_tools_tool = tool(
  async () => {
    return "Result of client_tools_tool";
  },
  {
    name: "client_tools_tool",
    description: "Abstract representation of the \`clientTools\` map supplied to the Mastra agent client; client-provided tools executed via \`clientTool.execute\`.",
    schema: z.object({}),
  }
);



/**
 * Node: taskProcessRequest
 * Agent: mastra_agent_client
 */
async function taskProcessRequest(state: typeof MastraClientSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a client-wrapper." +
        "\nNode: taskProcessRequest",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskExecuteClientTool
 * Agent: mastra_agent_client
 */
async function taskExecuteClientTool(state: typeof MastraClientSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a client-wrapper." +
        "\nNode: taskExecuteClientTool",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskReturnResponse
 * Agent: mastra_agent_client
 */
async function taskReturnResponse(state: typeof MastraClientSystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a client-wrapper." +
        "\nNode: taskReturnResponse",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastraClientSystemAnnotation)
  .addNode("taskProcessRequest", taskProcessRequest)
  .addNode("taskExecuteClientTool", taskExecuteClientTool)
  .addNode("taskReturnResponse", taskReturnResponse)
  .addEdge(START, "taskProcessRequest")
  .addEdge("taskProcessRequest", "taskExecuteClientTool")
  .addEdge("taskExecuteClientTool", "taskReturnResponse")
  .addEdge("taskReturnResponse", END)
;

export const graph = workflow.compile();
graph.name = "MastraClientSystem";
// Workflow: mastra_agent_workflow
