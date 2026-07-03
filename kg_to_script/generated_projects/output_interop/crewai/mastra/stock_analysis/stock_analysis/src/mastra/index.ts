/**
 * Mastra AI Instance - StockAnalysisCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Automate the process of analyzing a stock to produce a detailed report and investment recommendation.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { financialAgent, researchAnalystAgent, financialAnalystAgent, investmentAdvisorAgent } from './agents'

// Import workflows
import { workflowStockAnalysis } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * CrewAI-based team coordinating multiple analyst agents to produce stock analysis and recommendations.
 */
export const mastra = new Mastra({
  agents: {
    financialAgent,
    researchAnalystAgent,
    financialAnalystAgent,
    investmentAdvisorAgent,
  },
  workflows: {
    workflowStockAnalysis,
  },
})
