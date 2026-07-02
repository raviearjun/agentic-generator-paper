from __future__ import annotations

import os
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader

from ...core.models import (
    CapabilityModel,
    ConstraintModel,
    EnvironmentModel,
    GoalModel,
    HumanAgentModel,
    ObjectiveModel,
    ResourceModel,
)
from .models import AutoGenProject


def _create_jinja_env() -> Environment:
    template_dir = os.path.join(
        os.path.dirname(__file__),
        "templates"
    )
    return Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def _build_team_context(project: AutoGenProject) -> Dict[str, Any]:
    model_name = project.model_name or "gpt-4o-mini"

    ordered_tasks = project.ordered_tasks or project.tasks

    default_prompt = None
    if not ordered_tasks:
        default_prompt = (
            "Have a conversation according to your roles.\n"
            "Stay in character.\n"
            "End naturally when appropriate.\n"
        )

    tool_defs = []
    for tool in project.tools:
        # Derive CamelCase class name from tool label (adapter responsibility)
        import re as _re
        class_name = _re.sub(r"[^a-zA-Z0-9]", "", tool.label) if tool.label else tool.var_name
        tool_defs.append({
            "var_name": tool.var_name,
            "class_name": class_name,
            "description": tool.description,
        })

    return {
        "project": project,
        "model_name": model_name,
        "team_type": project.team_type,
        "ordered_tasks": ordered_tasks,
        "default_prompt": default_prompt,
        "tool_defs": tool_defs,
        "goals": project.goals,
        "objectives": project.objectives,
        "human_agents": project.human_agents,
        "environments": project.environments,
        "capabilities": project.capabilities,
        "resources": project.resources,
        "constraints": project.constraints,
    }


def _build_main_context(project: AutoGenProject) -> Dict[str, Any]:
    resolved_steps = []
    seen_task_vars: set = set()

    tasks_by_iri = {t.iri: t for t in project.tasks}
    agents_by_iri = {a.iri: a for a in project.agents}
    human_agents_by_iri = {h.iri: h for h in project.human_agents}

    # Build a global step-IRI → task_var_name map across all workflows so that
    # cross-workflow next_step_iris references are resolved correctly.
    global_step_iri_to_task_var: dict = {}
    for workflow in project.workflows:
        for s in workflow.steps:
            if s.iri:
                global_step_iri_to_task_var[s.iri] = s.task_var_name

    for workflow in project.workflows:
        steps_sorted = sorted(workflow.steps, key=lambda s: s.step_order)
        for i, step in enumerate(steps_sorted):
            # Deduplicate across workflows — same task might appear in multiple flows
            if step.task_var_name in seen_task_vars:
                continue
            seen_task_vars.add(step.task_var_name)

            task = tasks_by_iri.get(step.task_iri)
            task_desc = task.description if (task and task.description) else (step.description or step.task_var_name)
            import re
            agent_var = None
            if (not step.agent_iri or step.agent_iri == "") and task and task.description:
                match = re.search(r"sender:\s*([a-zA-Z0-9_]+)", task.description)
                if match:
                    agent_var = match.group(1)

            if not agent_var:
                agent = agents_by_iri.get(step.agent_iri) or human_agents_by_iri.get(step.agent_iri)
                agent_var = agent.var_name if agent else (re.sub(r"[^a-zA-Z0-9_]", "", step.agent_iri.split("#")[-1]) if step.agent_iri else "agent")

            next_task_vars = []
            for next_iri in step.next_step_iris:
                nxt = global_step_iri_to_task_var.get(next_iri)
                if nxt:
                    next_task_vars.append(nxt)

            if not next_task_vars and i < len(steps_sorted) - 1:
                next_task_vars.append(steps_sorted[i + 1].task_var_name)

            resolved_steps.append({
                "step_var_name": step.var_name or step.task_var_name,
                "task_var_name": step.task_var_name,
                "task_description": task_desc,
                "agent_var": agent_var,
                "next_task_vars": next_task_vars,
            })

    return {
        "project": project,
        "name": project.name,
        "human_agents": project.human_agents,
        "resolved_steps": resolved_steps,
    }


def _build_tool_context(project: AutoGenProject):
    import re as _re
    tool_defs = []
    for tool in project.tools:
        class_name = _re.sub(r"[^a-zA-Z0-9]", "", tool.label) if tool.label else tool.var_name
        tool_defs.append({
            "var_name": tool.var_name,
            "class_name": class_name,
            "description": tool.description,
            "configs": tool.configs,
        })
    return tool_defs


def generate_project(project: AutoGenProject, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)

    env = _create_jinja_env()

    team_template = env.get_template("team.py.j2")
    team_ctx = _build_team_context(project)
    with open(os.path.join(output_dir, "team.py"), "w", encoding="utf-8") as f:
        f.write(team_template.render(**team_ctx))

    main_template = env.get_template("main.py.j2")
    main_ctx = _build_main_context(project)
    with open(os.path.join(output_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_template.render(**main_ctx))

    requirements = """
autogen-agentchat>=0.4.0
autogen-ext>=0.4.0
openai
python-dotenv
"""

    with open(os.path.join(output_dir, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(requirements.strip())

    return output_dir
