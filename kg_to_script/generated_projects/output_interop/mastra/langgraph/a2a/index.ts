import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastraA2AClientAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_a2_a_api
const tool_a2_a_api = tool(
  async () => {
    return "Result of tool_a2_a_api";
  },
  {
    name: "tool_a2_a_api",
    description: "A2A JSON-RPC HTTP API endpoints used to interact with remote agents (agent-card, message/send, message/stream, tasks/*, pushNotificationConfig/*).",
    schema: z.object({}),
  }
);
// Tool: tool_process_a2_a_stream
const tool_process_a2_a_stream = tool(
  async () => {
    return "Result of tool_process_a2_a_stream";
  },
  {
    name: "tool_process_a2_a_stream",
    description: "Utility to parse and yield typed A2A stream events (SSE -> typed Message/Task/TaskStatusUpdateEvent/TaskArtifactUpdateEvent).",
    schema: z.object({}),
  }
);



/**
 * Node: taskGetAgentCard
 * Agent: agent_id_constructor_parameter
 */
async function taskGetAgentCard(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskGetAgentCard",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskSendMessage
 * Agent: agent_id_constructor_parameter
 */
async function taskSendMessage(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskSendMessage",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskSendMessageStream
 * Agent: agent_id_constructor_parameter
 */
async function taskSendMessageStream(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskSendMessageStream",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGetTask
 * Agent: agent_id_constructor_parameter
 */
async function taskGetTask(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskGetTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCancelTask
 * Agent: agent_id_constructor_parameter
 */
async function taskCancelTask(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskCancelTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskResubscribeTask
 * Agent: agent_id_constructor_parameter
 */
async function taskResubscribeTask(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskResubscribeTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskSetPushNotificationConfig
 * Agent: agent_id_constructor_parameter
 */
async function taskSetPushNotificationConfig(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskSetPushNotificationConfig",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGetPushNotificationConfig
 * Agent: agent_id_constructor_parameter
 */
async function taskGetPushNotificationConfig(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskGetPushNotificationConfig",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskListPushNotificationConfig
 * Agent: agent_id_constructor_parameter
 */
async function taskListPushNotificationConfig(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskListPushNotificationConfig",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskDeletePushNotificationConfig
 * Agent: agent_id_constructor_parameter
 */
async function taskDeletePushNotificationConfig(state: typeof MastraA2AClientAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a A2A remote agent." +
        "\nNode: taskDeletePushNotificationConfig",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastraA2AClientAnnotation)
  .addNode("taskGetAgentCard", taskGetAgentCard)
  .addNode("taskSendMessage", taskSendMessage)
  .addNode("taskSendMessageStream", taskSendMessageStream)
  .addNode("taskGetTask", taskGetTask)
  .addNode("taskCancelTask", taskCancelTask)
  .addNode("taskResubscribeTask", taskResubscribeTask)
  .addNode("taskSetPushNotificationConfig", taskSetPushNotificationConfig)
  .addNode("taskGetPushNotificationConfig", taskGetPushNotificationConfig)
  .addNode("taskListPushNotificationConfig", taskListPushNotificationConfig)
  .addNode("taskDeletePushNotificationConfig", taskDeletePushNotificationConfig)
  .addEdge(START, "taskGetAgentCard")
  .addEdge("taskGetAgentCard", "taskSendMessage")
  .addEdge("taskSendMessage", "taskSendMessageStream")
  .addEdge("taskSendMessageStream", "taskGetTask")
  .addEdge("taskGetTask", "taskCancelTask")
  .addEdge("taskCancelTask", "taskResubscribeTask")
  .addEdge("taskResubscribeTask", "taskSetPushNotificationConfig")
  .addEdge("taskSetPushNotificationConfig", "taskGetPushNotificationConfig")
  .addEdge("taskGetPushNotificationConfig", "taskListPushNotificationConfig")
  .addEdge("taskListPushNotificationConfig", "taskDeletePushNotificationConfig")
  .addEdge("taskDeletePushNotificationConfig", END)
;

export const graph = workflow.compile();
graph.name = "MastraA2AClient";
// Workflow: a2_a_client_workflow
