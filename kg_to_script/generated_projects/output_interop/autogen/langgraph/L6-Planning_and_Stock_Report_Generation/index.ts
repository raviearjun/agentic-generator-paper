import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const GroupChatTeamforBlogGenerationAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});




/**
 * Node: taskInitiateWriteBlog
 * Agent: admin
 */
async function taskInitiateWriteBlog(state: typeof GroupChatTeamforBlogGenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Admin." +
        "\n\nYour task: Write a blogpost about the stock price performance of Nvidia in the past month. Today's date is 2024-04-23." +
        "\nNode: taskInitiateWriteBlog",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPlannerPlan
 * Agent: planner
 */
async function taskPlannerPlan(state: typeof GroupChatTeamforBlogGenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Planner." +
        "\n\nYour task: Given the blogpost task, determine what information can be retrieved using Python code (e.g., historical prices, volumes) and produce a stepwise plan. After each step is executed, inspect results and direct remaining steps; on failure, suggest workarounds." +
        "\nNode: taskPlannerPlan",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskEngineerWriteCode
 * Agent: engineer
 */
async function taskEngineerWriteCode(state: typeof GroupChatTeamforBlogGenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Engineer." +
        "\n\nYour task: Write Python code to retrieve stock data and produce analysis outputs based on the planner's specifications." +
        "\nNode: taskEngineerWriteCode",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskExecutorRunCode
 * Agent: executor
 */
async function taskExecutorRunCode(state: typeof GroupChatTeamforBlogGenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Executor." +
        "\n\nYour task: Execute the latest code message from the engineer (look back up to last 3 messages for code), store artifacts in the 'coding' directory, and report outputs and errors." +
        "\nNode: taskExecutorRunCode",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskWriterProduceBlog
 * Agent: writer
 */
async function taskWriterProduceBlog(state: typeof GroupChatTeamforBlogGenerationAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Writer." +
        "\n\nYour task: Write a blog post in markdown summarizing Nvidia's stock performance in the past month using provided analysis outputs. Use appropriate titles and place content in a pseudo mdcode block. Accept and apply admin feedback to refine." +
        "\nNode: taskWriterProduceBlog",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(GroupChatTeamforBlogGenerationAnnotation)
  .addNode("taskInitiateWriteBlog", taskInitiateWriteBlog)
  .addNode("taskPlannerPlan", taskPlannerPlan)
  .addNode("taskEngineerWriteCode", taskEngineerWriteCode)
  .addNode("taskExecutorRunCode", taskExecutorRunCode)
  .addNode("taskWriterProduceBlog", taskWriterProduceBlog)
  .addEdge(START, "taskInitiateWriteBlog")
  .addEdge("taskInitiateWriteBlog", "taskPlannerPlan")
  .addEdge("taskPlannerPlan", "taskEngineerWriteCode")
  .addEdge("taskEngineerWriteCode", "taskExecutorRunCode")
  .addEdge("taskExecutorRunCode", "taskWriterProduceBlog")
;

export const graph = workflow.compile();
graph.name = "GroupChatTeamforBlogGeneration";
// Workflow: wp_group_chat1
