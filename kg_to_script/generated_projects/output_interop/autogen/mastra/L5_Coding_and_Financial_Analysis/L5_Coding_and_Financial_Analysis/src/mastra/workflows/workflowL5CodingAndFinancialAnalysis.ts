/**
 * Workflow: workflow_l5_coding_and_financial_analysis
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow representing the conversational code-writing and execution loop for producing YTD stock plots.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { codeExecutorAgent } from '../agents'

// ── Workflow Steps ──

const taskPlotYtdV1 = createStep({
  id: 'task_plot_ytd_v1',
  description: `今天是 {today}. 创建图表，显示 NVDA 和 TLSA 的股票收益。确保代码位于标记代码块中，并将图表保存到文件 ytd_stock_gains.png。`,
  inputSchema: z.object({date_range: z.string()}),
  outputSchema: z.object({date_range: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `今天是 ${context.today ?? ''}. 创建图表，显示 NVDA 和 TLSA 的股票收益。确保代码位于标记代码块中，并将图表保存到文件 ytd_stock_gains.png。`
    const result = await codeExecutorAgent.generate(prompt)
    return {
      ...context,
      date_range: context.date_range ?? result.text,
    }
  },
})

const taskPlotYtdV2 = createStep({
  id: 'task_plot_ytd_v2',
  description: `Today is {today}. Download the stock prices YTD for NVDA and TSLA and create a plot. Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png.`,
  inputSchema: z.object({date_range: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Today is ${context.today ?? ''}. Download the stock prices YTD for NVDA and TSLA and create a plot. Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png.`
    const result = await codeExecutorAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_l5_coding_and_financial_analysis
 *
 * Workflow representing the conversational code-writing and execution loop for producing YTD stock plots.
 */
export const workflowL5CodingAndFinancialAnalysis = createWorkflow({
  id: 'workflow_l5_coding_and_financial_analysis',
  inputSchema: z.object({date_range: z.string()}),
  outputSchema: z.object({}),
  steps: [taskPlotYtdV1, taskPlotYtdV2],
})
  .then(taskPlotYtdV1)
  .then(taskPlotYtdV2)
  .commit()
