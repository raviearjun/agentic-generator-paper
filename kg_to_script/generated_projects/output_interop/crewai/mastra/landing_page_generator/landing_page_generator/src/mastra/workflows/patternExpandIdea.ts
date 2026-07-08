/**
 * Workflow: pattern_expand_idea
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { seniorIdeaAnalyst, seniorStrategist } from '../agents'

// ── Workflow Steps ──

const taskExpandIdea = createStep({
  id: 'task_expand_idea',
  description: `THIS IS A GREAT IDEA! Analyze and expand it by conducting a comprehensive research.`,
  inputSchema: z.object({idea: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `THIS IS A GREAT IDEA! Analyze and expand it by conducting a comprehensive research.

Final answer MUST be a comprehensive idea report detailing why this is a great idea, the value proposition, unique selling points, why people should care about it and distinguishing features.

IDEA:
# ----------
${context.idea ?? ''}`
    const result = await seniorIdeaAnalyst.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskRefineIdea = createStep({
  id: 'task_refine_idea',
  description: `Expand idea report with a Why, How, and What messaging strategy using the Golden Circle Communication technique, based on the idea report.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Expand idea report with a Why, How, and What messaging strategy using the Golden Circle Communication technique, based on the idea report.

Your final answer MUST be the updated complete comprehensive idea report with WHY, HOW, WHAT, a core message, key features and supporting arguments.

YOU MUST RETURN THE COMPLETE IDEA REPORT AND THE DETAILS, You'll get a $100 tip if you do your best work!`
    const result = await seniorStrategist.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * pattern_expand_idea
 */
export const patternExpandIdea = createWorkflow({
  id: 'pattern_expand_idea',
  inputSchema: z.object({idea: z.string()}),
  outputSchema: z.object({}),
  steps: [taskExpandIdea, taskRefineIdea],
})
  .then(taskExpandIdea)
  .then(taskRefineIdea)
  .commit()
