/**
 * Mastra AI Instance - RecruitmentCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Agent goal: find potential candidates matching provided job requirements.
 *   - : Agent goal: evaluate and rank candidates against job requirements.
 *   - : Agent goal: create outreach templates and communication plans.
 *   - : Agent goal: compile findings and recommend top candidates.
 *   - : Team-level objective to orchestrate agent collaboration for recruitment.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { researcher, matcher, communicator, reporter } from './agents'

// Import workflows
import { workflowRecruitment } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * CrewAI-based team coordinating agents to automate recruitment tasks.
 */
export const mastra = new Mastra({
  agents: {
    researcher,
    matcher,
    communicator,
    reporter,
  },
  workflows: {
    workflowRecruitment,
  },
})
