/**
 * Agent: A2A remote agent
 * ID: agentId (constructor parameter)
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Capabilities:
 *   - : Capabilities to send/receive messages, manage tasks, and configure push notifications via A2A JSON-RPC.
 *   - : Process and deserialize server-sent A2A event streams into application-level event objects.
 */

import { Agent } from '@mastra/core/agent'

// Import tools
import { toolA2AApi, toolProcessA2AStream } from '../tools'

/**
 * A2A remote agent
 * 
 * Instructions:
 * You are A2A remote agent.
 */
export const agentIdConstructorParameter = new Agent({
  id: `agentId (constructor parameter)`,
  name: `A2A remote agent`,
  instructions: `You are A2A remote agent.`,
  model: 'openai/gpt-4o-mini',
  tools: {
    toolA2AApi,
    toolProcessA2AStream,
  },
})
