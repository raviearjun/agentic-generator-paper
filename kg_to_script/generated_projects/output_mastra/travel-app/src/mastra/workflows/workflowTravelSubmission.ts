/**
 * Workflow: workflow_travel_submission
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { travelAnalyzer } from '../agents'

// ── Workflow Steps ──

const taskOutboundFlight = createStep({
  id: 'task_outbound_flight',
  description: `Available outboundFlight items will be provided. Select a single outbound flight based on travelForm (departureLocation, arrivalLocation, startDate, endDate) and flightPriority. ALWAYS pass entire date timestamps for departureTime and arrivalTime. Return ids (or flightNumber) and a short reasoning.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Available outboundFlight items will be provided. Select a single outbound flight based on travelForm (departureLocation, arrivalLocation, startDate, endDate) and flightPriority. ALWAYS pass entire date timestamps for departureTime and arrivalTime. Return ids (or flightNumber) and a short reasoning.`
    const result = await travelAnalyzer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskReturnFlight = createStep({
  id: 'task_return_flight',
  description: `Available returnFlight items will be provided. Select a single return flight based on travelForm and flightPriority. ALWAYS return full flight objects for outbound and return flights and timestamps.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Available returnFlight items will be provided. Select a single return flight based on travelForm and flightPriority. ALWAYS return full flight objects for outbound and return flights and timestamps.`
    const result = await travelAnalyzer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskAccommodationHotels = createStep({
  id: 'task_accommodation_hotels',
  description: `Given available hotels and the travelForm (arrivalCityId, hotelPriceRange), select up to 3 hotel options. Ignore 'reviewScore' and extract numeric rating from description/accessibility fields. Provide ids and reasoning.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Given available hotels and the travelForm (arrivalCityId, hotelPriceRange), select up to 3 hotel options. Ignore 'reviewScore' and extract numeric rating from description/accessibility fields. Provide ids and reasoning.`
    const result = await travelAnalyzer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskAttraction = createStep({
  id: 'task_attraction',
  description: `Given a set of attractions for the arrival city and the user's interests, select three attractions, provide brief reasoning, and include price, duration, and rating where available.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Given a set of attractions for the arrival city and the user's interests, select three attractions, provide brief reasoning, and include price, duration, and rating where available.`
    const result = await travelAnalyzer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskAirbnbLocation = createStep({
  id: 'task_airbnb_location',
  description: `Search for Airbnb location matches for the arrival city and select up to 3 unique place ids to be used in the subsequent Airbnb search. Provide ids and reasoning.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Search for Airbnb location matches for the arrival city and select up to 3 unique place ids to be used in the subsequent Airbnb search. Provide ids and reasoning.`
    const result = await travelAnalyzer.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskAccommodationAirbnb = createStep({
  id: 'task_accommodation_airbnb',
  description: `Given Airbnb search results and travelForm (typeOfPlace, startDate, endDate), select up to 3 Airbnb options, then pick the top result to return. Provide ids and reasoning.`,
  inputSchema: z.object({}),
  outputSchema: z.object({reasoning: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Given Airbnb search results and travelForm (typeOfPlace, startDate, endDate), select up to 3 Airbnb options, then pick the top result to return. Provide ids and reasoning.`
    const result = await travelAnalyzer.generate(prompt)
    return {
      ...context,
      reasoning: context.reasoning ?? result.text,
    }
  },
})

// ── Workflow Definition ──

/**
 * workflow_travel_submission
 */
export const workflowTravelSubmission = createWorkflow({
  id: 'workflow_travel_submission',
  inputSchema: z.object({}),
  outputSchema: z.object({reasoning: z.string()}),
  steps: [taskOutboundFlight, taskReturnFlight, taskAccommodationHotels, taskAttraction, taskAirbnbLocation, taskAccommodationAirbnb],
})
  .then(taskOutboundFlight)
  .then(taskReturnFlight)
  .then(taskAccommodationHotels)
  .then(taskAttraction)
  .then(taskAirbnbLocation)
  .then(taskAccommodationAirbnb)
  .commit()
