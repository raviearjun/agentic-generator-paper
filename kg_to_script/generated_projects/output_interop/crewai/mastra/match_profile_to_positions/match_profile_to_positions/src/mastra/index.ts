/**
 * Mastra AI Instance - MatchToProposalCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Extract relevant information from the CV, such as skills, experience, and education.
 *   - : Match the CV to the job opportunities based on skills, experience, and key achievements.
 *   - : Overall objective for the crew: automate the matching of candidate CVs to job proposals.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { cvReader, matcher } from './agents'

// Import workflows
import { workflowSequential } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * CrewAI Team that coordinates cv_reader and matcher agents to match CVs to job proposals.
 */
export const mastra = new Mastra({
  agents: {
    cvReader,
    matcher,
  },
  workflows: {
    workflowSequential,
  },
})
