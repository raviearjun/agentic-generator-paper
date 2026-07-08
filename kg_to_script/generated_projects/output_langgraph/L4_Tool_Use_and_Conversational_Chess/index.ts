import { ChatOpenAI } from "@langchain/openai";
import { Annotation, START, END, StateGraph } from "@langchain/langgraph";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const ConversationalChessTeamAnnotation = Annotation.Root({
  messages: Annotation<any[]>({
    // Append rather than replace: each node only returns its own new
    // message(s), so the reducer must accumulate history across nodes
    // or every node past the first only ever sees the immediately
    // preceding node's output.
    reducer: (prev, next) => prev.concat(next),
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
        "\n\nYour task: 让我们下棋吧，该你走了！" +
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
        "\n\nYour task: Summary of last board state and last move (provided by board proxy)." +
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
        "\n\nYour task: 调用 get_legal_moves() 获取当前合法走法列表（UCI 格式）。" +
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
        "\n\nYour task: 选择一个合法走法并调用 make_move(move) 来执行该步棋。" +
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
        "\n\nYour task: Call check_made_move(msg) to determine if a move has been executed; if true, end nested chat iteration." +
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
