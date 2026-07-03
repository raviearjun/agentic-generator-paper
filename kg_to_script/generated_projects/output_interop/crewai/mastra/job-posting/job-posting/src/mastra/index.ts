/**
 * Mastra AI Instance - JobPostingCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Analyze the company website and provided description to extract insights on culture, values, and specific needs.
 *   - : Use insights from the Research Analyst to create a detailed, engaging, and enticing job posting.
 *   - : Review the job posting for clarity, engagement, grammatical accuracy, and alignment with the company's culture and values.
 *   - : Automate the creation of job postings using CrewAI to analyze company information and produce polished job descriptions and analyses.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { researchAgent, writerAgent, reviewAgent } from './agents'

// Import workflows
import { jobPostingWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 * CrewAI crew that orchestrates agents to create job postings
 */
export const mastra = new Mastra({
  agents: {
    researchAgent,
    writerAgent,
    reviewAgent,
  },
  workflows: {
    jobPostingWorkflow,
  },
})
