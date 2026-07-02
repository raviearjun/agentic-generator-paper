/**
 * Agent: Weather Assistant
 * ID: weather-agent
 * 
 * Auto-generated from AgentO Knowledge Graph
 * Capabilities:
 *   - : Fetch current weather (temperature, humidity, wind, precipitation) for a given location.
 */

import { Agent } from '@mastra/core/agent'

// Import tools
import { toolWeatherTool } from '../tools'

/**
 * Weather Assistant
 * 
 * Instructions:
 * You are Weather Assistant.
 */
export const weatherAgent = new Agent({
  id: `weather-agent`,
  name: `Weather Assistant`,
  instructions: `You are Weather Assistant.`,
  model: 'openai/gpt-4o-mini',
  tools: {
    toolWeatherTool,
  },
})
