import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const EmailAssistantTeamStateGraphsystemAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: You're an AI email assistant, tasked with writing an email for the user.\nUse the entire conversation history between you, and the user to craft the email for them.\n\n<conversation>\n{CONVERSATION}\n</conversation>\n\nIf there is NOT enough information to send an email, respond to the user requesting the missing information.\nRequired fields:\n- subject - The subject of the email\n- body - The body of the email\n- to - The recipient of the email" +
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
        "\n\nYour task: # New Email\n\n## Subject\n{subject}\n\n## To\n{to}\n\n## Body\n{body}\n\n## Response Instructions\n\n- **Response**: Any response submitted will be passed to an LLM to rewrite the email. It can rewrite the email body, subject, or recipient.\n\n- **Edit or Accept**: Editing/Accepting the email will send the email.\n\n- **Ignore**: Ignoring the email will end the conversation, and the email will not be sent." +
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
        "\n\nYour task: You're an AI email assistant, tasked with rewriting an email for the user.\nHere is the current state of the email for the user:\n<email>\n  <subject>\n    {SUBJECT}\n  </subject>\n  <body>\n    {BODY}\n  </body>\n  <to>\n    {TO}\n  </to>\n</email>\n\nHere is the user's response, which should contain some request for changes to the email:\n<user-response>\n{USER_RESPONSE}\n</user-response>\n\nGiven that, please rewrite the email. Do NOT modify anything the user does not request to be changed." +
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
        "\n\nYour task: Render a confirmation UI indicating the email was successfully sent." +
        "\nNode: taskSendEmail",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(EmailAssistantTeamStateGraphsystemAnnotation)
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
