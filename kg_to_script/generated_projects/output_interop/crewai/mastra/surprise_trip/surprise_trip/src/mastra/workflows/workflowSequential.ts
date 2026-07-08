/**
 * Workflow: workflow_sequential
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { personalizedActivityPlanner, restaurantScout, itineraryCompiler } from '../agents'

// ── Workflow Steps ──

const taskPersonalizedActivityPlanningTask = createStep({
  id: 'task_personalized_activity_planning_task',
  description: `Research and find cool things to do at {destination}. Focus on activities and events that match the traveler's interests and age group. Utilize internet search tools and recommendation engines to gather the information.`,
  inputSchema: z.object({destination: z.string(), origin: z.string(), age: z.string(), hotel_location: z.string(), flight_information: z.string(), trip_duration: z.string()}),
  outputSchema: z.object({destination: z.string(), origin: z.string(), age: z.string(), hotel_location: z.string(), flight_information: z.string(), trip_duration: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Research and find cool things to do at ${context.destination ?? ''}. Focus on activities and events that match the traveler's interests and age group. Utilize internet search tools and recommendation engines to gather the information.

Traveler's information:
- origin: ${context.origin ?? ''}
- destination: ${context.destination ?? ''}
- age of the traveler: ${context.age ?? ''}
- hotel localtion: ${context.hotel_location ?? ''}
- flight infromation: ${context.flight_information ?? ''}
- how long is the trip: ${context.trip_duration ?? ''}`
    const result = await personalizedActivityPlanner.generate(prompt)
    return {
      ...context,
      destination: context.destination ?? result.text,
      origin: context.origin ?? result.text,
      age: context.age ?? result.text,
      hotel_location: context.hotel_location ?? result.text,
      flight_information: context.flight_information ?? result.text,
      trip_duration: context.trip_duration ?? result.text,
    }
  },
})

const taskRestaurantScenicLocationScoutTask = createStep({
  id: 'task_restaurant_scenic_location_scout_task',
  description: `Find highly-rated restaurants and dining experiences at {destination}. Recommend scenic locations and fun activities that align with the traveler's preferences. Use internet search tools, restaurant review sites, and travel guides.`,
  inputSchema: z.object({destination: z.string(), origin: z.string(), age: z.string(), hotel_location: z.string(), flight_information: z.string(), trip_duration: z.string()}),
  outputSchema: z.object({destination: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Find highly-rated restaurants and dining experiences at ${context.destination ?? ''}. Recommend scenic locations and fun activities that align with the traveler's preferences. Use internet search tools, restaurant review sites, and travel guides.

Traveler's information:
- origin: ${context.origin ?? ''}
- destination: ${context.destination ?? ''}
- age of the traveler: ${context.age ?? ''}
- hotel localtion: ${context.hotel_location ?? ''}
- flight infromation: ${context.flight_information ?? ''}
- how long is the trip: ${context.trip_duration ?? ''}`
    const result = await restaurantScout.generate(prompt)
    return {
      ...context,
      destination: context.destination ?? result.text,
    }
  },
})

const taskItineraryCompilationTask = createStep({
  id: 'task_itinerary_compilation_task',
  description: `Compile all researched information into a comprehensive day-by-day itinerary for the trip to {destination}. Ensure the itinerary integrates flights, hotel information, and all planned activities and dining experiences. Use text formatting and document creation tools to organize the information.`,
  inputSchema: z.object({destination: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Compile all researched information into a comprehensive day-by-day itinerary for the trip to ${context.destination ?? ''}. Ensure the itinerary integrates flights, hotel information, and all planned activities and dining experiences. Use text formatting and document creation tools to organize the information.`
    const result = await itineraryCompiler.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_sequential
 */
export const workflowSequential = createWorkflow({
  id: 'workflow_sequential',
  inputSchema: z.object({destination: z.string(), origin: z.string(), age: z.string(), hotel_location: z.string(), flight_information: z.string(), trip_duration: z.string()}),
  outputSchema: z.object({}),
  steps: [taskPersonalizedActivityPlanningTask, taskRestaurantScenicLocationScoutTask, taskItineraryCompilationTask],
})
  .then(taskPersonalizedActivityPlanningTask)
  .then(taskRestaurantScenicLocationScoutTask)
  .then(taskItineraryCompilationTask)
  .commit()
