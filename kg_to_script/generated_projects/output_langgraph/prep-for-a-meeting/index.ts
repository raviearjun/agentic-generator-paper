import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MeetingPreparationCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: Conduct comprehensive research on each of the individuals and companies\ninvolved in the upcoming meeting. Gather information on recent\nnews, achievements, professional background, and any relevant\nbusiness activities.\n\nParticipants: {participants}\nMeeting Context: {context}" +
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
        "\n\nYour task: Analyze the current industry trends, challenges, and opportunities\nrelevant to the meeting's context. Consider market reports, recent\ndevelopments, and expert opinions to provide a comprehensive\noverview of the industry landscape.\n\nParticipants: {participants}\nMeeting Context: {context}" +
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
        "\n\nYour task: Develop strategic talking points, questions, and discussion angles\nfor the meeting based on the research and industry analysis conducted\n\nMeeting Context: {context}\nMeeting Objective: {objective}" +
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
        "\n\nYour task: Compile all the research findings, industry analysis, and strategic\ntalking points into a concise, comprehensive briefing document for\nthe meeting.\nEnsure the briefing is easy to digest and equips the meeting\nparticipants with all necessary information and strategies.\n\nMeeting Context: {context}\nMeeting Objective: {objective}" +
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
