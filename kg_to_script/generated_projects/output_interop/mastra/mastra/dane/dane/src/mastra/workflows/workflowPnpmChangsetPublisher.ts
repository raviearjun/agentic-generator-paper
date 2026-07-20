/**
 * Workflow: workflow_pnpm_changset_publisher
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { danePackagePublisher } from '../agents'

// ── Workflow Steps ──

const taskPkgGetPacakgesToPublish = createStep({
  id: 'task_pkg_get_pacakges_to_publish',
  description: `Please analyze the following monorepo directories and identify packages that need pnpm publishing:`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Please analyze the following monorepo directories and identify packages that need pnpm publishing:
CRITICAL: This step is about planning. We do not want to build anything. All packages MUST be placed in the correct order.

Publish Requirements:
- @mastra/core first, MUST be before any other package
- all packages in correct dependency order before building
- Identify packages that have changes requiring a new pnpm publish
- Include create-mastra in the packages list if changes exist
- EXCLUDE @mastra/dane from consideration

Please list all packages that need building grouped by their directory.
DO NOT NOT USE the 'pnpmBuild' tool during this step.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await danePackagePublisher.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskPkgAssemblePackages = createStep({
  id: 'task_pkg_assemble_packages',
  description: `Assemble file system paths for the packages reported by the agent and prepare build sets`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Assemble file system paths for the packages reported by the agent and prepare build sets
    // TODO: Implement step logic
    throw new Error('task_pkg_assemble_packages not implemented yet')
  },
})

const taskPkgBuildPackages = createStep({
  id: 'task_pkg_build_packages',
  description: `Build packages using pnpmBuild tool for each package path (sequential and parallel phases)`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Build packages using pnpmBuild tool for each package path (sequential and parallel phases)
    // TODO: Implement step logic
    throw new Error('task_pkg_build_packages not implemented yet')
  },
})

const taskPkgVerifyBuild = createStep({
  id: 'task_pkg_verify_build',
  description: `Verify dist artifacts exist for all built packages`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // Verify dist artifacts exist for all built packages
    // TODO: Implement step logic
    throw new Error('task_pkg_verify_build not implemented yet')
  },
})

const taskPkgPublishChangeset = createStep({
  id: 'task_pkg_publish_changeset',
  description: `All packages have been built and verified. Publish the changeset for the verified packages and ensure atomic publish and error reporting.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `All packages have been built and verified. Publish the changeset for the verified packages and ensure atomic publish and error reporting.

Context from prior steps:
${JSON.stringify(context)}`
    const result = await danePackagePublisher.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskPkgSetLatestDistTag = createStep({
  id: 'task_pkg_set_latest_dist_tag',
  description: `Update npm dist-tag for published packages (agent assisted)`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Update npm dist-tag for published packages (agent assisted)

Context from prior steps:
${JSON.stringify(context)}`
    const result = await danePackagePublisher.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_pnpm_changset_publisher
 */
export const workflowPnpmChangsetPublisher = createWorkflow({
  id: 'workflow_pnpm_changset_publisher',
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  steps: [taskPkgGetPacakgesToPublish, taskPkgAssemblePackages, taskPkgBuildPackages, taskPkgVerifyBuild, taskPkgPublishChangeset, taskPkgSetLatestDistTag],
})
  .then(taskPkgGetPacakgesToPublish)
  .then(taskPkgAssemblePackages)
  .then(taskPkgBuildPackages)
  .then(taskPkgVerifyBuild)
  .then(taskPkgPublishChangeset)
  .then(taskPkgSetLatestDistTag)
  .commit()
