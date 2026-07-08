import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const OnboardingTeamAnnotation = Annotation.Root({
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
 * Node: taskOnboardingPersonalInfo
 * Agent: onboarding_personal_information_agent
 */
async function taskOnboardingPersonalInfo(state: typeof OnboardingTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a onboarding_personal_information." +
        "\n\nYour task: Hello, I'm here to help you get started with our product. Could you tell me your name and location?" +
        "\nNode: taskOnboardingPersonalInfo",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskOnboardingTopicPreference
 * Agent: onboarding_topic_preference_agent
 */
async function taskOnboardingTopicPreference(state: typeof OnboardingTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a onboarding_topic_preference." +
        "\n\nYour task: Great! Could you tell me what topics you are interested in reading about?" +
        "\nNode: taskOnboardingTopicPreference",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCustomerEngagementRequest
 * Agent: customer_engagement_agent
 */
async function taskCustomerEngagementRequest(state: typeof OnboardingTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a customer_engagement." +
        "\n\nYour task: Let's find something fun to read." +
        "\nNode: taskCustomerEngagementRequest",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(OnboardingTeamAnnotation)
  .addNode("taskOnboardingPersonalInfo", taskOnboardingPersonalInfo)
  .addNode("taskOnboardingTopicPreference", taskOnboardingTopicPreference)
  .addNode("taskCustomerEngagementRequest", taskCustomerEngagementRequest)
  .addEdge(START, "taskOnboardingPersonalInfo")
  .addEdge("taskOnboardingPersonalInfo", "taskOnboardingTopicPreference")
  .addEdge("taskOnboardingTopicPreference", "taskCustomerEngagementRequest")
  .addEdge("taskCustomerEngagementRequest", END)
;

export const graph = workflow.compile();
graph.name = "OnboardingTeam";
// Workflow: onboarding_workflow
