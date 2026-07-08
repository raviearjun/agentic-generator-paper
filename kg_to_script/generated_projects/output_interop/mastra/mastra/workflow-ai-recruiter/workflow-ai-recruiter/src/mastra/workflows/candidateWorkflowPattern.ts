/**
 * Workflow: candidate_workflow_pattern
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow to extract candidate information from a resume and generate follow-up questions
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { mastraLlm } from '../agents'

// ── Workflow Steps ──

const gatherCandidateInfoTask = createStep({
  id: 'gather_candidate_info_task',
  description: `You are given this resume text: "\${resumeText}"`,
  inputSchema: z.object({resumeText: z.string()}),
  outputSchema: z.object({candidateName: z.string(), specialty: z.string(), resumeText: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You are given this resume text: "\$${context.resumeText ?? ''}"`
    const result = await mastraLlm.generate(prompt)
    return {
      ...context,
      candidateName: context.candidateName ?? result.text,
      specialty: context.specialty ?? result.text,
      resumeText: context.resumeText ?? result.text,
    }
  },
})

const askAboutSpecialtyTask = createStep({
  id: 'ask_about_specialty_task',
  description: `You are a recruiter. Given the resume below, craft a short question for \${candidateName} about how they got into "\${specialty}". Resume: \${resumeText}`,
  inputSchema: z.object({candidateName: z.string(), specialty: z.string(), resumeText: z.string()}),
  outputSchema: z.object({candidateName: z.string(), resumeText: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You are a recruiter. Given the resume below, craft a short question for \$${context.candidateName ?? ''} about how they got into "\$${context.specialty ?? ''}". Resume: \$${context.resumeText ?? ''}`
    const result = await mastraLlm.generate(prompt)
    return {
      ...context,
      candidateName: context.candidateName ?? result.text,
      resumeText: context.resumeText ?? result.text,
    }
  },
})

const askAboutRoleTask = createStep({
  id: 'ask_about_role_task',
  description: `You are a recruiter. Given the resume below, craft a short question for \${candidateName} asking what interests them most about this role. Resume: \${resumeText}`,
  inputSchema: z.object({candidateName: z.string(), resumeText: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `You are a recruiter. Given the resume below, craft a short question for \$${context.candidateName ?? ''} asking what interests them most about this role. Resume: \$${context.resumeText ?? ''}`
    const result = await mastraLlm.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * candidate_workflow_pattern
 *
 * Workflow to extract candidate information from a resume and generate follow-up questions
 */
export const candidateWorkflowPattern = createWorkflow({
  id: 'candidate_workflow_pattern',
  inputSchema: z.object({resumeText: z.string()}),
  outputSchema: z.object({}),
  steps: [gatherCandidateInfoTask, askAboutSpecialtyTask, askAboutRoleTask],
})
  // NOTE: Branching workflow — simplified to sequential for type compatibility
  // TODO: Implement conditional branching using .branch() API
  .then(gatherCandidateInfoTask)
  .then(askAboutSpecialtyTask)
  .then(askAboutRoleTask)
  .commit()
