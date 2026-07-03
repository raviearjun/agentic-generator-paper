import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const GroupChatTeamforBlogGenerationAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
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
