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
  description: `Initiated by code_executor_agent to request code from code_writer_agent (Chinese message).`,
  inputSchema: z.object({date_range: z.string()}),
  outputSchema: z.object({date_range: z.string()}),
  execute: async ({ inputData }) => {
    // 今天是 {today}. 创建图表，显示 NVDA 和 TLSA 的股票收益。确保代码位于标记代码块中，并将图表保存到文件 ytd_stock_gains.png。
    // This step uses agent: codeExecutorAgent
    // const result = await codeExecutorAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_plot_ytd_v1 not implemented yet')
  },
})

const taskPlotYtdV2 = createStep({
  id: 'task_plot_ytd_v2',
  description: `Initiated by code_executor_agent to request code from code_writer_agent (English message about downloading and plotting YTD stock prices).`,
  inputSchema: z.object({date_range: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Today is {today}. Download the stock prices YTD for NVDA and TSLA and create a plot. Make sure the code is in markdown code block and save the figure to a file stock_prices_YTD_plot.png.
    // This step uses agent: codeExecutorAgent
    // const result = await codeExecutorAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_plot_ytd_v2 not implemented yet')
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
