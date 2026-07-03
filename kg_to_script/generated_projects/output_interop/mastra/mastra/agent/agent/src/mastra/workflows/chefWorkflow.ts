/**
 * Workflow: chef_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Sequential steps inferred from task functions in src/index.ts
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { chefAgent } from '../agents'

// ── Workflow Steps ──

const taskQueryPantry = createStep({
  id: 'task_query_pantry',
  description: `User asks what they can make given pantry ingredients (pasta, canned tomatoes, garlic, olive oil, dried herbs).`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make?
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_query_pantry not implemented yet')
  },
})

const taskGenerateText = createStep({
  id: 'task_generate_text',
  description: `Alternate/duplicate generate usage with same pantry query.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // In my kitchen I have: pasta, canned tomatoes, garlic, olive oil, and some dried herbs (basil and oregano). What can I make?
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_generate_text not implemented yet')
  },
})

const taskTextStream = createStep({
  id: 'task_text_stream',
  description: `Streamed response for chicken/coconut/sweet potatoes/curry powder scenario.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder.
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_text_stream not implemented yet')
  },
})

const taskGenerateStream = createStep({
  id: 'task_generate_stream',
  description: `Streaming variant with array input; yields streamed recipe.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Now I'm over at my friend's house, and they have: chicken thighs, coconut milk, sweet potatoes, and some curry powder.
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_generate_stream not implemented yet')
  },
})

const taskTextObject = createStep({
  id: 'task_text_object',
  description: `Generate a lasagna recipe structured as an object with ingredients and steps.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // I want to make lasagna, can you generate a lasagna recipe for me?
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_text_object not implemented yet')
  },
})

const taskTextObjectJsonschema = createStep({
  id: 'task_text_object_jsonschema',
  description: `Generate lasagna recipe constrained by provided JSON Schema.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // I want to make lasagna, can you generate a lasagna recipe for me?
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_text_object_jsonschema not implemented yet')
  },
})

const taskGenerateObject = createStep({
  id: 'task_generate_object',
  description: `Generate lasagna recipe with structured output (array input variant).`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // I want to make lasagna, can you generate a lasagna recipe for me?
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_generate_object not implemented yet')
  },
})

const taskStreamObject = createStep({
  id: 'task_stream_object',
  description: `Streamed generation of a lasagna recipe as structured object.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // I want to make lasagna, can you generate a lasagna recipe for me?
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_stream_object not implemented yet')
  },
})

const taskGenerateStreamObject = createStep({
  id: 'task_generate_stream_object',
  description: `Final streaming structured generation variant.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // I want to make lasagna, can you generate a lasagna recipe for me?
    // This step uses agent: chefAgent
    // const result = await chefAgent.generate('...')
    // TODO: Implement step logic
    throw new Error('task_generate_stream_object not implemented yet')
  },
})

// ── Workflow Definition ──

/**
 * chef_workflow
 *
 * Sequential steps inferred from task functions in src/index.ts
 */
export const chefWorkflow = createWorkflow({
  id: 'chef_workflow',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskQueryPantry, taskGenerateText, taskTextStream, taskGenerateStream, taskTextObject, taskTextObjectJsonschema, taskGenerateObject, taskStreamObject, taskGenerateStreamObject],
})
  .then(taskQueryPantry)
  .then(taskGenerateText)
  .then(taskTextStream)
  .then(taskGenerateStream)
  .then(taskTextObject)
  .then(taskTextObjectJsonschema)
  .then(taskGenerateObject)
  .then(taskStreamObject)
  .then(taskGenerateStreamObject)
  .commit()
