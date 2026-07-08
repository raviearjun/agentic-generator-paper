import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const MastraruntimeAnnotation = Annotation.Root({
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
 * Agent: mastra_default_agent
 */
async function taskStepOne(state: typeof MastraruntimeAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-executor." +
        "\n\nYour task: Execute: doubledValue = context.machineContext.triggerData.inputValue * 2" +
        "\nNode: taskStepOne",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStepTwo
 * Agent: mastra_default_agent
 */
async function taskStepTwo(state: typeof MastraruntimeAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a workflow-executor." +
        "\n\nYour task: If context.machineContext.stepResults.stepOne.status == 'success' then incrementedValue = context.machineContext.stepResults.stepOne.payload.doubledValue + 1 else incrementedValue = 0" +
        "\nNode: taskStepTwo",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastraruntimeAnnotation)
  .addNode("taskStepOne", taskStepOne)
  .addNode("taskStepTwo", taskStepTwo)
  .addEdge(START, "taskStepOne")
  .addEdge("taskStepOne", "taskStepTwo")
  .addEdge("taskStepTwo", END)
;

export const graph = workflow.compile();
graph.name = "mastraruntime";
// Workflow: my_workflow
