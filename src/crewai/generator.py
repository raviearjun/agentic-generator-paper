"""
Layer 3 – File Generation

Generates a complete CrewAI project directory from a CrewProject IR:
  - config/agents.yaml  (via PyYAML)
  - config/tasks.yaml   (via PyYAML)
  - crew.py             (via Jinja2)
  - main.py             (via Jinja2)
  - .env                (plain text)

Design decisions:
  - YAML files use PyYAML (safe_dump) — never f-strings
  - Python files use Jinja2 templates — never f-strings
  - Output directory mirrors official CrewAI structure
"""

from __future__ import annotations

import os
from collections import OrderedDict
from typing import Any, Dict, List

import yaml
from jinja2 import Environment, FileSystemLoader

from .models import AgentModel, CrewProject, TaskModel, ToolModel


# ─────────────────────── YAML helpers ───────────────────────

class _LiteralStr(str):
    """String subclass that PyYAML will dump as a block-scalar literal."""
    pass


def _literal_representer(dumper: yaml.Dumper, data: _LiteralStr) -> Any:
    """Represent _LiteralStr as YAML block scalar (|)."""
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


def _ordered_dict_representer(dumper: yaml.Dumper, data: OrderedDict) -> Any:
    """Represent OrderedDict as regular YAML mapping (preserving order)."""
    return dumper.represent_mapping("tag:yaml.org,2002:map", data.items())


def _setup_yaml_dumper() -> type:
    """Create a custom YAML Dumper with our representers."""
    dumper = yaml.Dumper
    dumper.add_representer(_LiteralStr, _literal_representer)
    dumper.add_representer(OrderedDict, _ordered_dict_representer)
    return dumper


def _clean_text(text: str) -> str:
    """Normalize line endings and trim whitespace."""
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def _wrap_multiline(text: str) -> Any:
    """If text is multiline or long, wrap as block scalar; otherwise plain."""
    text = _clean_text(text)
    if "\n" in text or len(text) > 100:
        return _LiteralStr(text + "\n")
    return text


# ─────────────────────── YAML builders ───────────────────────

def build_agents_yaml(project: CrewProject) -> str:
    """
    Build agents.yaml content from the CrewProject IR.

    Each agent key maps to: role, goal, backstory
    (tools, llm, etc. are in crew.py, not YAML)
    """
    data = OrderedDict()
    for agent in project.agents:
        entry = OrderedDict()
        entry["role"] = _wrap_multiline(agent.role)
        entry["goal"] = _wrap_multiline(agent.goal)
        entry["backstory"] = _wrap_multiline(agent.backstory)
        data[agent.var_name] = entry

    dumper = _setup_yaml_dumper()
    return yaml.dump(data, Dumper=dumper, default_flow_style=False, allow_unicode=True, sort_keys=False)


