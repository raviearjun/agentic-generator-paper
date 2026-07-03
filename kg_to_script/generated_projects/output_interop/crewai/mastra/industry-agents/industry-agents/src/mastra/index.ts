/**
 * Mastra AI Instance - Blogcrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Continuously track the latest biomedical advancements and identify how Weaviate’s features can support AI applications in biomedical research, diagnostics, and personalized medicine.
 *   - : Stay updated on healthcare policy shifts, digital health trends, and explore how Weaviate’s features can optimize workflows in hospital systems, EHR integration, and health communication.
 *   - : Monitor financial sector trends including AI in trading, compliance automation, and client advisory, and assess how Weaviate’s tools can enable cutting-edge financial applications.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { biomedicalMarketingAgent, healthcareMarketingAgent, financialMarketingAgent } from './agents'

// Import workflows
import { workflowBlogCrew } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    biomedicalMarketingAgent,
    healthcareMarketingAgent,
    financialMarketingAgent,
  },
  workflows: {
    workflowBlogCrew,
  },
})
