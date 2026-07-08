/**
 * Workflow: stock_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { stockAgent } from '../agents'

// Import tools used by workflow steps
import { stockPricesTool } from '../tools'

// ── Workflow Steps ──

const taskInit = createStep({
  id: 'task_init',
  description: `Initialize the Stock Agent before handling requests.`,
  inputSchema: z.object({}),
  outputSchema: z.object({symbol: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Initialize the Stock Agent before handling requests.`
    const result = await stockAgent.generate(prompt)
    return {
      ...context,
      symbol: context.symbol ?? result.text,
    }
  },
})

const taskQuery = createStep({
  id: 'task_query',
  description: `What is the current stock price of Apple (AAPL)?`,
  inputSchema: z.object({symbol: z.string()}),
  outputSchema: z.object({symbol: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `What is the current stock price of Apple (AAPL)?`
    const result = await stockAgent.generate(prompt)
    return {
      ...context,
      symbol: context.symbol ?? result.text,
    }
  },
})

const taskToolCall = createStep({
  id: 'task_tool_call',
  description: `Call the stockPrices tool with symbol 'AAPL' to fetch the latest closing price.`,
  inputSchema: z.object({symbol: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Call the stockPrices tool with symbol 'AAPL' to fetch the latest closing price.`
    const result = await stockAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskEnd = createStep({
  id: 'task_end',
  description: `Return the formatted current price to the user.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Return the formatted current price to the user.`
    const result = await stockAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * stock_workflow
 */
export const stockWorkflow = createWorkflow({
  id: 'stock_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskInit, taskQuery, taskToolCall, taskEnd],
})
  .then(taskInit)
  .then(taskQuery)
  .then(taskToolCall)
  .then(taskEnd)
  .commit()
