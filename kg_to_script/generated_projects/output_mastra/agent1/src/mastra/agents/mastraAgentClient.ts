/**
 * Agent: client-wrapper
 * ID: MastraAgentClient
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Capabilities:
 *   - : Capability to synthesize audio from text.
 *   - : Capability to transcribe audio to text.
 *   - : Capability to execute a client-supplied tool via `clientTool.execute` and return results to the agent stream.
 */

import { Agent } from '@mastra/core/agent'

// Import tools
import { voiceProviderTool, clientToolsTool } from '../tools'

/**
 * client-wrapper
 * 
 * Instructions:
 * Goal for the Mastra agent client: handle streaming responses, orchestrate client tool execution, and expose voice and observation endpoints.
 */
export const mastraAgentClient = new Agent({
  id: `MastraAgentClient`,
  name: `client-wrapper`,
  instructions: `Goal for the Mastra agent client: handle streaming responses, orchestrate client tool execution, and expose voice and observation endpoints.`,
  model: 'openai/gpt-4o-mini',
  tools: {
    voiceProviderTool,
    clientToolsTool,
  },
})
