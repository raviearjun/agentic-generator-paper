import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const GameBuilderCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_serper
const tool_serper = tool(
  async () => {
    return "Result of tool_serper";
  },
  {
    name: "tool_serper",
    description: "Serper search API used for web search (mentioned in README).",
    schema: z.object({}),
  }
);
// Tool: tool_openai_api
const tool_openai_api = tool(
  async () => {
    return "Result of tool_openai_api";
  },
  {
    name: "tool_openai_api",
    description: "OpenAI API access used by CrewAI to call LLMs (configured via environment variables).",
    schema: z.object({}),
  }
);



/**
 * Node: taskCode
 * Agent: senior_engineer_agent
 */
async function taskCode(state: typeof GameBuilderCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior Software Engineer." +
        "\nNode: taskCode",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskReview
 * Agent: qa_engineer_agent
 */
async function taskReview(state: typeof GameBuilderCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Software Quality Control Engineer." +
        "\nNode: taskReview",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskEvaluate
 * Agent: chief_qa_engineer_agent
 */
async function taskEvaluate(state: typeof GameBuilderCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chief Software Quality Control Engineer." +
        "\nNode: taskEvaluate",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(GameBuilderCrewAnnotation)
  .addNode("taskCode", taskCode)
  .addNode("taskReview", taskReview)
  .addNode("taskEvaluate", taskEvaluate)
  .addEdge(START, "taskCode")
  .addEdge("taskCode", "taskReview")
  .addEdge("taskReview", "taskEvaluate")
  .addEdge("taskEvaluate", END)
;

export const graph = workflow.compile();
graph.name = "GameBuilderCrew";
// Workflow: wp_sequential
