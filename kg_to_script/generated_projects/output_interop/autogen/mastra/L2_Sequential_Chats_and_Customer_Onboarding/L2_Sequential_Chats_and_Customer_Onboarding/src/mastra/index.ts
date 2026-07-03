/**
 * Mastra AI Instance - OnboardingTeam
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Pipeline: KG (.ttl) → SPARQL → Pydantic IR → TypeScript
 * Goals:
 *   - : Gather customer's name and location.
 *   - : Collect customer's preferences on news topics.
 *   - : Provide engaging and fun content based on customer's info and topic preferences.
 * Human Agents:
 *   - agent_customer_proxy_agent (customer_proxy)
 */

import { Mastra } from '@mastra/core'

// Import agents
import { onboardingPersonalInformationAgent, onboardingTopicPreferenceAgent, customerEngagementAgent } from './agents'

// Import workflows
import { onboardingWorkflow } from './workflows'

/**
 * Mastra instance with registered agents, workflows, and memory.
 *
 */
export const mastra = new Mastra({
  agents: {
    onboardingPersonalInformationAgent,
    onboardingTopicPreferenceAgent,
    customerEngagementAgent,
  },
  workflows: {
    onboardingWorkflow,
  },
})
