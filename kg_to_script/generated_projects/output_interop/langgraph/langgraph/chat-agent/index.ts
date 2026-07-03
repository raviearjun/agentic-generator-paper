import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const StateGraphTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});



// Define Agent: chat_agent
const chat_agent = async (state: typeof StateGraphTeamAnnotation.State) => {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    { role: "system", content: "You are a assistant." },
    ...state.messages,
  ]);
  return { messages: [response] };
};

const graph = new StateGraph(StateGraphTeamAnnotation)
  .addNode("taskChat", chat_agent)
  .addEdge(START, "taskChat")
  .addEdge("taskChat", END);

export const agent = graph.compile();
agent.name = "StateGraphTeam";
// Workflow: wp_stategraph
