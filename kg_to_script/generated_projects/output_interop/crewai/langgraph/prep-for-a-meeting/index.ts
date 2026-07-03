import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MeetingPreparationCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: exa_search_tool_search
const exa_search_tool_search = tool(
  async () => {
    return "Result of exa_search_tool_search";
  },
  {
    name: "exa_search_tool_search",
    description: "Search for a webpage based on the query (returns a list of result IDs).",
    schema: z.object({}),
  }
);
// Tool: exa_search_tool_find_similar
const exa_search_tool_find_similar = tool(
  async () => {
    return "Result of exa_search_tool_find_similar";
  },
  {
    name: "exa_search_tool_find_similar",
    description: "Search for webpages similar to a given URL.",
    schema: z.object({}),
  }
);
// Tool: exa_search_tool_get_contents
const exa_search_tool_get_contents = tool(
  async () => {
    return "Result of exa_search_tool_get_contents";
  },
  {
    name: "exa_search_tool_get_contents",
    description: "Get the contents of webpages given a list of IDs.",
    schema: z.object({}),
  }
);



/**
 * Node: researchTask
 * Agent: researcher_agent
 */
async function researchTask(state: typeof MeetingPreparationCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Research Specialist." +
        "\nNode: researchTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: industryAnalysisTask
 * Agent: industry_analyst_agent
 */
async function industryAnalysisTask(state: typeof MeetingPreparationCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Industry Analyst." +
        "\nNode: industryAnalysisTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: meetingStrategyTask
 * Agent: meeting_strategy_agent
 */
async function meetingStrategyTask(state: typeof MeetingPreparationCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Meeting Strategy Advisor." +
        "\nNode: meetingStrategyTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: summaryAndBriefingTask
 * Agent: summary_and_briefing_agent
 */
async function summaryAndBriefingTask(state: typeof MeetingPreparationCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Briefing Coordinator." +
        "\nNode: summaryAndBriefingTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MeetingPreparationCrewAnnotation)
  .addNode("researchTask", researchTask)
  .addNode("industryAnalysisTask", industryAnalysisTask)
  .addNode("meetingStrategyTask", meetingStrategyTask)
  .addNode("summaryAndBriefingTask", summaryAndBriefingTask)
  .addEdge(START, "researchTask")
  .addEdge("researchTask", "industryAnalysisTask")
  .addEdge("industryAnalysisTask", "meetingStrategyTask")
  .addEdge("meetingStrategyTask", "summaryAndBriefingTask")
  .addEdge("summaryAndBriefingTask", END)
;

export const graph = workflow.compile();
graph.name = "MeetingPreparationCrew";
// Workflow: meeting_preparation_pattern
