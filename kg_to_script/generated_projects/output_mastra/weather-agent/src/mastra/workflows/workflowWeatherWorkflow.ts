/**
 * Workflow: workflow_weather_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { weatherAgent } from '../agents'

// ── Workflow Steps ──

const taskFetchWeather = createStep({
  id: 'task_fetch_weather',
  description: `Fetches weather forecast for a given city. Use triggerData.city as input to retrieve forecast data from the Open-Meteo APIs and return an array of daily forecast objects.`,
  inputSchema: z.object({city_as_input_to_retrieve_forecast_data_from_the_Open: z.array(z.string())}),
  outputSchema: z.object({You_are_a_local_activities_and_travel_expert_who_excels_at_weather: z.string(), Suggest_2_3_time: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Fetches weather forecast for a given city. Use triggerData.city as input to retrieve forecast data from the Open-Meteo APIs and return an array of daily forecast objects.`
    const result = await weatherAgent.generate(prompt)
    return {
      ...context,
      You_are_a_local_activities_and_travel_expert_who_excels_at_weather: context.You_are_a_local_activities_and_travel_expert_who_excels_at_weather ?? result.text,
      Suggest_2_3_time: context.Suggest_2_3_time ?? result.text,
    }
  },
})

const taskPlanActivities = createStep({
  id: 'task_plan_activities',
  description: `You are a local activities and travel expert who excels at weather-based planning. Analyze the weather data and provide practical activity recommendations.`,
  inputSchema: z.object({You_are_a_local_activities_and_travel_expert_who_excels_at_weather: z.string(), Suggest_2_3_time: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You are a local activities and travel expert who excels at weather-based planning. Analyze the weather data and provide practical activity recommendations.

For each day in the forecast, structure your response exactly as follows:

📅 [Day, Month Date, Year]
═══════════════════════════

🌡️ WEATHER SUMMARY
• Conditions: [brief description]
• Temperature: [X°C/Y°F to A°C/B°F]
• Precipitation: [X% chance]

🌅 MORNING ACTIVITIES
Outdoor:
• [Activity Name] - [Brief description including specific location/route]
  Best timing: [specific time range]
  Note: [relevant weather consideration]

🌞 AFTERNOON ACTIVITIES
Outdoor:
• [Activity Name] - [Brief description including specific location/route]
  Best timing: [specific time range]
  Note: [relevant weather consideration]

🏠 INDOOR ALTERNATIVES
• [Activity Name] - [Brief description including specific venue]
  Ideal for: [weather condition that would trigger this alternative]

⚠️ SPECIAL CONSIDERATIONS
• [Any relevant weather warnings, UV index, wind conditions, etc.]

Guidelines:
- Suggest 2-3 time-specific outdoor activities per day
- Include 1-2 indoor backup options
- For precipitation >50%, lead with indoor activities
- All activities must be specific to the location
- Include specific venues, trails, or locations
- Consider activity intensity based on temperature
- Keep descriptions concise but informative

Maintain this exact formatting for consistency, using the emoji and section headers as shown.`
    const result = await weatherAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_weather_workflow
 */
export const workflowWeatherWorkflow = createWorkflow({
  id: 'workflow_weather_workflow',
  inputSchema: z.object({city_as_input_to_retrieve_forecast_data_from_the_Open: z.array(z.string())}),
  outputSchema: z.object({}),
  steps: [taskFetchWeather, taskPlanActivities],
})
  .then(taskFetchWeather)
  .then(taskPlanActivities)
  .commit()
