import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const MarkDownValidatorCrewAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\\n\\nYour task: Use the markdown_validation_tool to review the file(s) at this path: {filename}.\nBe sure to pass only the file path to the markdown_validation_tool.\nUse the following format to call the markdown_validation_tool:\nDo I need to use a tool? Yes\nAction: markdown_validation_tool\nAction Input: {filename}\n\nGet the validation results from the tool and then summarize it into a list of changes\nthe developer should make to the document.\nDO NOT recommend ways to update the document.\nDO NOT change any of the content of the document or add content to it.\nIt is critical to your task to only respond with a list of changes.\n\nIf you already know the answer or if you do not need to use a tool,\nreturn it as your Final Answer." +
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
