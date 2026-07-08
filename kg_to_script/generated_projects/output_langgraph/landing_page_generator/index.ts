import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const TeamexpandideaAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: THIS IS A GREAT IDEA! Analyze and expand it by conducting a comprehensive research.\n\nFinal answer MUST be a comprehensive idea report detailing why this is a great idea, the value proposition, unique selling points, why people should care about it and distinguishing features.\n\nIDEA:\n# ----------\n{idea}" +
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
        "\n\nYour task: Expand idea report with a Why, How, and What messaging strategy using the Golden Circle Communication technique, based on the idea report.\n\nYour final answer MUST be the updated complete comprehensive idea report with WHY, HOW, WHAT, a core message, key features and supporting arguments.\n\nYOU MUST RETURN THE COMPLETE IDEA REPORT AND THE DETAILS, You'll get a $100 tip if you do your best work!" +
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
        "\n\nYour task: Learn the templates options choose and copy the one that suits the idea below the best, YOU MUST COPY, and then YOU MUST read the src/component in the directory you just copied, to decide what component files should be updated to make the landing page about the idea below.\n\n- YOU MUST READ THE DIRECTORY BEFORE CHOOSING THE FILES.\n- YOU MUST NOT UPDATE any Pricing components.\n- YOU MUST UPDATE ONLY the 4 most important components.\n\nYour final answer MUST be ONLY a JSON array of components full file paths that need to be updated.\n\nIDEA\n# ----------\n{idea}" +
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
        "\n\nYour task: READ the ./[chosen_template]/src/app/page.jsx OR ./[chosen_template]/src/app/(main)/page.jsx to learn its content and then write an updated version to the filesystem that removes any section related components that are not in our list from the returns. Keep the imports.\n\nFinal answer MUST BE ONLY a valid json list with the full path of each of the components we will be using, the same way you got them.\n\nRULES\n# -----\n- NEVER ADD A FINAL DOT to the file content.\n- NEVER WRITE \\n (newlines as string) on the file, just the code.\n- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.\n- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.\n- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.\n- Save the file as with \`.jsx\` extension.\n- Return the same valid JSON list of the components your got.\n\nYou'll get a $100 tip if you follow all the rules!\n\nAlso update any necessary text to reflect this landing page is about the idea below.\n\nIDEA\n# ----------\n{idea}" +
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
        "\n\nYour task: A engineer will update the {component} (code below), return a list of good options of texts to replace EACH INDIVIDUAL existing text on the component, the suggestion MUST be based on the idea below, and also MUST be similar in length with the original text, we need to replace ALL TEXT.\n\nNEVER USE Apostrophes for contraction! You'll get a $100 tip if you do your best work!\n\nIDEA\n# -----\n{expanded_idea}\n\nREACT COMPONENT CONTENT\n# -----\n{file_content}" +
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
        "\n\nYour task: YOU MUST USE the tool to write an updated version of the react component to the file system in the following path: {component} replacing the text content with the suggestions provided.\n\nYou only modify the text content, you don't add or remove any components.\n\nRULES\n# -----\n- Remove all the links, this should be single page landing page.\n- Don't make up images, videos, gifs, icons, logos, etc.\n- keep the same style and tailwind classes.\n- MUST HAVE 'use client' at the be beginning of the code.\n- href in buttons, links, NavLinks, and navigations should be \`#\`.\n- NEVER WRITE \\n (newlines as string) on the file, just the code.\n- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.\n- Keep the same component imports and don't use new components.\n- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.\n- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.\n- Save the file as with \`.jsx\` extension.\n\nIf you follow the rules I'll give you a $100 tip!!! MY LIFE DEPEND ON YOU FOLLOWING IT!\n\nCONTENT TO BE UPDATED\n# -----\n{file_content}" +
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
        "\n\nYour task: Check the React component code to make sure it's valid and abide by the rules below, if it doesn't then write the correct version to the file system using the write file tool into the following path: {component}.\n\nYour final answer should be a confirmation that the component is valid and abides by the rules and if you had to write an updated version to the file system.\n\nRULES\n# -----\n- NEVER USE Apostrophes for contraction!\n- ALL COMPONENTS USED SHOULD BE IMPORTED.\n- MUST HAVE 'use client' at the be beginning of the code.\n- href in buttons, links, NavLinks, and navigations should be \`#\`.\n- NEVER WRITE \\n (newlines as string) on the file, just the code.\n- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.\n- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.\n- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.\n- Always use \`export function\` for the component class.\n\nYou'll get a $100 tip if you follow all the rules!" +
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
