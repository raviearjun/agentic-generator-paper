import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const GameBuilderCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: You will create a game using python, these are the instructions:\n\nInstructions\n# ------------\n{game}" +
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
        "\n\nYour task: You will create a game using python, these are the instructions:\n\nInstructions\n# ------------\n{game}\n\nUsing the code you got, check for errors. Check for logic errors,\nsyntax errors, missing imports, variable declarations, mismatched brackets,\nand security vulnerabilities." +
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
        "\n\nYour task: You are helping create a game using python, these are the instructions:\n\nInstructions\n# ------------\n{game}\n\nYou will look over the code to insure that it is complete and\ndoes the job that it is supposed to do." +
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
