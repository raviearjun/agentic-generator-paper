/**
 * Workflow: sequential_pattern
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { metaQuestExpert } from '../agents'

// ── Workflow Steps ──

const answerQuestionTask = createStep({
  id: 'answer_question_task',
  description: `Answer the user question with the most relevant information from the context and available knowledge sources.`,
  inputSchema: z.object({question: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Answer the user question with the most relevant information from the context and available knowledge sources.
Question: ${context.question ?? ''}

Do not answer questions that are not related to the context or knowledge sources.`
    const result = await metaQuestExpert.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * sequential_pattern
 */
export const sequentialPattern = createWorkflow({
  id: 'sequential_pattern',
  inputSchema: z.object({question: z.string()}),
  outputSchema: z.object({}),
  steps: [answerQuestionTask],
})
  .parallel([answerQuestionTask])
  .commit()
