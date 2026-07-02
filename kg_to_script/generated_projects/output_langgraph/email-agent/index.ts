import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const EmailAssistantTeamStateGraphsystemAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_write_email
const tool_write_email = tool(
  async () => {
    return "Result of tool_write_email";
  },
  {
    name: "tool_write_email",
    description: "Write an email based on the conversation history",
    schema: z.object({}),
  }
);



/**
 * Node: taskWriteEmail
 * Agent: email_assistant_agent
 */
async function taskWriteEmail(state: typeof EmailAssistantTeamStateGraphsystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Email Assistant." +
        "\nNode: taskWriteEmail",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskWriteEmail
 * Agent: email_assistant_agent
 */
async function taskWriteEmail(state: typeof EmailAssistantTeamStateGraphsystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Email Assistant." +
        "\nNode: taskWriteEmail",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskInterrupt
 * Agent: email_assistant_agent
 */
async function taskInterrupt(state: typeof EmailAssistantTeamStateGraphsystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Email Assistant." +
        "\nNode: taskInterrupt",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskRewriteEmail
 * Agent: email_assistant_agent
 */
async function taskRewriteEmail(state: typeof EmailAssistantTeamStateGraphsystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Email Assistant." +
        "\nNode: taskRewriteEmail",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskSendEmail
 * Agent: email_assistant_agent
 */
async function taskSendEmail(state: typeof EmailAssistantTeamStateGraphsystemAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Email Assistant." +
        "\nNode: taskSendEmail",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(EmailAssistantTeamStateGraphsystemAnnotation)
  .addNode("taskWriteEmail", taskWriteEmail)
  .addNode("taskWriteEmail", taskWriteEmail)
  .addNode("taskInterrupt", taskInterrupt)
  .addNode("taskRewriteEmail", taskRewriteEmail)
  .addNode("taskSendEmail", taskSendEmail)
  .addEdge(START, "taskWriteEmail")
  .addEdge("taskWriteEmail", "taskWriteEmail")
  .addEdge("taskWriteEmail", "taskInterrupt")
  .addEdge("taskInterrupt", "taskSendEmail")
  .addEdge("taskInterrupt", "taskRewriteEmail")
  .addEdge("taskRewriteEmail", "taskInterrupt")
;

export const graph = workflow.compile();
graph.name = "EmailAssistantTeamStateGraphsystem";
// Workflow: email_agent_state_graph
