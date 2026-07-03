import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const ConversationalChessTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    reducer: (_, next) => next,
    default: () => [],
  }),
});

// Tool: tool_get_legal_moves
const tool_get_legal_moves = tool(
  async () => {
    return "Result of tool_get_legal_moves";
  },
  {
    name: "tool_get_legal_moves",
    description: "Returns a list of legal moves in UCI format for the current chess board state.",
    schema: z.object({}),
  }
);
// Tool: tool_make_move
const tool_make_move = tool(
  async () => {
    return "Result of tool_make_move";
  },
  {
    name: "tool_make_move",
    description: "Executes a move on the chess board in UCI format and returns a human-readable result string.",
    schema: z.object({}),
  }
);



/**
 * Node: taskInitiateChat
 * Agent: player_black
 */
async function taskInitiateChat(state: typeof ConversationalChessTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chess Player (Black)." +
        "\nNode: taskInitiateChat",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskBoardProxySummaryToWhite
 * Agent: board_proxy
 */
async function taskBoardProxySummaryToWhite(state: typeof ConversationalChessTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Board Proxy / Referee." +
        "\nNode: taskBoardProxySummaryToWhite",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskGetLegalMoves
 * Agent: player_white
 */
async function taskGetLegalMoves(state: typeof ConversationalChessTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chess Player (White)." +
        "\nNode: taskGetLegalMoves",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskMakeMove
 * Agent: player_white
 */
async function taskMakeMove(state: typeof ConversationalChessTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Chess Player (White)." +
        "\nNode: taskMakeMove",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

/**
 * Node: taskCheckMadeMove
 * Agent: board_proxy
 */
async function taskCheckMadeMove(state: typeof ConversationalChessTeamAnnotation.State) {
  const model = new ChatOpenAI({ model: "gpt-4o-mini" });
  const response = await model.invoke([
    {
      role: "system",
      content:
        "You are a Board Proxy / Referee." +
        "\nNode: taskCheckMadeMove",
    },
    ...state.messages,
  ]);
  return { messages: [response] };
}

const workflow = new StateGraph(ConversationalChessTeamAnnotation)
  .addNode("taskInitiateChat", taskInitiateChat)
  .addNode("taskBoardProxySummaryToWhite", taskBoardProxySummaryToWhite)
  .addNode("taskGetLegalMoves", taskGetLegalMoves)
  .addNode("taskMakeMove", taskMakeMove)
  .addNode("taskCheckMadeMove", taskCheckMadeMove)
  .addEdge(START, "taskInitiateChat")
  .addEdge("taskInitiateChat", "taskBoardProxySummaryToWhite")
  .addEdge("taskBoardProxySummaryToWhite", "taskGetLegalMoves")
  .addEdge("taskGetLegalMoves", "taskMakeMove")
  .addEdge("taskMakeMove", "taskCheckMadeMove")
;

export const graph = workflow.compile();
graph.name = "ConversationalChessTeam";
// Workflow: wp_chess_nested
