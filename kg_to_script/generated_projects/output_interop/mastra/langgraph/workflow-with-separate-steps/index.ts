import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const MastrainstanceAnnotation = Annotation.Root({
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
        "\n\nYour task: Doubles triggerData.inputValue and returns an object with { doubledValue }." +
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
        "\n\nYour task: Triples triggerData.inputValue and returns an object with { tripledValue }." +
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
        "\n\nYour task: Reads the payload from stepOne (doubledValue) and returns an object with { incrementedValue } which is doubledValue + 1." +
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
        "\n\nYour task: Reads the payload from stepThree (tripledValue) and returns an object with { isEven } indicating whether tripledValue is even." +
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
