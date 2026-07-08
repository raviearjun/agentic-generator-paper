/**
 * Workflow: wp_stategraph
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { chatAgent } from '../agents'

// ── Workflow Steps ──

const taskChat = createStep({
  id: 'task_chat',
  description: `Invoke model with the system prompt and current state.messages; return response messages.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Invoke model with the system prompt and current state.messages; return response messages.`
    const result = await chatAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wp_stategraph
 */
export const wpStategraph = createWorkflow({
  id: 'wp_stategraph',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskChat],
})
  .parallel([taskChat])
  .commit()
