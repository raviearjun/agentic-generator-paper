import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const RegistryRegistryMCPServerAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
    default: () => [],
  }),
});

// Tool: tool_registry_list
const tool_registry_list = tool(
  async () => {
    return "Result of tool_registry_list";
  },
  {
    name: "tool_registry_list",
    description: "List available MCP registries. Can filter by ID, tag, or name and provide detailed or summary views.",
    schema: z.object({}),
  }
);
// Tool: tool_registry_servers
const tool_registry_servers = tool(
  async () => {
    return "Result of tool_registry_servers";
  },
  {
    name: "tool_registry_servers",
    description: "Get servers from a specific MCP registry. Can filter by tag or search term. Internally fetches registry data, invokes post-processing, and filters results.",
    schema: z.object({}),
  }
);



/**
 * Node: taskFetchServersFromRegistry
 * Agent: registry_registry_server
 */
async function taskFetchServersFromRegistry(state: typeof RegistryRegistryMCPServerAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a mcp-server." +
        "\n\nYour task: Fetch servers from the registry by locating the registry entry in local registryData, verifying servers_url, performing HTTP GET, and returning raw response for post-processing." +
        "\nNode: taskFetchServersFromRegistry",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskPostProcessServers
 * Agent: registry_registry_server
 */
async function taskPostProcessServers(state: typeof RegistryRegistryMCPServerAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a mcp-server." +
        "\n\nYour task: Normalize registry-specific response formats into canonical ServerEntry objects with id, name, description, createdAt, updatedAt using the registry's postProcessServers function when available." +
        "\nNode: taskPostProcessServers",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskFilterServers
 * Agent: registry_registry_server
 */
async function taskFilterServers(state: typeof RegistryRegistryMCPServerAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a mcp-server." +
        "\n\nYour task: Apply search filtering on server name or description; support tag-based filtering when server metadata includes tags." +
        "\nNode: taskFilterServers",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGetServersFromRegistry
 * Agent: registry_registry_server
 */
async function taskGetServersFromRegistry(state: typeof RegistryRegistryMCPServerAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a mcp-server." +
        "\n\nYour task: Orchestrate fetching, post-processing, and filtering of servers for a given registryId and optional filters; return final server list or throw on error." +
        "\nNode: taskGetServersFromRegistry",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(RegistryRegistryMCPServerAnnotation)
  .addNode("taskFetchServersFromRegistry", taskFetchServersFromRegistry)
  .addNode("taskPostProcessServers", taskPostProcessServers)
  .addNode("taskFilterServers", taskFilterServers)
  .addNode("taskGetServersFromRegistry", taskGetServersFromRegistry)
  .addEdge(START, "taskFetchServersFromRegistry")
  .addEdge("taskFetchServersFromRegistry", "taskPostProcessServers")
  .addEdge("taskPostProcessServers", "taskFilterServers")
  .addEdge("taskFilterServers", "taskGetServersFromRegistry")
  .addEdge("taskGetServersFromRegistry", END)
;

export const graph = workflow.compile();
graph.name = "RegistryRegistryMCPServer";
// Workflow: workflow_registry_servers
