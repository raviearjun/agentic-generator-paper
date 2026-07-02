"""
run_experiment.py — Multi-prompt, multi-model KG generation experiment runner.

Usage:
    python run_experiment.py --framework CrewAI --prompt P0 --model chatgpt
    python run_experiment.py --framework all --prompt all --model all
    python run_experiment.py --framework AutoGen --prompt P2 --model gemini --source-dir ../generated_kg/AutoGen

Arguments:
    --framework     Framework name or 'all' (CrewAI | LangGraph | AutoGen | all)
    --prompt        Prompt variant or 'all' (P0 | P1 | P2 | P3 | P4 | all)
    --model         LLM backend or 'all' (chatgpt | gemini | claude | all)
    --source-dir    Optional: path to a specific source folder to process a single example
    --dry-run       Print what would be run without calling the API
    --output-root   Root folder for outputs (default: ../experiment_kg)
    --ontology      Path to ontology file (default: ../agentO.ttl)
    --skip-existing Skip if output file already exists (default: True)

Environment variables required:
    OPENAI_API_KEY     — for ChatGPT models
    GEMINI_API_KEY     — for Gemini models
    ANTHROPIC_API_KEY  — for Claude models

Output structure:
    experiment_kg/
        <framework>/
            <prompt_id>/
                <model>/
                    <example>_instances.ttl
"""

import argparse
import os
import sys
import time
import json
import re
from pathlib import Path

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent.resolve()

PROMPT_FILES = {
    "P0": REPO_ROOT / "prompts" / "baseline.md",
    "P1": REPO_ROOT / "prompts" / "minimal.md",
    "P2": REPO_ROOT / "prompts" / "structured.md",
    "P3": REPO_ROOT / "prompts" / "reasoning.md",
    "P4": REPO_ROOT / "prompts" / "validation.md",
    "P5": REPO_ROOT / "prompts" / "framework_specific.md",
}

# Source folders keyed by framework name.
# Each value points to the folder containing the actual framework source code.
# AutoGen examples are Jupyter notebooks (.ipynb); CrewAI/LangGraph are project dirs.
FRAMEWORK_SOURCES = {
    "CrewAI":    REPO_ROOT / "GT_scripts" / "CrewAI",
    "LangGraph": REPO_ROOT / "GT_scripts" / "LangGraph",
    "AutoGen":   REPO_ROOT / "GT_scripts" / "AutoGen",
    "Mastra AI": REPO_ROOT / "GT_scripts" / "Mastra AI",
}

MODEL_CONFIGS = {
    "chatgpt": {
        "provider": "openai",
        "model":    "gpt-5-mini",
        "env_key":  "OPENAI_API_KEY",
    },
    "gemini": {
        "provider": "google",
        "model":    "gemini-2.5-flash",
        "env_key":  "GEMINI_API_KEY",
    },
    "claude": {
        "provider": "anthropic",
        "model":    "claude-opus-4-8",
        "env_key":  "ANTHROPIC_API_KEY",
    },
}

DEFAULT_ONTOLOGY = REPO_ROOT / "agentO.ttl"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "experiment_kg"


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def load_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".md", ".yaml", ".yml", ".toml", ".env.example", ".ipynb"}
EXCLUDED_DIRS    = {".git", ".github", "venv", "__pycache__", "node_modules",
                    "dist", "build", "docs", "examples", "tests", "test",
                    "experiment_kg", "generated_kg", ".mypy_cache", ".ruff_cache"}

# Top-level subdirs to skip when enumerating examples per framework
FRAMEWORK_EXCLUDED_EXAMPLE_DIRS = {
    "LangGraph": {"utils"},
}


def read_source_files(folder: Path) -> str:
    """Read relevant source files only — skip binaries, generated output, and large files.

    ``folder`` may also be a single file path; in that case only that file is read.
    """
    parts = []
    total = 0
    file_iter = [folder] if folder.is_file() else sorted(folder.rglob("*"))
    for path in file_iter:
        if not path.is_file():
            continue
        # Skip excluded directories
        if any(p in EXCLUDED_DIRS for p in path.parts):
            continue
        # Skip non-source extensions
        if path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        # Skip large files
        try:
            size = path.stat().st_size
        except OSError:
            continue
        try:
            if path.suffix.lower() == ".ipynb":
                # Extract only code cell sources from notebooks
                import json as _json
                nb = _json.loads(path.read_text(encoding="utf-8", errors="strict"))
                cell_texts = []
                for cell in nb.get("cells", []):
                    if cell.get("cell_type") == "code":
                        src = "".join(cell.get("source", []))
                        if src.strip():
                            cell_texts.append(src)
                text = "\n\n".join(cell_texts)
            else:
                text = path.read_text(encoding="utf-8", errors="strict")
        except (UnicodeDecodeError, OSError, Exception):
            continue
        rel = path.name if folder.is_file() else path.relative_to(folder)
        parts.append(f"### {rel}\n\n```\n{text}\n```")
        total += len(text)
    print(f"  [source] {len(parts)} files, {total:,} chars")
    return "\n\n".join(parts)


