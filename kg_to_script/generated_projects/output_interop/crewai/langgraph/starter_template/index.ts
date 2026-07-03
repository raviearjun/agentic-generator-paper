import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const CustomCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_duck_duck_go_search_run
const tool_duck_duck_go_search_run = tool(
  async () => {
    return "Result of tool_duck_duck_go_search_run";
  },
  {
    name: "tool_duck_duck_go_search_run",
    description: "LangChain DuckDuckGo search tool used for web search",
    schema: z.object({}),
  }
);



/**
 * Node: task1
 * Agent: agent_1_name
 */
async function task1(state: typeof CustomCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Define agent 1 role here." +
        "\nNode: task1",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: task2
 * Agent: agent_2_name
 */
async function task2(state: typeof CustomCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Define agent 2 role here." +
        "\nNode: task2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(CustomCrewAnnotation)
  .addNode("task1", task1)
  .addNode("task2", task2)
  .addEdge(START, "task1")
  .addEdge("task1", "task2")
  .addEdge("task2", END)
;

export const graph = workflow.compile();
graph.name = "CustomCrew";
// Workflow: workflow_custom_crew
