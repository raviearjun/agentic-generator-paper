import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const OnboardingTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
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
