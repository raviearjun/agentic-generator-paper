import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const TeamexpandideaAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_search_internet
const tool_search_internet = tool(
  async () => {
    return "Result of tool_search_internet";
  },
  {
    name: "tool_search_internet",
    description: "Search the internet using Serper Dev API and return organic results.",
    schema: z.object({}),
  }
);
// Tool: tool_scrape_and_summarize_website
const tool_scrape_and_summarize_website = tool(
  async () => {
    return "Result of tool_scrape_and_summarize_website";
  },
  {
    name: "tool_scrape_and_summarize_website",
    description: "Scrape website content via Browserless and summarize chunks using internal agent tasks.",
    schema: z.object({}),
  }
);
// Tool: tool_learn_landing_page_options
const tool_learn_landing_page_options = tool(
  async () => {
    return "Result of tool_learn_landing_page_options";
  },
  {
    name: "tool_learn_landing_page_options",
    description: "Read templates configuration and surface available landing page templates.",
    schema: z.object({}),
  }
);
// Tool: tool_copy_landing_page_template
const tool_copy_landing_page_template = tool(
  async () => {
    return "Result of tool_copy_landing_page_template";
  },
  {
    name: "tool_copy_landing_page_template",
    description: "Copy a selected landing page template folder from templates/ into workdir/.",
    schema: z.object({}),
  }
);
// Tool: tool_write_file
const tool_write_file = tool(
  async () => {
    return "Result of tool_write_file";
  },
  {
    name: "tool_write_file",
    description: "Validated write file tool that writes React component and other files into workdir.",
    schema: z.object({}),
  }
);
// Tool: tool_read_file
const tool_read_file = tool(
  async () => {
    return "Result of tool_read_file";
  },
  {
    name: "tool_read_file",
    description: "Read file from the toolkit root_dir (workdir).",
    schema: z.object({}),
  }
);
// Tool: tool_list_directory
const tool_list_directory = tool(
  async () => {
    return "Result of tool_list_directory";
  },
  {
    name: "tool_list_directory",
    description: "List directory contents from the toolkit root_dir (workdir).",
    schema: z.object({}),
  }
);



/**
 * Node: taskExpandIdea
 * Agent: senior_idea_analyst
 */
async function taskExpandIdea(state: typeof TeamexpandideaAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior Idea Analyst." +
        "\nNode: taskExpandIdea",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskRefineIdea
 * Agent: senior_strategist
 */
async function taskRefineIdea(state: typeof TeamexpandideaAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior Communications Strategist." +
        "\nNode: taskRefineIdea",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskChooseTemplate
 * Agent: senior_react_engineer
 */
async function taskChooseTemplate(state: typeof TeamexpandideaAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior React Engineer." +
        "\nNode: taskChooseTemplate",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskUpdatePage
 * Agent: senior_react_engineer
 */
async function taskUpdatePage(state: typeof TeamexpandideaAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior React Engineer." +
        "\nNode: taskUpdatePage",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskComponentContent
 * Agent: senior_content_editor
 */
async function taskComponentContent(state: typeof TeamexpandideaAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior Content Editor." +
        "\nNode: taskComponentContent",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskUpdateComponent
 * Agent: senior_content_editor
 */
async function taskUpdateComponent(state: typeof TeamexpandideaAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior Content Editor." +
        "\nNode: taskUpdateComponent",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskQaComponent
 * Agent: senior_content_editor
 */
async function taskQaComponent(state: typeof TeamexpandideaAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Senior Content Editor." +
        "\nNode: taskQaComponent",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(TeamexpandideaAnnotation)
  .addNode("taskExpandIdea", taskExpandIdea)
  .addNode("taskRefineIdea", taskRefineIdea)
  .addNode("taskChooseTemplate", taskChooseTemplate)
  .addNode("taskUpdatePage", taskUpdatePage)
  .addNode("taskComponentContent", taskComponentContent)
  .addNode("taskUpdateComponent", taskUpdateComponent)
  .addNode("taskQaComponent", taskQaComponent)
  .addEdge(START, "taskExpandIdea")
  .addEdge("taskExpandIdea", "taskRefineIdea")
  .addEdge("taskChooseTemplate", "taskUpdatePage")
  .addEdge("taskComponentContent", "taskUpdateComponent")
  .addEdge("taskUpdateComponent", "taskQaComponent")
  .addEdge("taskRefineIdea", END)
  .addEdge("taskUpdatePage", END)
  .addEdge("taskQaComponent", END)
;

export const graph = workflow.compile();
graph.name = "teamexpandidea";
// Workflow: pattern_expand_idea
// Workflow: pattern_choose_template
// Workflow: pattern_create_content
