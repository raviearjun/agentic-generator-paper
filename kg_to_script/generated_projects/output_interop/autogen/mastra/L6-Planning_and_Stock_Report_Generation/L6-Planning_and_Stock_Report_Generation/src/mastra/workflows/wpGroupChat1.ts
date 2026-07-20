/**
 * Workflow: wp_group_chat1
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Derived workflow pattern from the GroupChat agent configuration.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { admin, planner, engineer, executor, writer } from '../agents'

// ── Workflow Steps ──

const taskInitiateWriteBlog = createStep({
  id: 'task_initiate_write_blog',
  description: `Write a blogpost about the stock price performance of Nvidia in the past month. Today's date is 2024-04-23.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Write a blogpost about the stock price performance of Nvidia in the past month. Today's date is 2024-04-23.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await admin.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskPlannerPlan = createStep({
  id: 'task_planner_plan',
  description: `Given the blogpost task, determine what information can be retrieved using Python code (e.g., historical prices, volumes) and produce a stepwise plan. After each step is executed, inspect results and direct remaining steps; on failure, suggest workarounds.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Given the blogpost task, determine what information can be retrieved using Python code (e.g., historical prices, volumes) and produce a stepwise plan. After each step is executed, inspect results and direct remaining steps; on failure, suggest workarounds.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await planner.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskEngineerWriteCode = createStep({
  id: 'task_engineer_write_code',
  description: `Write Python code to retrieve stock data and produce analysis outputs based on the planner's specifications.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Write Python code to retrieve stock data and produce analysis outputs based on the planner's specifications.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await engineer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskExecutorRunCode = createStep({
  id: 'task_executor_run_code',
  description: `Execute the latest code message from the engineer (look back up to last 3 messages for code), store artifacts in the 'coding' directory, and report outputs and errors.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Execute the latest code message from the engineer (look back up to last 3 messages for code), store artifacts in the 'coding' directory, and report outputs and errors.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await executor.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskWriterProduceBlog = createStep({
  id: 'task_writer_produce_blog',
  description: `Write a blog post in markdown summarizing Nvidia's stock performance in the past month using provided analysis outputs. Use appropriate titles and place content in a pseudo mdcode block. Accept and apply admin feedback to refine.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Write a blog post in markdown summarizing Nvidia's stock performance in the past month using provided analysis outputs. Use appropriate titles and place content in a pseudo mdcode block. Accept and apply admin feedback to refine.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await writer.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * wp_group_chat1
 *
 * Derived workflow pattern from the GroupChat agent configuration.
 */
export const wpGroupChat1 = createWorkflow({
  id: 'wp_group_chat1',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskInitiateWriteBlog, taskPlannerPlan, taskEngineerWriteCode, taskExecutorRunCode, taskWriterProduceBlog],
})
  .then(taskInitiateWriteBlog)
  .then(taskPlannerPlan)
  .then(taskEngineerWriteCode)
  .then(taskExecutorRunCode)
  .then(taskWriterProduceBlog)
  .commit()
