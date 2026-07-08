/**
 * Agent: Admin
 * ID: Admin
 * 
 * Auto-generated from AgentO Knowledge Graph
 */

import { Agent } from '@mastra/core/agent'

/**
 * Admin
 * 
 * Instructions:
 * You are Admin.
 */
export const admin = new Agent({
  id: `Admin`,
  name: `Admin`,
  instructions: `You are Admin.`,
  model: 'openai/gpt-4o-mini',
})
