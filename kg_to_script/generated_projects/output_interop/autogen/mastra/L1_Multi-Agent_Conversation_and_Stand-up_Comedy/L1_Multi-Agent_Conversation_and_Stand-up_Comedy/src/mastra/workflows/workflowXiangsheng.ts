/**
 * Workflow: workflow_xiangsheng
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * High-level workflow capturing initiation, summary, and follow-up interactions for the stand-up duo.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { unnamed } from '../agents'

// ── Workflow Steps ──

const taskGuodegangInitiateChat1 = createStep({
  id: 'task_guodegang_initiate_chat_1',
  description: `message="我是郭德纲，于谦呀，我们给观众讲一段相声怎么样？"; recipient=于谦; max_turns=6`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `message="我是郭德纲，于谦呀，我们给观众讲一段相声怎么样？"; recipient=于谦; max_turns=6`
    const result = await unnamed.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGuodegangInitiateChat2 = createStep({
  id: 'task_guodegang_initiate_chat_2',
  description: `message="我是郭德纲，于谦呀，我们给观众讲一段相声怎么样？"; summary_method="reflection_with_llm"; summary_prompt="简洁的总结下这场相声表演。"`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `message="我是郭德纲，于谦呀，我们给观众讲一段相声怎么样？"; summary_method="reflection_with_llm"; summary_prompt="简洁的总结下这场相声表演。"`
    const result = await unnamed.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskGuodegangSendFollowup = createStep({
  id: 'task_guodegang_send_followup',
  description: `message='我们刚才的相声在讲什么?'; recipient=于谦`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `message='我们刚才的相声在讲什么?'; recipient=于谦`
    const result = await unnamed.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_xiangsheng
 *
 * High-level workflow capturing initiation, summary, and follow-up interactions for the stand-up duo.
 */
export const workflowXiangsheng = createWorkflow({
  id: 'workflow_xiangsheng',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskGuodegangInitiateChat1, taskGuodegangInitiateChat2, taskGuodegangSendFollowup],
})
  .then(taskGuodegangInitiateChat1)
  .then(taskGuodegangInitiateChat2)
  .then(taskGuodegangSendFollowup)
  .commit()
