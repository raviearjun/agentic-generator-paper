/**
 * Mastra AI Instance - OrderPizzaGraphTeam
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : High-level goal to find a pizza shop and place an order for the user.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { langgraphAnthropicAgent } from './agents'

// Import workflows
import { orderPizzaStateGraph } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * Team representing the StateGraph workflow for ordering pizza.
 */
export const mastra = new Mastra({
  agents: {
    langgraphAnthropicAgent,
  },
  workflows: {
    orderPizzaStateGraph,
  },
})