def build_prompt(prompt_template: str, ontology: str, source_code: str) -> str:
    p = prompt_template.replace("{{ontology}}", ontology)
    p = p.replace("{{source_code}}", source_code)
    return p


EXTRA_PREFIXES = {
    "beam:":    "@prefix beam: <http://w3id.org/beam/core#> .",
    "dcterms:": "@prefix dcterms: <http://purl.org/dc/terms/> .",
    "dc:":      "@prefix dc: <http://purl.org/dc/elements/1.1/> .",
    "skos:":    "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
    "prov:":    "@prefix prov: <http://www.w3.org/ns/prov#> .",
}


def clean_turtle(raw: str) -> str:
    """
    Post-process raw LLM output into valid Turtle:
    1. Strip all markdown code fences (```ttl / ```turtle / ```)
    2. Extract from first @prefix or first Turtle comment, discarding preamble prose
    3. Truncate trailing prose after the last triple
    4. Fix dangling `;` before new subjects or comment section headers
    5. Fix `;` before a new non-indented full triple
    6. Inject missing standard prefix declarations
    """
    # 1. Strip all code fences
    text = re.sub(r"```(?:ttl|turtle|rdf|sparql)?\s*\n?", "", raw, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # 2. Find where Turtle content starts (first @prefix or a comment that precedes @prefix)
    lines = text.split("\n")
    first_prefix = next((i for i, l in enumerate(lines) if l.strip().startswith("@prefix")), None)
    first_comment = next((i for i, l in enumerate(lines)
                          if l.strip().startswith("#") and
                          all(ll.strip() == "" or ll.strip().startswith("#")
                              for ll in lines[:i])), None)
    if first_prefix is not None:
        start = first_prefix
        if first_comment is not None and first_comment < first_prefix:
            block = "\n".join(lines[first_comment:first_prefix])
            if any(kw in block for kw in ["REASONING", "VALIDATION", "Issues", "Assumptions"]):
                start = first_comment
        lines = lines[start:]
    text = "\n".join(lines)

    # 3. Strip trailing prose — only stop on clearly non-Turtle lines:
    #    numbered+bold lists ("1. **Something**") or bold sentences ("**Word...")
    #    Do NOT stop on # comments or ### section headers — those are valid Turtle.
    out_lines = []
    triples_seen = False
    for line in text.split("\n"):
        s = line.strip()
        # A triple has been written once we see a non-prefix, non-comment, non-blank line
        if s and not s.startswith("#") and not s.startswith("@prefix") and not s.startswith("@base"):
            triples_seen = True
        # Stop only if we've seen triples AND hit clear prose markers
        if triples_seen and re.match(r'^\d+\.\s+\*\*|^\*\*\w', s):
            break
        out_lines.append(line)
    while out_lines and out_lines[-1].strip() == "":
        out_lines.pop()
    text = "\n".join(out_lines)

    # 4. Fix dangling `;` at end of file or before blank+comment block
    text = re.sub(r";\s*\n(\s*\n+)(\s*#)", r" .\n\1\2", text)
    text = re.sub(r";\s*$", " .", text.rstrip())

    # 5. Fix non-indented `;` before a non-indented full triple (:subj :pred)
    def fix_semi_before_full_triple(t):
        result = []
        t_lines = t.split("\n")
        for i, line in enumerate(t_lines):
            s = line.rstrip()
            if s.endswith(";") and not s.startswith(" ") and not s.startswith("\t"):
                j = i + 1
                while j < len(t_lines) and (t_lines[j].strip() == "" or t_lines[j].strip().startswith("#")):
                    j += 1
                if j < len(t_lines):
                    nxt = t_lines[j]
                    if not nxt.startswith(" ") and re.match(r'^:[A-Za-z_][\w]*\s+:[A-Za-z_]', nxt.strip()):
                        s = s[:-1] + "."
            result.append(s)
        return "\n".join(result)

    text = fix_semi_before_full_triple(text)

    # 6. Inject missing prefix declarations
    declared = set(re.findall(r'@prefix\s+(\S+?):', text))
    injections = []
    for pfx, decl in EXTRA_PREFIXES.items():
        key = pfx.rstrip(":")
        if key not in declared and re.search(r'\b' + re.escape(pfx), text):
            injections.append(decl)
    if injections:
        t_lines = text.split("\n")
        last_pfx = max((i for i, l in enumerate(t_lines) if l.strip().startswith("@prefix")), default=-1)
        if last_pfx >= 0:
            t_lines = t_lines[:last_pfx+1] + injections + t_lines[last_pfx+1:]
        else:
            t_lines = injections + [""] + t_lines
        text = "\n".join(t_lines)

    return text.strip()


def call_openai(prompt: str, model: str) -> tuple[str, float]:
    from openai import OpenAI
    client = OpenAI()
    t0 = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in ontology population."},
            {"role": "user",   "content": prompt},
        ],
    )
    elapsed = time.perf_counter() - t0
    return response.choices[0].message.content, elapsed


