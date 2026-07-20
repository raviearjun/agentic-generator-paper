/**
 * Workflow: writer_state_graph_pattern
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { writerAgent } from '../agents'

// ── Workflow Steps ──

const taskPrepare = createStep({
  id: 'task_prepare',
  description: `Prepare a text document for the user with a short title and short description for browsing purposes. Can be also used when creating a new version of the document.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Prepare a text document for the user with a short title and short description for browsing purposes. Can be also used when creating a new version of the document.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await writerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskWriter = createStep({
  id: 'task_writer',
  description: `Write a text document based on the user's request. Only output the content, do not ask any additional questions. If there is selected text in state.context.writer.selected, include that context in the generation.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Write a text document based on the user's request. Only output the content, do not ask any additional questions. If there is selected text in state.context.writer.selected, include that context in the generation.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await writerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskSuggestions = createStep({
  id: 'task_suggestions',
  description: `Invoke the model on the conversation messages (including tool finished signals) to produce the finish/suggestions message; append the resulting model output to the message stream.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Invoke the model on the conversation messages (including tool finished signals) to produce the finish/suggestions message; append the resulting model output to the message stream.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await writerAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * writer_state_graph_pattern
 */
export const writerStateGraphPattern = createWorkflow({
  id: 'writer_state_graph_pattern',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskPrepare, taskWriter, taskSuggestions],
})
  .then(taskPrepare)
  .then(taskWriter)
  .then(taskSuggestions)
  .commit()
