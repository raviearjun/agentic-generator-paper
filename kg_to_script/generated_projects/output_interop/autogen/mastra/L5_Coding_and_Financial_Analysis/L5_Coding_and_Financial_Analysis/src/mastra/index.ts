/**
 * Mastra AI Instance - CodingandFinancialAnalysisCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Produce and save plots (e.g., ytd_stock_gains.png, stock_prices_YTD_plot.png) showing year-to-date gains for requested tickers (NVDA and TSLA/TLSA).
 */

import { Mastra } from '@mastra/core'

// Import agents
import { codeWriterAgent, codeExecutorAgent } from './agents'

// Import workflows
import { workflowL5CodingAndFinancialAnalysis } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Team comprising a code writer and a code executor that collaborate to generate and run plotting code.
 */
export const mastra = new Mastra({
  agents: {
    codeWriterAgent,
    codeExecutorAgent,
  },
  workflows: {
    workflowL5CodingAndFinancialAnalysis,
  },
})
