/**
 * Mastra AI Instance - TradingSystem
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Provide portfolio overview and enable executing trades via the UI.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { tradeAgent } from './agents'

// Import workflows
import { buyStockWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Frontend trading system that displays portfolio data and enables trade execution.
 */
export const mastra = new Mastra({
  agents: {
    tradeAgent,
  },
  workflows: {
    buyStockWorkflow,
  },
})