def build_tasks_yaml(project: CrewProject) -> str:
    """
    Build tasks.yaml content from the CrewProject IR.

    Each task key maps to: description, expected_output
    (agent, context, output_json are in crew.py, not YAML)
    """
    data = OrderedDict()
    for task in project.tasks:
        entry = OrderedDict()
        entry["description"] = _wrap_multiline(task.description)
        entry["expected_output"] = _wrap_multiline(task.expected_output)
        data[task.var_name] = entry

    dumper = _setup_yaml_dumper()
    return yaml.dump(data, Dumper=dumper, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ─────────────────────── Jinja2 setup ───────────────────────

def _create_jinja_env() -> Environment:
    """Create Jinja2 environment with templates directory."""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    # Custom filter: escape a value for embedding in Python single-quoted string
    def _py_escape(s: str) -> str:
        if not s:
            return ""
        return s.replace("\\", "\\\\").replace("'", "\\'")

    env.filters["py_escape"] = _py_escape
    return env


# ─────────────────────── Jinja2 context builders ───────────────────────

def _build_tool_imports(project: CrewProject) -> List[Dict[str, Any]]:
    """
    Determine tool import statements and instantiation code.

    Known CrewAI tool classes are mapped to crewai_tools imports.
    Unknown tools get stub comments.
    """
    KNOWN_TOOLS = {
        "SerperDevTool": {"module": "crewai_tools", "class": "SerperDevTool", "args": ""},
        "ScrapeWebsiteTool": {"module": "crewai_tools", "class": "ScrapeWebsiteTool", "args": ""},
        "WebsiteSearchTool": {"module": "crewai_tools", "class": "WebsiteSearchTool", "args": ""},
        "FileReadTool": {"module": "crewai_tools", "class": "FileReadTool", "args": ""},
        "TXTSearchTool": {"module": "crewai_tools", "class": "TXTSearchTool", "args": ""},
        "DirectoryReadTool": {"module": "crewai_tools", "class": "DirectoryReadTool", "args": ""},
        "DOCXSearchTool": {"module": "crewai_tools", "class": "DOCXSearchTool", "args": ""},
        "PDFSearchTool": {"module": "crewai_tools", "class": "PDFSearchTool", "args": ""},
        "CSVSearchTool": {"module": "crewai_tools", "class": "CSVSearchTool", "args": ""},
        "JSONSearchTool": {"module": "crewai_tools", "class": "JSONSearchTool", "args": ""},
        "MDXSearchTool": {"module": "crewai_tools", "class": "MDXSearchTool", "args": ""},
        "YoutubeVideoSearchTool": {"module": "crewai_tools", "class": "YoutubeVideoSearchTool", "args": ""},
    }

    tool_imports: List[Dict[str, Any]] = []
    for tool in project.tools:
        class_name = tool.class_name

        # Try exact match
        if class_name in KNOWN_TOOLS:
            info = KNOWN_TOOLS[class_name]
        else:
            # Try fuzzy match (remove "Tool" suffix or lowercase compare)
            info = None
            for known_name, known_info in KNOWN_TOOLS.items():
                if known_name.lower() == class_name.lower():
                    info = known_info
                    class_name = known_name
                    break

        # Build constructor args from tool configs
        config_args = ""
        if tool.configs:
            args_parts = []
            for cfg in tool.configs:
                args_parts.append(f'{cfg.key}="{cfg.value}"')
            config_args = ", ".join(args_parts)

        tool_imports.append({
            "var_name": tool.var_name,
            "class_name": class_name,
            "module": info["module"] if info else None,
            "args": config_args or (info["args"] if info else ""),
            "is_known": info is not None,
            "description": tool.description[:80] if tool.description else "",
        })

    return tool_imports


def _build_crew_context(project: CrewProject) -> Dict[str, Any]:
    """Build the complete Jinja2 template context for crew.py."""
    tool_imports = _build_tool_imports(project)

    # Group tool imports by module for clean import statements
    import_groups: Dict[str, List[str]] = {}
    for ti in tool_imports:
        if ti["is_known"] and ti["module"]:
            module = ti["module"]
            if module not in import_groups:
                import_groups[module] = []
            if ti["class_name"] not in import_groups[module]:
                import_groups[module].append(ti["class_name"])

    # Check if any agent uses a non-default LLM
    has_custom_llm = any(
        a.llm and a.llm.provider
        for a in project.agents
    )

    return {
        "crew_name": project.crew_name,
        "crew_var_name": project.crew_var_name,
        "process": project.process.value,
        "agents": project.agents,
        "tasks": project.tasks,
        "tools": project.tools,
        "tool_imports": tool_imports,
        "import_groups": import_groups,
        "has_custom_llm": has_custom_llm,
        "has_tools": len(project.tools) > 0,
    }


def _build_main_context(project: CrewProject) -> Dict[str, Any]:
    """Build the complete Jinja2 template context for main.py."""
    return {
        "crew_name": project.crew_name,
        "crew_var_name": project.crew_var_name,
        "input_variables": project.input_variables,
    }


# ─────────────────────── .env.example builder ───────────────────────

# Maps tool class names to the env vars they require at runtime.
_TOOL_ENV_VARS: Dict[str, List[str]] = {
    "SerperDevTool":         ["SERPER_API_KEY"],
    "BrowserbaseLoadTool":   ["BROWSERBASE_API_KEY"],
    "SECTools":              ["SEC_API_API_KEY"],
    "ScrapeWebsiteTool":     [],   # no extra key needed
    "WebsiteSearchTool":     [],
    "FileReadTool":          [],
    "TXTSearchTool":         [],
    "DirectoryReadTool":     [],
    "DOCXSearchTool":        [],
    "PDFSearchTool":         [],
    "CSVSearchTool":         [],
    "JSONSearchTool":        [],
    "MDXSearchTool":         [],
    "YoutubeVideoSearchTool": [],
}

# Maps LLM provider to its required env vars.
_LLM_PROVIDER_ENV_VARS: Dict[str, List[str]] = {
    "openai":      ["OPENAI_API_KEY"],
    "azure":       ["AZURE_OPENAI_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT", "AZURE_OPENAI_VERSION"],
    "azureopenai": ["AZURE_OPENAI_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT", "AZURE_OPENAI_VERSION"],
    "anthropic":   ["ANTHROPIC_API_KEY"],
    "ollama":      [],   # runs locally, no key needed
    "nvidia":      ["NVIDIA_API_KEY"],
    "nvidia_nim":  ["NVIDIA_API_KEY"],
    "cohere":      ["COHERE_API_KEY"],
    "gemini":      ["GEMINI_API_KEY"],
    "groq":        ["GROQ_API_KEY"],
    "mistral":     ["MISTRAL_API_KEY"],
    "huggingface": ["HUGGINGFACEHUB_API_TOKEN"],
}


def build_env_example(project: CrewProject) -> str:
    """
    Generate .env.example content from a CrewProject IR.

    Logic:
      - OPENAI_API_KEY is always included (default LLM unless overridden).
      - If any agent uses a non-default LLM provider, swap/add provider keys.
      - Tool-specific keys (e.g. SERPER_API_KEY) are added based on tools used.
      - Keys already defined in project.env_vars (from KG) are merged in.
      - All values are placeholders, never real secrets.
    """
    # ordered dict to preserve insertion order and avoid duplicates
    entries: Dict[str, str] = {}

    # ── 1. Default: always start with OPENAI_API_KEY ──
    entries["OPENAI_API_KEY"] = "your_openai_api_key_here"

    # ── 2. LLM provider keys ──
    for agent in project.agents:
        if agent.llm and agent.llm.provider:
            provider_key = agent.llm.provider.lower().replace("-", "").replace("_", "")
            for prov_pattern, env_vars in _LLM_PROVIDER_ENV_VARS.items():
                if prov_pattern.replace("_", "") in provider_key:
                    # If non-OpenAI provider found, remove the default OPENAI key
                    if prov_pattern not in ("openai",):
                        entries.pop("OPENAI_API_KEY", None)
                    for var in env_vars:
                        entries[var] = f"your_{var.lower()}_here"
                    break

    # ── 3. Tool-specific API keys ──
    for tool in project.tools:
        class_key = tool.class_name
        # exact match first, then case-insensitive
        matched = _TOOL_ENV_VARS.get(class_key)
        if matched is None:
            for k, v in _TOOL_ENV_VARS.items():
                if k.lower() == class_key.lower():
                    matched = v
                    break
        if matched:
            for var in matched:
                entries[var] = f"your_{var.lower()}_here"

    # ── 4. Merge env_vars already found in the KG (overwrite placeholder with KG value) ──
    for cfg in project.env_vars:
        entries[cfg.key] = cfg.value

    # ── 5. Build file content with section comments ──
    lines: List[str] = [
        "# .env.example – copy to .env and fill in your actual keys",
        "# Never commit the real .env file to version control.",
        "",
    ]

    # Separate LLM keys from tool keys for readability
    llm_vars   = {"OPENAI_API_KEY", "ANTHROPIC_API_KEY", "AZURE_OPENAI_KEY",
                  "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT", "AZURE_OPENAI_VERSION",
                  "NVIDIA_API_KEY", "COHERE_API_KEY", "GEMINI_API_KEY",
                  "GROQ_API_KEY", "MISTRAL_API_KEY", "HUGGINGFACEHUB_API_TOKEN"}
    tool_keys  = {k: v for k, v in entries.items() if k not in llm_vars}
    model_keys = {k: v for k, v in entries.items() if k in llm_vars}

    if model_keys:
        lines.append("# LLM API Keys")
        for k, v in model_keys.items():
            lines.append(f"{k}={v}")
        lines.append("")

    if tool_keys:
        lines.append("# Tool API Keys")
        for k, v in tool_keys.items():
            lines.append(f"{k}={v}")
        lines.append("")

    return "\n".join(lines)


# ─────────────────────── pyproject.toml builder ───────────────────────

# Maps LLM provider names (from KG :LanguageModel) to their PyPI packages.
# Used to detect extra dependencies beyond the default crewai[tools].
_LLM_PROVIDER_PACKAGES: Dict[str, List[str]] = {
    "azure":       ["langchain-openai>=0.3.0"],
    "azureopenai": ["langchain-openai>=0.3.0"],
    "anthropic":   ["anthropic>=0.60.0"],
    "ollama":      ["langchain-community>=0.3.0"],
    "nvidia":      ["langchain-nvidia-ai-endpoints>=0.3.0"],
    "nvidia_nim":  ["langchain-nvidia-ai-endpoints>=0.3.0"],
    "cohere":      ["cohere>=5.0.0"],
    "gemini":      ["google-generativeai>=0.8.0"],
    "groq":        ["groq>=0.9.0"],
    "mistral":     ["mistralai>=1.0.0"],
    "huggingface": ["huggingface-hub>=0.24.0"],
}


def build_pyproject_toml(project: CrewProject) -> str:
    """
    Generate pyproject.toml content from a CrewProject IR.

    Dependencies are determined programmatically:
      - crewai[tools]  : always required
      - python-dotenv  : always required (for .env / API keys)
      - LLM packages   : only when agents use a non-default (non-OpenAI) provider
      - unknown tools  : listed as a TODO comment for the user
    """
    # ── Project name: strip trailing "_crew" to mirror official examples ──
    raw_name = project.crew_var_name or "my_crew"
    pkg_name = raw_name[:-5] if raw_name.endswith("_crew") else raw_name

    # ── Base dependencies (always present) ──
    deps: List[str] = [
        'crewai[tools]>=0.152.0',
        'python-dotenv>=1.0.1',
    ]
    unknown_tools: List[str] = []

    # ── Collect tool class names that are NOT in KNOWN_TOOLS ──
    known_classnames = {k.lower() for k in [
        "SerperDevTool", "ScrapeWebsiteTool", "WebsiteSearchTool",
        "FileReadTool", "TXTSearchTool", "DirectoryReadTool",
        "DOCXSearchTool", "PDFSearchTool", "CSVSearchTool",
        "JSONSearchTool", "MDXSearchTool", "YoutubeVideoSearchTool",
    ]}
    for tool in project.tools:
        if tool.class_name.lower() not in known_classnames:
            unknown_tools.append(tool.class_name)

    # ── Collect extra packages for non-default LLM providers ──
    seen_providers: set = set()
    for agent in project.agents:
        if agent.llm and agent.llm.provider:
            provider_key = agent.llm.provider.lower().replace("-", "").replace("_", "")
            if provider_key not in seen_providers:
                seen_providers.add(provider_key)
                for prov_pattern, pkgs in _LLM_PROVIDER_PACKAGES.items():
                    if prov_pattern.replace("_", "") in provider_key:
                        deps.extend(pkgs)
                        break

    # ── Build TOML string manually (no extra dependency on tomllib/tomli_w) ──
    lines: List[str] = [
        "[project]",
        f'name = "{pkg_name}"',
        'version = "0.1.0"',
        f'description = "{project.description[:80] if project.description else ""}"',
        'authors = [{name = "Your Name", email = "you@example.com"}]',
        'readme = "README.md"',
        'requires-python = ">=3.10,<=3.13"',
        "",
        "dependencies = [",
    ]

    for dep in deps:
        lines.append(f'    "{dep}",')  # produces:  "crewai[tools]>=0.152.0",

    # Add unknown tool stubs as comments so user knows what to add
    for tool_cls in unknown_tools:
        lines.append(f'    # TODO: add PyPI package for custom tool "{tool_cls}"')

    lines += [
        "]",
        "",
        "[project.scripts]",
        f'{pkg_name} = "main:run"',
        'train      = "main:train"',
        "",
        "[tool.uv]",
        "dev-dependencies = []",
        "",
        "[build-system]",
        'requires      = ["hatchling"]',
        'build-backend = "hatchling.build"',
        "",
    ]

    return "\n".join(lines)


# ─────────────────────── Public API ───────────────────────

def generate_project(project: CrewProject, output_dir: str) -> str:
    """
    Generate a complete CrewAI project directory from a CrewProject IR.

    Output structure:
        <output_dir>/
        ├── pyproject.toml
        ├── .env.example        ← always generated (safe placeholders)
        ├── .env                ← only when KG defines env_vars
        ├── config/
        │   ├── agents.yaml
        │   └── tasks.yaml
        ├── crew.py
        └── main.py

    Returns:
        The output directory path.
    """
    # Create directory structure
    config_dir = os.path.join(output_dir, "config")
    os.makedirs(config_dir, exist_ok=True)

    # ── Layer 3A: YAML generation (PyYAML) ──
    agents_yaml = build_agents_yaml(project)
    tasks_yaml = build_tasks_yaml(project)

    with open(os.path.join(config_dir, "agents.yaml"), "w", encoding="utf-8") as f:
        f.write(agents_yaml)

    with open(os.path.join(config_dir, "tasks.yaml"), "w", encoding="utf-8") as f:
        f.write(tasks_yaml)

    # ── Layer 3B: Python generation (Jinja2) ──
    env = _create_jinja_env()

    # crew.py
    crew_template = env.get_template("crew.py.j2")
    crew_ctx = _build_crew_context(project)
    crew_code = crew_template.render(**crew_ctx)
    with open(os.path.join(output_dir, "crew.py"), "w", encoding="utf-8") as f:
        f.write(crew_code)

    # main.py
    main_template = env.get_template("main.py.j2")
    main_ctx = _build_main_context(project)
    main_code = main_template.render(**main_ctx)
    with open(os.path.join(output_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_code)

    # ── .env file (only when KG explicitly provides values) ──
    if project.env_vars:
        with open(os.path.join(output_dir, ".env"), "w", encoding="utf-8") as f:
            for ev in project.env_vars:
                f.write(f"{ev.key}={ev.value}\n")

    # ── .env.example (always generated – safe placeholder version) ──
    env_example_content = build_env_example(project)
    with open(os.path.join(output_dir, ".env.example"), "w", encoding="utf-8") as f:
        f.write(env_example_content)

    # ── pyproject.toml ──
    pyproject_content = build_pyproject_toml(project)
    with open(os.path.join(output_dir, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(pyproject_content)

    print(
        f"  [Generated] {output_dir}/ "
        f"(agents.yaml, tasks.yaml, crew.py, main.py, pyproject.toml, .env.example"
        f"{', .env' if project.env_vars else ''})"
    )

    return output_dir
