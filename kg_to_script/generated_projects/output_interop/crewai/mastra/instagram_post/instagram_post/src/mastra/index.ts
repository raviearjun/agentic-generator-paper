/**
 * Mastra AI Instance - CopyCrewagentsforcopygeneration
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Produce thorough product and competitor analysis to inform marketing strategy.
 *   - : Formulate marketing strategies and creative ideas based on product and competitor analysis.
 *   - : Produce multiple Instagram ad copy options aligned with campaign strategy.
 *   - : Generate three photographic concepts that best represent the campaign and product without showing the actual product.
 *   - : Ensure final creative outputs are aligned with product goals; review and approve imagery.
 *   - : Produce marketing analysis and 3 Instagram ad copy options for the product.
 *   - : Produce three photograph concepts and a reviewed final selection aligned with campaign copy.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { productCompetitorAgent, strategyPlannerAgent, creativeContentCreatorAgent, seniorPhotographerAgent, chiefCreativeDiretorAgent } from './agents'

// Import workflows
import { workflowCopyCrew, workflowImageCrew } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    productCompetitorAgent,
    strategyPlannerAgent,
    creativeContentCreatorAgent,
    seniorPhotographerAgent,
    chiefCreativeDiretorAgent,
  },
  workflows: {
    workflowCopyCrew,
    workflowImageCrew,
  },
})
