from __future__ import annotations

import os
import re
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader

from ..core.models import CrewProject, ProcessType


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


def _build_team_context(
    project: CrewProject,
) -> Dict[str, Any]:

    model_name = "gpt-4o-mini"

    if (
        project.language_models
        and project.language_models[0].model_name
    ):
        extracted_model = (
            project.language_models[0]
            .model_name
            .strip()
        )

        if extracted_model:
            model_name = extracted_model
    """
    team_type = (
        "SelectorGroupChat"
        if project.process == ProcessType.HIERARCHICAL
        else "RoundRobinGroupChat"
    )
    """
    team_type = "RoundRobinGroupChat"

    ordered_tasks = []

    task_map = {
        t.var_name: t
        for t in project.tasks
    }

    step_map = {
        step.step_order: step
        for step in project.workflow_steps
    }
    
    workflow_patterns = getattr(project, "workflow_patterns", [])

    if workflow_patterns:
        root_patterns = [
            p for p in workflow_patterns
            if getattr(p, "is_root", False)
        ]

        def collect_tasks(pattern):
            for order in pattern.workflow_step_orders:
                step = next(
                    (s for s in project.workflow_steps if s.step_order == order),
                    None,
                )
                if not step:
                    continue

                task = task_map.get(step.task_var_name)
                if task and task not in ordered_tasks:
                    ordered_tasks.append(task)

            for child_iri in pattern.sub_patterns:
                child = next(
                    (p for p in workflow_patterns if p.iri == child_iri),
                    None,
                )
                if child:
                    collect_tasks(child)

        for root in root_patterns:
            collect_tasks(root)

    # Fall back to workflow steps if root-pattern traversal found nothing
    # (e.g. the pattern exists but is_root was not set in the KG).
    if not ordered_tasks and project.workflow_steps:
        for step in sorted(
            project.workflow_steps,
            key=lambda s: s.step_order,
        ):
            task = task_map.get(step.task_var_name)
            if task and task not in ordered_tasks:
                ordered_tasks.append(task)

    if not ordered_tasks:
        ordered_tasks = project.tasks

    workflow_patterns = getattr(project, "workflow_patterns", [])

    root_patterns = [
        p for p in workflow_patterns
        if getattr(p, "is_root", False)
    ]

    pattern_map = {
        p.iri: p
        for p in workflow_patterns
    }

    pattern_metadata = {}

    for pattern in workflow_patterns:
        agent_names = []
        pattern_tasks = []
        prompt_parts = []

        for order in pattern.workflow_step_orders:
            step = step_map.get(order)
            if not step:
                continue

            task = task_map.get(step.task_var_name)
            if not task:
                continue

            pattern_tasks.append(task)

            if (
                task.agent_var_name
                and task.agent_var_name not in agent_names
            ):
                agent_names.append(task.agent_var_name)

            prompt_parts.append(
                f"""
    Task:
    {task.description}

    Expected Output:
    {task.expected_output}
    """.strip()
            )

        pattern_metadata[pattern.iri] = {
            "agents": agent_names,
            "tasks": pattern_tasks,
            "prompt": "\n\n".join(prompt_parts),
        }

    def build_pattern_tree(pattern):
        meta = pattern_metadata[pattern.iri]

        return {
            "pattern": pattern,
            "agents": meta["agents"],
            "tasks": meta["tasks"],
            "prompt": meta["prompt"],
            "children": [
                build_pattern_tree(pattern_map[child])
                for child in pattern.sub_patterns
                if child in pattern_map
            ],
        }

    workflow_tree = [
        build_pattern_tree(root)
        for root in root_patterns
    ]

    if not ordered_tasks:

        default_prompt = """

Have a conversation according to your roles.

Stay in character.

End naturally when appropriate.

"""

    else:

        default_prompt = None
    
    tool_defs = []

    for tool in project.tools:
        tool_defs.append(
            {
                "var_name": tool.var_name,
                "class_name": tool.class_name,
                "description": tool.description,
            }
        )

    termination = {
        "max_messages": 20,
        "text_mention": None,
    }

    configs = []

    for agent in project.agents:
        configs.extend(agent.configs)

    for tool in project.tools:
        configs.extend(tool.configs)

    for config in configs:
        key = config.key.lower()

        if key == "max_turns":
            try:
                termination["max_messages"] = max(
                    int(config.value) * max(len(project.agents), 1),
                    10,
                )
            except (TypeError, ValueError):
                # May be a compound string like "max_turns=2; summary_method=..."
                match = re.search(r'max_turns\s*=\s*(\d+)', str(config.value))
                if match:
                    termination["max_messages"] = max(
                        int(match.group(1)) * max(len(project.agents), 1),
                        10,
                    )

        elif key == "initiate_chat_params":
            # Compound string e.g. "max_turns=2; summary_method='last_msg'; ..."
            match = re.search(r'max_turns\s*=\s*(\d+)', str(config.value))
            if match:
                termination["max_messages"] = max(
                    int(match.group(1)) * max(len(project.agents), 1),
                    10,
                )

        elif key == "termination_condition":
            value = str(config.value)
            if "TERMINATE" in value:
                termination["text_mention"] = "TERMINATE"

        elif key == "is_termination_msg":
            # Parse lambda strings like: lambda msg: "some text" in msg["content"]
            # Extract the quoted string used as the termination trigger.
            value = str(config.value)
            match = re.search(r'["\']([^"\']+)["\']', value)
            if match and not termination["text_mention"]:
                termination["text_mention"] = match.group(1)

    return {
        "project": project,
        "model_name": model_name,
        "team_type": team_type,
        "ordered_tasks": ordered_tasks,
        "default_prompt": default_prompt,
        "tool_defs": tool_defs,
        "termination": termination,
        "workflow_patterns": workflow_patterns,
        "root_patterns": root_patterns,
        "pattern_map": pattern_map,
        "workflow_tree": workflow_tree,
        "pattern_metadata": pattern_metadata,
        "pattern_tasks": {
            iri: meta["tasks"]
            for iri, meta in pattern_metadata.items()
        },
        "pattern_prompts": {
            iri: meta["prompt"]
            for iri, meta in pattern_metadata.items()
        },
    }



def _build_main_context(
    project: CrewProject,
) -> Dict[str, Any]:

    return {
        "crew_name": project.crew_name,
        "input_variables": project.input_variables,
    }

def _build_tool_context(project: CrewProject):

    tool_defs = []

    for tool in project.tools:

        tool_defs.append(
            {
                "var_name": tool.var_name,
                "class_name": tool.class_name,
                "description": tool.description,
                "configs": tool.configs,
            }
        )

    return tool_defs

def generate_project(
    project: CrewProject,
    output_dir: str,
) -> str:

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    env = _create_jinja_env()

    team_template = env.get_template(
        "team.py.j2"
    )

    team_ctx = _build_team_context(
        project
    )

    with open(
        os.path.join(output_dir, "team.py"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(
            team_template.render(
                **team_ctx
            )
        )

    main_template = env.get_template(
        "main.py.j2"
    )

    main_ctx = _build_main_context(
        project
    )

    with open(
        os.path.join(output_dir, "main.py"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(
            main_template.render(
                **main_ctx
            )
        )

    requirements = """
autogen-agentchat>=0.4.0
autogen-ext>=0.4.0
openai
python-dotenv
"""

    with open(
        os.path.join(
            output_dir,
            "requirements.txt",
        ),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(
            requirements.strip()
        )

    return output_dir