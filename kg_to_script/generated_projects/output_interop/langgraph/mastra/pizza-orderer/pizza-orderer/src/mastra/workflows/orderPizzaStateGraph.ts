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
    // You are a helpful AI assistant, tasked with extracting information from the conversation between you, and the user, in order to find a pizza shop for them.
    // This step uses agent: langgraphAnthropicAgent
    // const result = await langgraphAnthropicAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('find_store_task not implemented yet')
  },
})

const orderPizzaTask = createStep({
  id: 'order_pizza_task',
  description: `You are a helpful AI assistant, tasked with placing an order for a pizza for the user.`,
  inputSchema: z.object({}),
  outputSchema: z.object({address: z.string()}),
  execute: async ({ inputData }) => {
    // You are a helpful AI assistant, tasked with placing an order for a pizza for the user.
    // This step uses agent: langgraphAnthropicAgent
    // const result = await langgraphAnthropicAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('order_pizza_task not implemented yet')
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
  outputSchema: z.object({address: z.string()}),
  steps: [findStoreTask, orderPizzaTask],
})
  .then(findStoreTask)
  .then(orderPizzaTask)
  .commit()
