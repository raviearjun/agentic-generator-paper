/**
 * Workflow: pattern_trip_planning
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { citySelectionAgent, localExpertAgent, travelConciergeAgent } from '../agents'

// ── Workflow Steps ──

const taskIdentifyCity = createStep({
  id: 'task_identify_city',
  description: `Analyze and select the best city for the trip based`,
  inputSchema: z.object({origin: z.string(), cities: z.string(), range: z.string(), interests: z.string()}),
  outputSchema: z.object({range: z.string(), origin: z.string(), interests: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Analyze and select the best city for the trip based
on specific criteria such as weather patterns, seasonal
events, and travel costs. This task involves comparing
multiple cities, considering factors like current weather
conditions, upcoming cultural or seasonal events, and
overall travel expenses.

Your final answer must be a detailed
report on the chosen city, and everything you found out
about it, including the actual flight costs, weather
forecast and attractions.
If you do your BEST WORK, I'll tip you $100!

Traveling from: ${context.origin ?? ''}
City Options: ${context.cities ?? ''}
Trip Date: ${context.range ?? ''}
Traveler Interests: ${context.interests ?? ''}`
    const result = await citySelectionAgent.generate(prompt)
    return {
      ...context,
      range: context.range ?? result.text,
      origin: context.origin ?? result.text,
      interests: context.interests ?? result.text,
    }
  },
})

const taskGatherCityInfo = createStep({
  id: 'task_gather_city_info',
  description: `As a local expert on this city you must compile an`,
  inputSchema: z.object({range: z.string(), origin: z.string(), interests: z.string()}),
  outputSchema: z.object({range: z.string(), origin: z.string(), interests: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `As a local expert on this city you must compile an
in-depth guide for someone traveling there and wanting
to have THE BEST trip ever!
Gather information about key attractions, local customs,
special events, and daily activity recommendations.
Find the best spots to go to, the kind of place only a
local would know.
This guide should provide a thorough overview of what
the city has to offer, including hidden gems, cultural
hotspots, must-visit landmarks, weather forecasts, and
high level costs.

The final answer must be a comprehensive city guide,
rich in cultural insights and practical tips,
tailored to enhance the travel experience.
If you do your BEST WORK, I'll tip you $100!

Trip Date: ${context.range ?? ''}
Traveling from: ${context.origin ?? ''}
Traveler Interests: ${context.interests ?? ''}`
    const result = await localExpertAgent.generate(prompt)
    return {
      ...context,
      range: context.range ?? result.text,
      origin: context.origin ?? result.text,
      interests: context.interests ?? result.text,
    }
  },
})

const taskPlanItinerary = createStep({
  id: 'task_plan_itinerary',
  description: `Expand this guide into a full 7-day travel`,
  inputSchema: z.object({range: z.string(), origin: z.string(), interests: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Expand this guide into a full 7-day travel
itinerary with detailed per-day plans, including
weather forecasts, places to eat, packing suggestions,
and a budget breakdown.

You MUST suggest actual places to visit, actual hotels
to stay and actual restaurants to go to.

This itinerary should cover all aspects of the trip,
from arrival to departure, integrating the city guide
information with practical travel logistics.

Your final answer MUST be a complete expanded travel plan,
formatted as markdown, encompassing a daily schedule,
anticipated weather conditions, recommended clothing and
items to pack, and a detailed budget, ensuring THE BEST
TRIP EVER. Be specific and give it a reason why you picked
each place, what makes them special! If you do your BEST WORK, I'll tip you $100!

Trip Date: ${context.range ?? ''}
Traveling from: ${context.origin ?? ''}
Traveler Interests: ${context.interests ?? ''}`
    const result = await travelConciergeAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * pattern_trip_planning
 */
export const patternTripPlanning = createWorkflow({
  id: 'pattern_trip_planning',
  inputSchema: z.object({origin: z.string(), cities: z.string(), range: z.string(), interests: z.string()}),
  outputSchema: z.object({}),
  steps: [taskIdentifyCity, taskGatherCityInfo, taskPlanItinerary],
})
  .then(taskIdentifyCity)
  .then(taskGatherCityInfo)
  .then(taskPlanItinerary)
  .commit()
