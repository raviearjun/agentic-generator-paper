from __future__ import annotations

import os
import re
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader

from ..core.models import (
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
        tool_defs.append({
            "var_name": tool.var_name,
            "class_name": tool.class_name,
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
    return {
        "name": project.name,
        "input_variables": project.input_variables,
    }


def _build_tool_context(project: AutoGenProject):
    tool_defs = []
    for tool in project.tools:
        tool_defs.append({
            "var_name": tool.var_name,
            "class_name": tool.class_name,
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
