import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const MastrainstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});




/**
 * Node: taskStepOne
 * Agent: mastra_agent
 */
async function taskStepOne(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-executor." +
        "\nNode: taskStepOne",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStepThree
 * Agent: mastra_agent
 */
async function taskStepThree(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-executor." +
        "\nNode: taskStepThree",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStepTwo
 * Agent: mastra_agent
 */
async function taskStepTwo(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-executor." +
        "\nNode: taskStepTwo",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStepFour
 * Agent: mastra_agent
 */
async function taskStepFour(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-executor." +
        "\nNode: taskStepFour",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastrainstanceAnnotation)
  .addNode("taskStepOne", taskStepOne)
  .addNode("taskStepThree", taskStepThree)
  .addNode("taskStepTwo", taskStepTwo)
  .addNode("taskStepFour", taskStepFour)
  .addEdge(START, "taskStepOne")
  .addEdge("taskStepOne", "taskStepTwo")
  .addEdge("taskStepThree", "taskStepFour")
  .addEdge("taskStepTwo", END)
  .addEdge("taskStepFour", END)
;

export const graph = workflow.compile();
graph.name = "mastrainstance";
// Workflow: my_workflow_pattern
