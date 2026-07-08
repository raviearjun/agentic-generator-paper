/**
 * Workflow: pattern_choose_template
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { seniorReactEngineer } from '../agents'

// ── Workflow Steps ──

const taskChooseTemplate = createStep({
  id: 'task_choose_template',
  description: `Learn the templates options choose and copy the one that suits the idea below the best, YOU MUST COPY, and then YOU MUST read the src/component in the directory you just copied, to decide what component files should be updated to make the landing page about the idea below.`,
  inputSchema: z.object({idea: z.string()}),
  outputSchema: z.object({idea: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Learn the templates options choose and copy the one that suits the idea below the best, YOU MUST COPY, and then YOU MUST read the src/component in the directory you just copied, to decide what component files should be updated to make the landing page about the idea below.

- YOU MUST READ THE DIRECTORY BEFORE CHOOSING THE FILES.
- YOU MUST NOT UPDATE any Pricing components.
- YOU MUST UPDATE ONLY the 4 most important components.

Your final answer MUST be ONLY a JSON array of components full file paths that need to be updated.

IDEA
# ----------
${context.idea ?? ''}`
    const result = await seniorReactEngineer.generate(prompt)
    return {
      ...context,
      idea: context.idea ?? result.text,
    }
  },
})

const taskUpdatePage = createStep({
  id: 'task_update_page',
  description: `READ the ./[chosen_template]/src/app/page.jsx OR ./[chosen_template]/src/app/(main)/page.jsx to learn its content and then write an updated version to the filesystem that removes any section related components that are not in our list from the returns. Keep the imports.`,
  inputSchema: z.object({idea: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `READ the ./[chosen_template]/src/app/page.jsx OR ./[chosen_template]/src/app/(main)/page.jsx to learn its content and then write an updated version to the filesystem that removes any section related components that are not in our list from the returns. Keep the imports.

Final answer MUST BE ONLY a valid json list with the full path of each of the components we will be using, the same way you got them.

RULES
# -----
- NEVER ADD A FINAL DOT to the file content.
- NEVER WRITE \\n (newlines as string) on the file, just the code.
- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.
- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.
- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.
- Save the file as with \`.jsx\` extension.
- Return the same valid JSON list of the components your got.

You'll get a $100 tip if you follow all the rules!

Also update any necessary text to reflect this landing page is about the idea below.

IDEA
# ----------
${context.idea ?? ''}`
    const result = await seniorReactEngineer.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * pattern_choose_template
 */
export const patternChooseTemplate = createWorkflow({
  id: 'pattern_choose_template',
  inputSchema: z.object({idea: z.string()}),
  outputSchema: z.object({}),
  steps: [taskChooseTemplate, taskUpdatePage],
})
  .then(taskChooseTemplate)
  .then(taskUpdatePage)
  .commit()
