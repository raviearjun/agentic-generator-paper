import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";

const MetaQuestKnowledgeCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});



// Define Agent: meta_quest_expert
const meta_quest_expert = async (state: typeof MetaQuestKnowledgeCrewAnnotation.State) => {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Meta Quest Expert."
        + "\n\nYour task: Answer the user question with the most relevant information from the context and available knowledge sources.\nQuestion: {question}\n\nDo not answer questions that are not related to the context or knowledge sources."
      ,
    },
    ...state.messages,
  ]);
  return { messages: [response] };
};

const workflow = new StateGraph(MetaQuestKnowledgeCrewAnnotation)
  .addNode("answerQuestionTask", meta_quest_expert)
  .addEdge(START, "answerQuestionTask")
  .addEdge("answerQuestionTask", END);

export const graph = workflow.compile();
graph.name = "MetaQuestKnowledgeCrew";
// Workflow: sequential_pattern
