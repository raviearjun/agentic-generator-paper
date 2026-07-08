import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const UnnamedProjectAnnotation = Annotation.Root({
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
 * Node: taskWriteBlog
 * Agent: unnamed
 */
async function taskWriteBlog(state: typeof UnnamedProjectAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Writer." +
        "\n\nYour task: 撰写一篇简洁但引人入胜的博客，内容涉及\n       DeepLearning.AI. 确保博客100 字以内。" +
        "\nNode: taskWriteBlog",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCriticInitiate1
 * Agent: unnamed
 */
async function taskCriticInitiate1(state: typeof UnnamedProjectAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Critic." +
        "\n\nYour task: 撰写一篇简洁但引人入胜的博客，内容涉及\n       DeepLearning.AI. 确保博客100 字以内。" +
        "\nNode: taskCriticInitiate1",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskNestedSeoReview
 * Agent: unnamed
 */
async function taskNestedSeoReview(state: typeof UnnamedProjectAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a SEO Reviewer." +
        "\n\nYour task: 仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}. 这里的 审查员 应该是你自己的角色" +
        "\nNode: taskNestedSeoReview",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskNestedLegalReview
 * Agent: unnamed
 */
async function taskNestedLegalReview(state: typeof UnnamedProjectAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Legal Reviewer." +
        "\n\nYour task: 仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}." +
        "\nNode: taskNestedLegalReview",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskNestedEthicsReview
 * Agent: unnamed
 */
async function taskNestedEthicsReview(state: typeof UnnamedProjectAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Ethics Reviewer." +
        "\n\nYour task: 仅以 JSON 对象的格式返回审查结果  :{'审查员': '', '审查结果': ''}" +
        "\nNode: taskNestedEthicsReview",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskMetaAggregate
 * Agent: unnamed
 */
async function taskMetaAggregate(state: typeof UnnamedProjectAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Meta Reviewer." +
        "\n\nYour task: 对所有审查员的反馈意见进行汇总，并对写作提出最终建议。" +
        "\nNode: taskMetaAggregate",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCriticInitiate2
 * Agent: unnamed
 */
async function taskCriticInitiate2(state: typeof UnnamedProjectAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Critic." +
        "\n\nYour task: 撰写一篇简洁但引人入胜的博客，内容涉及\n       DeepLearning.AI. 确保博客100 字以内。" +
        "\nNode: taskCriticInitiate2",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(UnnamedProjectAnnotation)
  .addNode("taskWriteBlog", taskWriteBlog)
  .addNode("taskCriticInitiate1", taskCriticInitiate1)
  .addNode("taskNestedSeoReview", taskNestedSeoReview)
  .addNode("taskNestedLegalReview", taskNestedLegalReview)
  .addNode("taskNestedEthicsReview", taskNestedEthicsReview)
  .addNode("taskMetaAggregate", taskMetaAggregate)
  .addNode("taskCriticInitiate2", taskCriticInitiate2)
  .addEdge(START, "taskWriteBlog")
  .addEdge("taskWriteBlog", "taskCriticInitiate1")
  .addEdge("taskCriticInitiate1", "taskNestedSeoReview")
  .addEdge("taskNestedSeoReview", "taskNestedLegalReview")
  .addEdge("taskNestedLegalReview", "taskNestedEthicsReview")
  .addEdge("taskNestedEthicsReview", "taskMetaAggregate")
  .addEdge("taskMetaAggregate", "taskCriticInitiate2")
  .addEdge("taskCriticInitiate2", END)
;

export const graph = workflow.compile();
graph.name = "UnnamedProject";
// Workflow: pattern_nested
