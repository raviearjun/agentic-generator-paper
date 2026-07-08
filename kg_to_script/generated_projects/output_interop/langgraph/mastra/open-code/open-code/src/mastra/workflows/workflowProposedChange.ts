/**
 * Workflow: workflow_proposed_change
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow capturing the lifecycle of a proposed code change: display, user decision, tool call, finalize.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { langgraphAgent } from '../agents'

// ── Workflow Steps ──

const taskProposeChange = createStep({
  id: 'task_propose_change',
  description: `Render the proposed change (code diff / description) to the user and request an explicit accept or reject decision.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Render the proposed change (code diff / description) to the user and request an explicit accept or reject decision.`
    const result = await langgraphAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskUserDecision = createStep({
  id: 'task_user_decision',
  description: `User evaluates the proposed change and selects accept or reject; the selection drives subsequent tool calls and UI state.`,
  inputSchema: z.object({}),
  outputSchema: z.object({On_reject: z.string()}),
  execute: async ({ inputData }) => {
    // User evaluates the proposed change and selects accept or reject; the selection drives subsequent tool calls and UI state.
    // TODO: Implement step logic
    throw new Error('task_user_decision not implemented yet')
  },
})

const taskHandleReject = createStep({
  id: 'task_handle_reject',
  description: `On reject: call the update_file tool with REJECTED_CHANGE_CONTENT (or do not apply change) and submit a human message 'Rejected change.'.`,
  inputSchema: z.object({On_reject: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `On reject: call the update_file tool with REJECTED_CHANGE_CONTENT (or do not apply change) and submit a human message 'Rejected change.'.`
    const result = await langgraphAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskFinalizeUi = createStep({
  id: 'task_finalize_ui',
  description: `Render final accepted or rejected status in the UI and present an artifact view of the proposed change.`,
  inputSchema: z.object({}),
  outputSchema: z.object({Final_UI_state: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Render final accepted or rejected status in the UI and present an artifact view of the proposed change.`
    const result = await langgraphAgent.generate(prompt)
    return {
      ...context,
      Final_UI_state: context.Final_UI_state ?? result.text,
    }
  },
})

// ── Workflow Definition ──

/**
 * workflow_proposed_change
 *
 * Workflow capturing the lifecycle of a proposed code change: display, user decision, tool call, finalize.
 */
export const workflowProposedChange = createWorkflow({
  id: 'workflow_proposed_change',
  inputSchema: z.object({}),
  outputSchema: z.object({Final_UI_state: z.string()}),
  steps: [taskProposeChange, taskUserDecision, taskHandleReject, taskFinalizeUi],
})
  .then(taskProposeChange)
  .then(taskUserDecision)
  .then(taskHandleReject)
  .then(taskFinalizeUi)
  .commit()
