/**
 * Workflow: workflow_stock_analysis
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Sequential workflow for the Stock Analysis Crew.
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { financialAnalystAgent, researchAnalystAgent, investmentAdvisorAgent } from '../agents'

// ── Workflow Steps ──

const taskFinancialAnalysis = createStep({
  id: 'task_financial_analysis',
  description: `Conduct a thorough analysis of {company_stock}'s stock financial health and market performance. This includes examining key financial metrics such as P/E ratio, EPS growth, revenue trends, and debt-to-equity ratio. Also, analyze the stock's performance in comparison to its industry peers and overall market trends.`,
  inputSchema: z.object({company_stock: z.string()}),
  outputSchema: z.object({company_stock: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Conduct a thorough analysis of ${context.company_stock ?? ''}'s stock financial health and market performance. This includes examining key financial metrics such as P/E ratio, EPS growth, revenue trends, and debt-to-equity ratio. Also, analyze the stock's performance in comparison to its industry peers and overall market trends.`
    const result = await financialAnalystAgent.generate(prompt)
    return {
      ...context,
      company_stock: context.company_stock ?? result.text,
    }
  },
})

const taskResearch = createStep({
  id: 'task_research',
  description: `Collect and summarize recent news articles, press releases, and market analyses related to the {company_stock} stock and its industry. Pay special attention to any significant events, market sentiments, and analysts' opinions. Also include upcoming events like earnings and others.`,
  inputSchema: z.object({company_stock: z.string()}),
  outputSchema: z.object({company_stock: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Collect and summarize recent news articles, press releases, and market analyses related to the ${context.company_stock ?? ''} stock and its industry. Pay special attention to any significant events, market sentiments, and analysts' opinions. Also include upcoming events like earnings and others.`
    const result = await researchAnalystAgent.generate(prompt)
    return {
      ...context,
      company_stock: context.company_stock ?? result.text,
    }
  },
})

const taskFilingsAnalysis = createStep({
  id: 'task_filings_analysis',
  description: `Analyze the latest 10-Q and 10-K filings from EDGAR for the stock {company_stock}. Focus on Management's Discussion and Analysis, financial statements, insider trading activity, and any disclosed risks. Extract relevant data and insights that could influence the stock's future performance.`,
  inputSchema: z.object({company_stock: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Analyze the latest 10-Q and 10-K filings from EDGAR for the stock ${context.company_stock ?? ''}. Focus on Management's Discussion and Analysis, financial statements, insider trading activity, and any disclosed risks. Extract relevant data and insights that could influence the stock's future performance.`
    const result = await financialAnalystAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskRecommend = createStep({
  id: 'task_recommend',
  description: `Review and synthesize the analyses provided by the Financial Analyst and the Research Analyst. Combine these insights to form a comprehensive investment recommendation. Consider all aspects, including financial health, market sentiment, and qualitative data from EDGAR filings. Include insider trading activity and upcoming events like earnings.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Review and synthesize the analyses provided by the Financial Analyst and the Research Analyst. Combine these insights to form a comprehensive investment recommendation. Consider all aspects, including financial health, market sentiment, and qualitative data from EDGAR filings. Include insider trading activity and upcoming events like earnings.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await investmentAdvisorAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_stock_analysis
 *
 * Sequential workflow for the Stock Analysis Crew.
 */
export const workflowStockAnalysis = createWorkflow({
  id: 'workflow_stock_analysis',
  inputSchema: z.object({company_stock: z.string()}),
  outputSchema: z.object({}),
  steps: [taskFinancialAnalysis, taskResearch, taskFilingsAnalysis, taskRecommend],
})
  .then(taskFinancialAnalysis)
  .then(taskResearch)
  .then(taskFilingsAnalysis)
  .then(taskRecommend)
  .commit()
