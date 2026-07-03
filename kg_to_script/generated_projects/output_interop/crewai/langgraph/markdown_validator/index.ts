import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MarkDownValidatorCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: markdown_validation_tool
const markdown_validation_tool = tool(
  async () => {
    return "Result of markdown_validation_tool";
  },
  {
    name: "markdown_validation_tool",
    description: "A tool to review files for markdown syntax errors. Uses PyMarkdownApi to scan a file path and returns formatted scan results.",
    schema: z.object({}),
  }
);



/**
 * Node: syntaxReviewTask
 * Agent: requirements_manager
 */
async function syntaxReviewTask(state: typeof MarkDownValidatorCrewAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Requirements Manager." +
        "\\nNode: syntaxReviewTask",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(MarkDownValidatorCrewAnnotation)
  .addNode("syntaxReviewTask", syntaxReviewTask)
  .addEdge(START, "syntaxReviewTask")
  .addEdge("syntaxReviewTask", END)
;

export const graph = workflow.compile();
graph.name = "MarkDownValidatorCrew";
// Workflow: markdown_validation_workflow
