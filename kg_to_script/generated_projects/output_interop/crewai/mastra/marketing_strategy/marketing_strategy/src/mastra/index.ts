/**
 * Mastra AI Instance - MarketingPostsCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Create a comprehensive marketing strategy to showcase CrewAI's AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities, targeting enterprise decision-makers.
 *   - : Conduct amazing analysis of the products and competitors, providing in-depth insights to guide marketing strategies.
 *   - : Synthesize amazing insights from product analysis to formulate incredible marketing strategies.
 *   - : Develop compelling and innovative content for social media campaigns, with a focus on creating high-impact ad copies.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { leadMarketAnalyst, chiefMarketingStrategist, creativeContentCreator } from './agents'

// Import workflows
import { wpSequential } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    leadMarketAnalyst,
    chiefMarketingStrategist,
    creativeContentCreator,
  },
  workflows: {
    wpSequential,
  },
})
