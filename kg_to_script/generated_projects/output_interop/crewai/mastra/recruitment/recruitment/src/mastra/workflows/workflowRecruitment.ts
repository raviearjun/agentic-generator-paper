/**
 * Workflow: workflow_recruitment
 *
 * Auto-generated from AgentO Knowledge Graph
 *
 * Workflow pattern representing Crew.process=Process.sequential
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { researcher, matcher, communicator, reporter } from '../agents'

// ── Workflow Steps ──

const taskResearchCandidates = createStep({
  id: 'task_research_candidates',
  description: `Conduct thorough research to find potential candidates for the specified job. Utilize various online resources and databases to gather a comprehensive list of potential candidates. Ensure that the candidates meet the job requirements provided.`,
  inputSchema: z.object({job_requirements: z.string()}),
  outputSchema: z.object({job_requirements: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Conduct thorough research to find potential candidates for the specified job. Utilize various online resources and databases to gather a comprehensive list of potential candidates. Ensure that the candidates meet the job requirements provided.

Job Requirements: ${context.job_requirements ?? ''}`
    const result = await researcher.generate(prompt)
    return {
      ...context,
      job_requirements: context.job_requirements ?? result.text,
    }
  },
})

const taskMatchAndScoreCandidates = createStep({
  id: 'task_match_and_score_candidates',
  description: `Evaluate and match the candidates to the best job positions based on their qualifications and suitability. Score each candidate to reflect their alignment with the job requirements. Don't try to scrape people's linkedin, since you don't have access to it.`,
  inputSchema: z.object({job_requirements: z.string()}),
  outputSchema: z.object({job_requirements: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Evaluate and match the candidates to the best job positions based on their qualifications and suitability. Score each candidate to reflect their alignment with the job requirements. Don't try to scrape people's linkedin, since you don't have access to it.

Job Requirements: ${context.job_requirements ?? ''}`
    const result = await matcher.generate(prompt)
    return {
      ...context,
      job_requirements: context.job_requirements ?? result.text,
    }
  },
})

const taskOutreachStrategy = createStep({
  id: 'task_outreach_strategy',
  description: `Develop a comprehensive strategy to reach out to the selected candidates. Create effective outreach methods and templates that can engage the candidates and encourage them to consider the job opportunity.`,
  inputSchema: z.object({job_requirements: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Develop a comprehensive strategy to reach out to the selected candidates. Create effective outreach methods and templates that can engage the candidates and encourage them to consider the job opportunity.

Job Requirements: ${context.job_requirements ?? ''}`
    const result = await communicator.generate(prompt)
    return { ...context, output: result.text }
  },
})

const taskReportCandidates = createStep({
  id: 'task_report_candidates',
  description: `Compile a comprehensive report for recruiters on the best candidates to put forward. Summarize the findings from the previous tasks and provide clear recommendations based on the job requirements.`,
  inputSchema: z.object({}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Compile a comprehensive report for recruiters on the best candidates to put forward. Summarize the findings from the previous tasks and provide clear recommendations based on the job requirements.`
    const result = await reporter.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * workflow_recruitment
 *
 * Workflow pattern representing Crew.process=Process.sequential
 */
export const workflowRecruitment = createWorkflow({
  id: 'workflow_recruitment',
  inputSchema: z.object({job_requirements: z.string()}),
  outputSchema: z.object({}),
  steps: [taskResearchCandidates, taskMatchAndScoreCandidates, taskOutreachStrategy, taskReportCandidates],
})
  .then(taskResearchCandidates)
  .then(taskMatchAndScoreCandidates)
  .then(taskOutreachStrategy)
  .then(taskReportCandidates)
  .commit()
