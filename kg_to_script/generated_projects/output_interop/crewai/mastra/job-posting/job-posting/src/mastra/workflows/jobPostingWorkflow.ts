/**
 * Workflow: job_posting_workflow
 *
 * Auto-generated from AgentO Knowledge Graph
 */

import { createWorkflow, createStep } from '@mastra/core/workflows'
import { z } from 'zod'

// Import agents used by workflow steps
import { researchAgent, writerAgent, reviewAgent } from '../agents'

// ── Workflow Steps ──

const researchCompanyCultureTask = createStep({
  id: 'research_company_culture_task',
  description: `Analyze the provided company website and the hiring manager's company's domain {company_domain}, description {company_description}. Focus on understanding the company's culture, values, and mission. Identify unique selling points and specific projects or achievements highlighted on the site. Compile a report summarizing these insights, specifically how they can be leveraged in a job posting to attract the right candidates.`,
  inputSchema: z.object({company_domain: z.string(), company_description: z.string()}),
  outputSchema: z.object({hiring_needs: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Analyze the provided company website and the hiring manager's company's domain ${context.company_domain ?? ''}, description ${context.company_description ?? ''}. Focus on understanding the company's culture, values, and mission. Identify unique selling points and specific projects or achievements highlighted on the site. Compile a report summarizing these insights, specifically how they can be leveraged in a job posting to attract the right candidates.`
    const result = await researchAgent.generate(prompt)
    return {
      ...context,
      hiring_needs: context.hiring_needs ?? result.text,
    }
  },
})

const researchRoleRequirementsTask = createStep({
  id: 'research_role_requirements_task',
  description: `Based on the hiring manager's needs: {hiring_needs}, identify the key skills, experiences, and qualities the ideal candidate should possess for the role. Consider the company's current projects, its competitive landscape, and industry trends. Prepare a list of recommended job requirements and qualifications that align with the company's needs and values.`,
  inputSchema: z.object({hiring_needs: z.string()}),
  outputSchema: z.object({hiring_needs: z.string(), company_description: z.string(), specific_benefits: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Based on the hiring manager's needs: ${context.hiring_needs ?? ''}, identify the key skills, experiences, and qualities the ideal candidate should possess for the role. Consider the company's current projects, its competitive landscape, and industry trends. Prepare a list of recommended job requirements and qualifications that align with the company's needs and values.`
    const result = await researchAgent.generate(prompt)
    return {
      ...context,
      hiring_needs: context.hiring_needs ?? result.text,
      company_description: context.company_description ?? result.text,
      specific_benefits: context.specific_benefits ?? result.text,
    }
  },
})

const draftJobPostingTask = createStep({
  id: 'draft_job_posting_task',
  description: `Draft a job posting for the role described by the hiring manager: {hiring_needs}. Use the insights on {company_description} to start with a compelling introduction, followed by a detailed role description, responsibilities, and required skills and qualifications. Ensure the tone aligns with the company's culture and incorporate any unique benefits or opportunities offered by the company. Specific benefits: {specific_benefits}.`,
  inputSchema: z.object({hiring_needs: z.string(), company_description: z.string(), specific_benefits: z.string()}),
  outputSchema: z.object({hiring_needs: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Draft a job posting for the role described by the hiring manager: ${context.hiring_needs ?? ''}. Use the insights on ${context.company_description ?? ''} to start with a compelling introduction, followed by a detailed role description, responsibilities, and required skills and qualifications. Ensure the tone aligns with the company's culture and incorporate any unique benefits or opportunities offered by the company. Specific benefits: ${context.specific_benefits ?? ''}.`
    const result = await writerAgent.generate(prompt)
    return {
      ...context,
      hiring_needs: context.hiring_needs ?? result.text,
    }
  },
})

const reviewAndEditJobPostingTask = createStep({
  id: 'review_and_edit_job_posting_task',
  description: `Review the draft job posting for the role {hiring_needs}. Check for clarity, engagement, grammatical accuracy, and alignment with the company's culture and values. Edit and refine the content, ensuring it speaks directly to the desired candidates and accurately reflects the role's unique benefits and opportunities. Provide feedback for any necessary revisions.`,
  inputSchema: z.object({hiring_needs: z.string()}),
  outputSchema: z.object({company_domain: z.string()}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Review the draft job posting for the role ${context.hiring_needs ?? ''}. Check for clarity, engagement, grammatical accuracy, and alignment with the company's culture and values. Edit and refine the content, ensuring it speaks directly to the desired candidates and accurately reflects the role's unique benefits and opportunities. Provide feedback for any necessary revisions.`
    const result = await reviewAgent.generate(prompt)
    return {
      ...context,
      company_domain: context.company_domain ?? result.text,
    }
  },
})

const industryAnalysisTask = createStep({
  id: 'industry_analysis_task',
  description: `Conduct an in-depth analysis of the industry related to the company's domain {company_domain}. Investigate current trends, challenges, and opportunities within the industry, utilizing market reports, recent developments, and expert opinions. Assess how these factors could impact the role being hired for and the overall attractiveness of the position to potential candidates.`,
  inputSchema: z.object({company_domain: z.string()}),
  outputSchema: z.object({}),
  execute: async ({ inputData }) => {
    // context accumulates every field seen so far (this step's own inputData,
    // which already carries forward everything prior steps produced) so that
    // {placeholder} references below can resolve to real values instead of
    // being sent to the agent as inert literal text.
    const context = inputData as Record<string, string>
    const prompt = `Conduct an in-depth analysis of the industry related to the company's domain ${context.company_domain ?? ''}. Investigate current trends, challenges, and opportunities within the industry, utilizing market reports, recent developments, and expert opinions. Assess how these factors could impact the role being hired for and the overall attractiveness of the position to potential candidates.`
    const result = await researchAgent.generate(prompt)
    return { ...context, output: result.text }
  },
})

// ── Workflow Definition ──

/**
 * job_posting_workflow
 */
export const jobPostingWorkflow = createWorkflow({
  id: 'job_posting_workflow',
  inputSchema: z.object({company_domain: z.string(), company_description: z.string()}),
  outputSchema: z.object({}),
  steps: [researchCompanyCultureTask, researchRoleRequirementsTask, draftJobPostingTask, reviewAndEditJobPostingTask, industryAnalysisTask],
})
  .then(researchCompanyCultureTask)
  .then(researchRoleRequirementsTask)
  .then(draftJobPostingTask)
  .then(reviewAndEditJobPostingTask)
  .then(industryAnalysisTask)
  .commit()
