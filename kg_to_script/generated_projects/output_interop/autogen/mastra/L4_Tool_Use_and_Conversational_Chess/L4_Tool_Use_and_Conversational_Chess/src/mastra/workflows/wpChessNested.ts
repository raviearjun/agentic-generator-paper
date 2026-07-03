/**
 * Workflow: wp_chess_nested
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow capturing a turn sequence: initiation -> nested board summary -> get legal moves -> make move -> check termination.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { playerBlack, boardProxy, playerWhite } from '../agents'

// Import tools used by workflow steps
import { toolGetLegalMoves, toolMakeMove } from '../tools'

// ── Workflow Steps ──

const taskInitiateChat = createStep({
  id: 'task_initiate_chat',
  description: `player_black initiates the game chat to start a move sequence.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // 让我们下棋吧，该你走了！
    // This step uses agent: playerBlack
    // const result = await playerBlack.generate('...')
    // TODO: Implement step logic
    throw new Error('task_initiate_chat not implemented yet')
  },
})

const taskBoardProxySummaryToWhite = createStep({
  id: 'task_board_proxy_summary_to_white',
  description: `Board proxy provides last message summary to the white player before the player's turn.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Summary of last board state and last move (provided by board proxy).
    // This step uses agent: boardProxy
    // const result = await boardProxy.generate('...')
    // TODO: Implement step logic
    throw new Error('task_board_proxy_summary_to_white not implemented yet')
  },
})

const taskGetLegalMoves = createStep({
  id: 'task_get_legal_moves',
  description: `Player requests the list of legal moves for selection.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // 调用 get_legal_moves() 获取当前合法走法列表（UCI 格式）。
    // This step uses agent: playerWhite
    // const result = await playerWhite.generate('...')
    // This step uses tool: toolGetLegalMoves
    // TODO: Implement step logic
    throw new Error('task_get_legal_moves not implemented yet')
  },
})

const taskMakeMove = createStep({
  id: 'task_make_move',
  description: `Player makes a selected move by calling make_move(move).`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // 选择一个合法走法并调用 make_move(move) 来执行该步棋。
    // This step uses agent: playerWhite
    // const result = await playerWhite.generate('...')
    // This step uses tool: toolMakeMove
    // TODO: Implement step logic
    throw new Error('task_make_move not implemented yet')
  },
})

const taskCheckMadeMove = createStep({
  id: 'task_check_made_move',
  description: `Board proxy evaluates the made_move flag to determine if the nested chat should terminate.`,
  inputSchema: z.object({}),
  outputSchema: z.object({Boolean: z.string()}),
  execute: async ({ inputData }) => {
    // Call check_made_move(msg) to determine if a move has been executed; if true, end nested chat iteration.
    // This step uses agent: boardProxy
    // const result = await boardProxy.generate('...')
    // TODO: Implement step logic
    throw new Error('task_check_made_move not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * wp_chess_nested
 *
 * Workflow capturing a turn sequence: initiation -> nested board summary -> get legal moves -> make move -> check termination.
 */
export const wpChessNested = createWorkflow({
  id: 'wp_chess_nested',
  inputSchema: z.object({}),
  outputSchema: z.object({Boolean: z.string()}),
  steps: [taskInitiateChat, taskBoardProxySummaryToWhite, taskGetLegalMoves, taskMakeMove, taskCheckMadeMove],
})
  .then(taskInitiateChat)
  .then(taskBoardProxySummaryToWhite)
  .then(taskGetLegalMoves)
  .then(taskMakeMove)
  .then(taskCheckMadeMove)
  .commit()
