import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const StateGraphTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});



// Define Agent: chat_agent
const chat_agent = async (state: typeof StateGraphTeamAnnotation.State) => {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a assistant."
        + "\n\nYour task: Invoke model with the system prompt and current state.messages; return response messages."
      ,
    },
    ...state.messages,
  ]);
  return { messages: [response] };
};

const workflow = new StateGraph(StateGraphTeamAnnotation)
  .addNode("taskChat", chat_agent)
  .addEdge(START, "taskChat")
  .addEdge("taskChat", END);

export const graph = workflow.compile();
graph.name = "StateGraphTeam";
// Workflow: wp_stategraph
