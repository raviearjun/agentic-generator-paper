import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MastrainstanceAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_get_cat_facts
const tool_get_cat_facts = tool(
  async () => {
    return "Result of tool_get_cat_facts";
  },
  {
    name: "tool_get_cat_facts",
    description: "Fetches cat facts",
    schema: z.object({}),
  }
);



/**
 * Node: taskStepOne
 * Agent: cat_one
 */
async function taskStepOne(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskStepOne",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStepTwo
 * Agent: cat_one
 */
async function taskStepTwo(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskStepTwo",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStepThree
 * Agent: cat_one
 */
async function taskStepThree(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskStepThree",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStepFour
 * Agent: cat_one
 */
async function taskStepFour(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskStepFour",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskStepFive
 * Agent: cat_one
 */
async function taskStepFive(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskStepFive",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskParStepOne
 * Agent: cat_one
 */
async function taskParStepOne(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskParStepOne",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskParStepSix
 * Agent: cat_one
 */
async function taskParStepSix(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskParStepSix",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskParStepTwo
 * Agent: cat_one
 */
async function taskParStepTwo(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskParStepTwo",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskParStepThree
 * Agent: cat_one
 */
async function taskParStepThree(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskParStepThree",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskBrStepOne
 * Agent: cat_one
 */
async function taskBrStepOne(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskBrStepOne",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskBrStepTwo
 * Agent: cat_one
 */
async function taskBrStepTwo(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskBrStepTwo",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskBrStepFour
 * Agent: cat_one
 */
async function taskBrStepFour(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskBrStepFour",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskBrStepThree
 * Agent: cat_one
 */
async function taskBrStepThree(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskBrStepThree",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskBrStepFive
 * Agent: cat_one
 */
async function taskBrStepFive(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskBrStepFive",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCycStepOne
 * Agent: cat_one
 */
async function taskCycStepOne(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskCycStepOne",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCycStepTwo
 * Agent: cat_one
 */
async function taskCycStepTwo(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskCycStepTwo",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCycStepThree
 * Agent: cat_one
 */
async function taskCycStepThree(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskCycStepThree",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCycStepOneLoop
 * Agent: cat_one
 */
async function taskCycStepOneLoop(state: typeof MastrainstanceAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a feline-expert." +
        "\nNode: taskCycStepOneLoop",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MastrainstanceAnnotation)
  .addNode("taskStepOne", taskStepOne)
  .addNode("taskStepTwo", taskStepTwo)
  .addNode("taskStepThree", taskStepThree)
  .addNode("taskStepFour", taskStepFour)
  .addNode("taskStepFive", taskStepFive)
  .addNode("taskParStepOne", taskParStepOne)
  .addNode("taskParStepSix", taskParStepSix)
  .addNode("taskParStepTwo", taskParStepTwo)
  .addNode("taskParStepThree", taskParStepThree)
  .addNode("taskBrStepOne", taskBrStepOne)
  .addNode("taskBrStepTwo", taskBrStepTwo)
  .addNode("taskBrStepFour", taskBrStepFour)
  .addNode("taskBrStepThree", taskBrStepThree)
  .addNode("taskBrStepFive", taskBrStepFive)
  .addNode("taskCycStepOne", taskCycStepOne)
  .addNode("taskCycStepTwo", taskCycStepTwo)
  .addNode("taskCycStepThree", taskCycStepThree)
  .addNode("taskCycStepOneLoop", taskCycStepOneLoop)
  .addEdge(START, "taskStepOne")
  .addEdge("taskStepOne", "taskStepTwo")
  .addEdge("taskStepTwo", "taskStepThree")
  .addEdge("taskStepThree", "taskStepFour")
  .addEdge("taskStepFour", "taskStepFive")
  .addEdge("taskParStepOne", "taskParStepSix")
  .addEdge("taskParStepOne", "taskParStepTwo")
  .addEdge("taskBrStepOne", "taskBrStepTwo")
  .addEdge("taskBrStepOne", "taskBrStepThree")
  .addEdge("taskBrStepTwo", "taskBrStepFour")
  .addEdge("taskBrStepThree", "taskBrStepFive")
  .addEdge("taskCycStepOne", "taskCycStepTwo")
  .addEdge("taskCycStepTwo", "taskCycStepThree")
  .addEdge("taskCycStepThree", "taskCycStepOneLoop")
  .addEdge("taskStepFive", END)
  .addEdge("taskParStepSix", END)
  .addEdge("taskParStepTwo", END)
  .addEdge("taskParStepThree", END)
  .addEdge("taskBrStepFour", END)
  .addEdge("taskBrStepFive", END)
  .addEdge("taskCycStepOneLoop", END)
;

export const graph = workflow.compile();
graph.name = "mastrainstance";
// Workflow: wf_sequential
// Workflow: wf_parallel
// Workflow: wf_branched
// Workflow: wf_cyclical
