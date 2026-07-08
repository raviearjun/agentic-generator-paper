import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const StandupDuoAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_open_ai_api
const tool_open_ai_api = tool(
  async () => {
    return "Result of tool_open_ai_api";
  },
  {
    name: "tool_open_ai_api",
    description: "External LLM API used by ConversableAgent (via autogen/OpenAI client).",
    schema: z.object({}),
  }
);
// Tool: tool_get_openai_api_key
const tool_get_openai_api_key = tool(
  async () => {
    return "Result of tool_get_openai_api_key";
  },
  {
    name: "tool_get_openai_api_key",
    description: "Helper function used to retrieve the OpenAI API key from environment/config.",
    schema: z.object({}),
  }
);



/**
 * Node: taskGuodegangInitiateChat1
 * Agent: unnamed
 */
async function taskGuodegangInitiateChat1(state: typeof StandupDuoAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a 逗哏 / stand-up comedian (performer)." +
        "\n\nYour task: message=\"我是郭德纲，于谦呀，我们给观众讲一段相声怎么样？\"; recipient=于谦; max_turns=6" +
        "\nNode: taskGuodegangInitiateChat1",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGuodegangInitiateChat2
 * Agent: unnamed
 */
async function taskGuodegangInitiateChat2(state: typeof StandupDuoAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a 逗哏 / stand-up comedian (performer)." +
        "\n\nYour task: message=\"我是郭德纲，于谦呀，我们给观众讲一段相声怎么样？\"; summary_method=\"reflection_with_llm\"; summary_prompt=\"简洁的总结下这场相声表演。\"" +
        "\nNode: taskGuodegangInitiateChat2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGuodegangSendFollowup
 * Agent: unnamed
 */
async function taskGuodegangSendFollowup(state: typeof StandupDuoAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a 逗哏 / stand-up comedian (performer)." +
        "\n\nYour task: message='我们刚才的相声在讲什么?'; recipient=于谦" +
        "\nNode: taskGuodegangSendFollowup",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(StandupDuoAnnotation)
  .addNode("taskGuodegangInitiateChat1", taskGuodegangInitiateChat1)
  .addNode("taskGuodegangInitiateChat2", taskGuodegangInitiateChat2)
  .addNode("taskGuodegangSendFollowup", taskGuodegangSendFollowup)
  .addEdge(START, "taskGuodegangInitiateChat1")
  .addEdge("taskGuodegangInitiateChat1", "taskGuodegangInitiateChat2")
  .addEdge("taskGuodegangInitiateChat2", "taskGuodegangSendFollowup")
  .addEdge("taskGuodegangSendFollowup", END)
;

export const graph = workflow.compile();
graph.name = "StandupDuo";
// Workflow: workflow_xiangsheng
