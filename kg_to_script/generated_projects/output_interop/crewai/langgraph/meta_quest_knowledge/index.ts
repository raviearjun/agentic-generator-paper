import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const MetaQuestKnowledgeCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});



// Define Agent: meta_quest_expert
const meta_quest_expert = async (state: typeof MetaQuestKnowledgeCrewAnnotation.State) => {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    { role: "system", content: "You are a Meta Quest Expert." },
    ...state.messages,
  ]);
  return { messages: [response] };
};

const graph = new StateGraph(MetaQuestKnowledgeCrewAnnotation)
  .addNode("answerQuestionTask", meta_quest_expert)
  .addEdge(START, "answerQuestionTask")
  .addEdge("answerQuestionTask", END);

export const agent = graph.compile();
agent.name = "MetaQuestKnowledgeCrew";
// Workflow: sequential_pattern
