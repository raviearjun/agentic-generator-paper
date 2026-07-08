/**
 * Workflow: workflow_weather_agent
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { weatherAgent } from '../agents'

// ── Workflow Steps ──

const taskFetchCurrentWeather = createStep({
  id: 'task_fetch_current_weather',
  description: `Fetch current weather data for the specified location using the weatherTool. If no location is provided, ask the user to supply one. Translate non-English location names to English before querying. Return concise but informative output including temperature, humidity, wind conditions, and precipitation. If asked for activity suggestions and forecast is available, include activity recommendations appropriate to the forecast.`,
  inputSchema: z.object({Translate_non: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Fetch current weather data for the specified location using the weatherTool. If no location is provided, ask the user to supply one. Translate non-English location names to English before querying. Return concise but informative output including temperature, humidity, wind conditions, and precipitation. If asked for activity suggestions and forecast is available, include activity recommendations appropriate to the forecast.`
    const result = await weatherAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_weather_agent
 */
export const workflowWeatherAgent = createWorkflow({
  id: 'workflow_weather_agent',
  inputSchema: z.object({Translate_non: z.string()}),
  outputSchema: z.object({}),
  steps: [taskFetchCurrentWeather],
})
  .then(taskFetchCurrentWeather)
  .commit()
