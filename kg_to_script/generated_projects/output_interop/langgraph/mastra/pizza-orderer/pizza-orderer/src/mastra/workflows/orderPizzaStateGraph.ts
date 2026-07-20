/**
 * Workflow: order_pizza_state_graph
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Order Pizza Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { langgraphAnthropicAgent } from '../agents'

// ── Workflow Steps ──

const findStoreTask = createStep({
  id: 'find_store_task',
  description: `You are a helpful AI assistant, tasked with extracting information from the conversation between you, and the user, in order to find a pizza shop for them.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You are a helpful AI assistant, tasked with extracting information from the conversation between you, and the user, in order to find a pizza shop for them.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await langgraphAnthropicAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const orderPizzaTask = createStep({
  id: 'order_pizza_task',
  description: `You are a helpful AI assistant, tasked with placing an order for a pizza for the user.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You are a helpful AI assistant, tasked with placing an order for a pizza for the user.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await langgraphAnthropicAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * order_pizza_state_graph
 *
 * Order Pizza Graph
 */
export const orderPizzaStateGraph = createWorkflow({
  id: 'order_pizza_state_graph',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [findStoreTask, orderPizzaTask],
})
  .then(findStoreTask)
  .then(orderPizzaTask)
  .commit()
