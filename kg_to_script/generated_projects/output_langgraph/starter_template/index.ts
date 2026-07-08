import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const CustomCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: Do something as part of task 1\n\nIf you do your BEST WORK, I'll give you a $10,000 commission!\n\nMake sure to use the most recent data as possible.\n\nUse this variable: {var1}\nAnd also this variable: {var2}" +
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
        "\n\nYour task: Take the input from task 1 and do something with it.\n\nIf you do your BEST WORK, I'll give you a $10,000 commission!\n\nMake sure to do something else." +
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
