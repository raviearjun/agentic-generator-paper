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
  description: `让我们下棋吧，该你走了！`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `让我们下棋吧，该你走了！`
    const result = await playerBlack.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskBoardProxySummaryToWhite = createStep({
  id: 'task_board_proxy_summary_to_white',
  description: `Summary of last board state and last move (provided by board proxy).`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Summary of last board state and last move (provided by board proxy).`
    const result = await boardProxy.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGetLegalMoves = createStep({
  id: 'task_get_legal_moves',
  description: `调用 get_legal_moves() 获取当前合法走法列表（UCI 格式）。`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `调用 get_legal_moves() 获取当前合法走法列表（UCI 格式）。`
    const result = await playerWhite.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskMakeMove = createStep({
  id: 'task_make_move',
  description: `选择一个合法走法并调用 make_move(move) 来执行该步棋。`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `选择一个合法走法并调用 make_move(move) 来执行该步棋。`
    const result = await playerWhite.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskCheckMadeMove = createStep({
  id: 'task_check_made_move',
  description: `Call check_made_move(msg) to determine if a move has been executed; if true, end nested chat iteration.`,
  inputSchema: z.object({}),
  outputSchema: z.object({Boolean: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call check_made_move(msg) to determine if a move has been executed; if true, end nested chat iteration.`
    const result = await boardProxy.generate(prompt)
    return {
      ...context,
      Boolean: context.Boolean ?? result.text,
    }
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
