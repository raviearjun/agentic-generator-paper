/**
 * Workflow: markdown_validation_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow pattern for the markdown validation crew (Process.sequential)
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { requirementsManager } from '../agents'

// ── Workflow Steps ──

const syntaxReviewTask = createStep({
  id: 'syntax_review_task',
  description: `Use the markdown_validation_tool to review the file(s) at this path: {filename}.`,
  inputSchema: z.object({filename: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Use the markdown_validation_tool to review the file(s) at this path: ${context.filename ?? ''}.
Be sure to pass only the file path to the markdown_validation_tool.
Use the following format to call the markdown_validation_tool:
Do I need to use a tool? Yes
Action: markdown_validation_tool
Action Input: ${context.filename ?? ''}

Get the validation results from the tool and then summarize it into a list of changes
the developer should make to the document.
DO NOT recommend ways to update the document.
DO NOT change any of the content of the document or add content to it.
It is critical to your task to only respond with a list of changes.

If you already know the answer or if you do not need to use a tool,
return it as your Final Answer.`
    const result = await requirementsManager.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * markdown_validation_workflow
 *
 * Workflow pattern for the markdown validation crew (Process.sequential)
 */
export const markdownValidationWorkflow = createWorkflow({
  id: 'markdown_validation_workflow',
  inputSchema: z.object({filename: z.string()}),
  outputSchema: z.object({}),
  steps: [syntaxReviewTask],
})
  .parallel([syntaxReviewTask])
  .commit()
