/**
 * Mastra AI Instance - MeetingPreparationCrew
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Conduct thorough research on people and companies involved in the meeting.
 *   - : Analyze the current industry trends, challenges, and opportunities.
 *   - : Develop talking points, questions, and strategic angles for the meeting.
 *   - : Compile all gathered information into a concise, informative briefing document.
 */

import { Mastra } from '@mastra/core'

// Import agents
import { researcherAgent, industryAnalystAgent, meetingStrategyAgent, summaryAndBriefingAgent } from './agents'

// Import workflows
import { meetingPreparationPattern } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    researcherAgent,
    industryAnalystAgent,
    meetingStrategyAgent,
    summaryAndBriefingAgent,
  },
  workflows: {
    meetingPreparationPattern,
  },
})