def call_gemini(prompt: str, model: str) -> tuple[str, float]:
    api_key = os.environ["GEMINI_API_KEY"]
    t0 = time.perf_counter()
    try:
        import google.genai as genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            temperature=0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )
        response = client.models.generate_content(model=model, contents=prompt, config=config)
        text = response.text
    except (ImportError, AttributeError):
        import google.generativeai as genai_old  # type: ignore
        genai_old.configure(api_key=api_key)
        old_model = model.replace("gemini-2.0-flash", "gemini-1.5-flash")
        client = genai_old.GenerativeModel(old_model)
        response = client.generate_content(prompt)
        text = response.text

    elapsed = time.perf_counter() - t0
    return text, elapsed


def call_anthropic(prompt: str, model: str) -> tuple[str, float]:
    import anthropic
    client = anthropic.Anthropic()
    t0 = time.perf_counter()
    with client.messages.stream(
        model=model,
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}],
        system="You are an expert in ontology population.",
    ) as stream:
        message = stream.get_final_message()
    elapsed = time.perf_counter() - t0
    return message.content[0].text, elapsed


def generate_kg(
    source_dir: Path,
    prompt_id: str,
    model_key: str,
    ontology_text: str,
    prompt_template: str,
    output_file: Path,
    dry_run: bool = False,
) -> dict:
    """Run one KG generation job. Returns a result dict."""
    result = {
        "source": str(source_dir),
        "prompt": prompt_id,
        "model":  model_key,
        "output": str(output_file),
        "status": "pending",
        "elapsed": 0.0,
        "error": None,
    }

    if output_file.exists():
        result["status"] = "skipped"
        return result

    if dry_run:
        print(f"  [DRY RUN] Would generate: {output_file}")
        result["status"] = "dry_run"
        return result

    source_code = read_source_files(source_dir)
    prompt = build_prompt(prompt_template, ontology_text, source_code)

    cfg = MODEL_CONFIGS[model_key]

    try:
        if cfg["provider"] == "openai":
            text, elapsed = call_openai(prompt, cfg["model"])
        elif cfg["provider"] == "google":
            text, elapsed = call_gemini(prompt, cfg["model"])
        elif cfg["provider"] == "anthropic":
            text, elapsed = call_anthropic(prompt, cfg["model"])
        else:
            raise ValueError(f"Unknown provider: {cfg['provider']}")
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        print(f"  ERROR: {e}")
        return result

    text = clean_turtle(text)

    header = (
        f"# Execution time: {elapsed:.2f} seconds\n"
        f"# Model used: {cfg['model']}\n"
        f"# Prompt: {prompt_id}\n\n"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(header + text, encoding="utf-8")

    result["status"] = "done"
    result["elapsed"] = elapsed
    print(f"  OK ({elapsed:.1f}s) → {output_file.name}")
    return result


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="KG generation experiment runner")
    parser.add_argument("--framework",    default="all")
    parser.add_argument("--prompt",       default="all")
    parser.add_argument("--model",        default="all")
    parser.add_argument("--source-dir",   default=None)
    parser.add_argument("--dry-run",      action="store_true")
    parser.add_argument("--output-root",  default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--ontology",     default=str(DEFAULT_ONTOLOGY))
    parser.add_argument("--skip-existing", default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument("--max-examples", type=int, default=None,
                        help="Maximum number of source examples to process per framework")
    args = parser.parse_args()

    output_root = Path(args.output_root)
    ontology_text = load_text(Path(args.ontology))

    # Resolve prompt list
    prompts = list(PROMPT_FILES.keys()) if args.prompt == "all" else [args.prompt.upper()]
    for p in prompts:
        if p not in PROMPT_FILES:
            print(f"Unknown prompt: {p}. Choose from {list(PROMPT_FILES.keys())}")
            sys.exit(1)

    # Resolve model list
    models = list(MODEL_CONFIGS.keys()) if args.model == "all" else [args.model.lower()]
    for m in models:
        if m not in MODEL_CONFIGS:
            print(f"Unknown model: {m}. Choose from {list(MODEL_CONFIGS.keys())}")
            sys.exit(1)

    # Resolve frameworks
    if args.framework == "all":
        frameworks = list(FRAMEWORK_SOURCES.keys())
    else:
        frameworks = [args.framework]

    # Check API keys
    if not args.dry_run:
        for m in models:
            env_key = MODEL_CONFIGS[m]["env_key"]
            if not os.environ.get(env_key):
                print(f"WARNING: {env_key} not set. {m} calls will fail.")

    # Build job list
    jobs = []
    for framework in frameworks:
        fw_dir = FRAMEWORK_SOURCES.get(framework)
        if fw_dir is None:
            print(f"Unknown framework: {framework}")
            continue

        # Each sub-directory (or TTL file's parent) is one example
        if args.source_dir:
            source_dirs = [Path(args.source_dir)]
        else:
            # If source has sub-projects (like CrewAI), enumerate them
            excluded = FRAMEWORK_EXCLUDED_EXAMPLE_DIRS.get(framework, set())
            subdirs = [d for d in sorted(fw_dir.iterdir()) if d.is_dir() and d.name not in excluded]
            loose_files = sorted(
                p for p in fw_dir.iterdir()
                if p.is_file() and p.suffix.lower() in SOURCE_EXTENSIONS
            )
            if subdirs:
                # Mixed layout: include sub-project dirs AND any loose source files at the top level
                source_dirs = subdirs + loose_files
            else:
                # Flat layout: each notebook/file is its own example (e.g. AutoGen .ipynb)
                source_dirs = loose_files

        if args.max_examples is not None:
            source_dirs = source_dirs[:args.max_examples]

        for source_dir in source_dirs:
            example_name = source_dir.stem if source_dir.is_file() else source_dir.name
            for prompt_id in prompts:
                for model_key in models:
                    out_file = output_root / framework / prompt_id / model_key / f"{example_name}_instances.ttl"
                    jobs.append((source_dir, prompt_id, model_key, out_file))

    print(f"\nTotal jobs: {len(jobs)}")
    print(f"Frameworks: {frameworks}")
    print(f"Prompts:    {prompts}")
    print(f"Models:     {models}")
    print(f"Output:     {output_root}\n")

    results = []
    for i, (source_dir, prompt_id, model_key, out_file) in enumerate(jobs, 1):
        print(f"[{i}/{len(jobs)}] {source_dir.name} | {prompt_id} | {model_key}")

        if args.skip_existing and out_file.exists():
            print("  Skipped (exists)")
            results.append({"source": str(source_dir), "prompt": prompt_id,
                             "model": model_key, "output": str(out_file),
                             "status": "skipped", "elapsed": 0, "error": None})
            continue

        prompt_template = load_text(PROMPT_FILES[prompt_id])
        r = generate_kg(source_dir, prompt_id, model_key, ontology_text,
                        prompt_template, out_file, dry_run=args.dry_run)
        results.append(r)

    # Save run log
    if not args.dry_run:
        log_path = output_root / "run_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nRun log saved to {log_path}")

    done  = sum(1 for r in results if r["status"] == "done")
    skip  = sum(1 for r in results if r["status"] == "skipped")
    err   = sum(1 for r in results if r["status"] == "error")
    print(f"\nSummary: {done} done, {skip} skipped, {err} errors")


if __name__ == "__main__":
    main()
