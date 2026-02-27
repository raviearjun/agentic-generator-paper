"""
One-time migration script: Add agento-ext:KickoffInputBundle triples to all CrewAI TTL files.

This appends a uniform, SPARQL-friendly input representation to each KG file,
replacing the 7+ ad-hoc patterns for encoding runtime inputs.

Run once from project root:
    python scripts/add_kickoff_inputs.py
"""

import os

TTL_DIR = os.path.join(os.path.dirname(__file__), "..", "generated_kg", "CrewAI")

# Namespace prefix block to inject (only if not already present)
EXT_PREFIX = '@prefix agento-ext: <http://www.w3id.org/agentic-ai/ext#> .'

# Per-crew KickoffInputBundle definitions
# key = TTL filename stem, value = list of (inputKey, inputValue, isDefault)
# isDefault=False means Pattern H: no concrete value available (runtime-only)
CREW_INPUTS = {
    "game-builder-crew_instances": [
        ("game", "A Snake game where the player controls a snake that moves continuously, and the player can change its direction using input keys. The snake grows longer each time it eats food, which appears randomly on the screen. The game ends if the snake collides with itself or the walls. The player's score increases with each food item eaten. The game should include a simple scoring system, a start screen, and a game-over screen displaying the final score.", True),
    ],
    "industry-agents_instances": [
        ("weaviate_feature", "MUVERA", True),
    ],
    "instagram_post_instances": [
        ("product_website", "", False),
        ("product_details", "", False),
    ],
    "job-posting_instances": [
        ("company_domain", "careers.wbd.com", True),
        ("company_description", "Warner Bros. Discovery is a premier global media and entertainment company, offering audiences the world's most differentiated and complete portfolio of content, brands and franchises across television, film, sports, news, streaming and gaming. We're home to the world's best storytellers, creating world-class products for consumers", True),
        ("hiring_needs", "Production Assistant, for a TV production set in Los Angeles in June 2025", True),
        ("specific_benefits", "Weekly Pay, Employee Meals, healthcare", True),
    ],
    "landing_page_generator_instances": [
        ("idea", "", False),
    ],
    "markdown_validator_instances": [
        ("filename", "", False),
    ],
    "marketing_strategy_instances": [
        ("customer_domain", "crewai.com", True),
        ("project_description", "CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.", True),
    ],
    "match_profile_to_positions_instances": [
        ("path_to_cv", "./src/match_to_proposal/data/cv.md", True),
        ("path_to_jobs_csv", "./src/match_to_proposal/data/jobs.csv", True),
    ],
    "meta_quest_knowledge_instances": [
        ("question", "How often should I take breaks?", True),
    ],
    "prep-for-a-meeting_instances": [
        ("participants", "", False),
        ("context", "", False),
        ("objective", "", False),
    ],
    "recruitment_instances": [
        ("job_requirements", "Ruby on Rails and React Engineer - We are seeking a skilled Ruby on Rails and React engineer to join our team. The ideal candidate will have experience in both backend and frontend development, with a passion for building high-quality web applications.", True),
    ],
    "screenplay_writer_instances": [
        # No runtime input variables - discussion text is embedded in the KG
    ],
    "starter_template_instances": [
        ("var1", "", False),
        ("var2", "", False),
    ],
    "stock_analysis_instances": [
        ("company_stock", "AMZN", True),
    ],
    "surprise_trip_instances": [
        ("origin", "São Paulo, GRU", True),
        ("destination", "New York, JFK", True),
        ("age", "31", True),
        ("hotel_location", "Brooklyn", True),
        ("flight_information", "GOL 1234, leaving at June 30th, 2024, 10:00", True),
        ("trip_duration", "14 days", True),
    ],
    "trip_planner_instances": [
        ("origin", "", False),
        ("cities", "", False),
        ("range", "", False),
        ("interests", "", False),
    ],
}


def _escape_ttl(value: str) -> str:
    """Escape a string for Turtle literal (double-quoted)."""
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def build_bundle_block(crew_stem: str, inputs: list) -> str:
    """Build the TTL block for KickoffInputBundle triples."""
    if not inputs:
        return ""

    lines = [
        "",
        "################################################################################",
        "# KickoffInputBundle (agento-ext) — Uniform runtime inputs for pipeline extraction",
        "################################################################################",
        "",
    ]

    for i, (key, value, is_default) in enumerate(inputs, 1):
        node_name = f":KickoffInput_{key}"
        escaped_val = _escape_ttl(value)

        lines.append(f'{node_name} a agento-ext:KickoffInputBundle ;')
        lines.append(f'    agento-ext:inputKey "{key}" ;')
        if is_default and value:
            lines.append(f'    agento-ext:inputValue "{escaped_val}" ;')
        else:
            lines.append(f'    agento-ext:inputValue "" ;')
        lines.append(f'    agento-ext:isDefaultValue {"true" if (is_default and value) else "false"} .')
        lines.append("")

    return "\n".join(lines)


def process_file(filepath: str, crew_stem: str, inputs: list) -> None:
    """Add agento-ext prefix and KickoffInputBundle triples to a TTL file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already modified
    if "agento-ext:" in content:
        print(f"  [SKIP] {crew_stem} — already has agento-ext triples")
        return

    # 1. Inject prefix after other @prefix lines
    prefix_lines = []
    other_lines = []
    in_prefix_block = True
    for line in content.split("\n"):
        if in_prefix_block and (line.startswith("@prefix") or line.startswith("@base")):
            prefix_lines.append(line)
        elif in_prefix_block and line.strip() == "" and prefix_lines:
            # Could be a blank between prefix and content
            prefix_lines.append(line)
        else:
            if in_prefix_block and prefix_lines:
                in_prefix_block = False
            other_lines.append(line)

    # Add our prefix after existing ones
    prefix_lines.insert(-1, EXT_PREFIX)  # Before the trailing blank line

    # 2. Build the bundle block
    bundle_block = build_bundle_block(crew_stem, inputs)

    # 3. Reassemble: prefixes + original content + bundle at end
    new_content = "\n".join(prefix_lines) + "\n" + "\n".join(other_lines)

    # Strip trailing whitespace and add bundle before final end
    new_content = new_content.rstrip() + "\n" + bundle_block

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    n_inputs = len(inputs)
    has_defaults = sum(1 for _, v, d in inputs if d and v)
    print(f"  [OK] {crew_stem} — {n_inputs} inputs ({has_defaults} with defaults)")


def main():
    print("Adding agento-ext:KickoffInputBundle to CrewAI TTL files...\n")

    for crew_stem, inputs in CREW_INPUTS.items():
        filepath = os.path.join(TTL_DIR, f"{crew_stem}.ttl")
        if not os.path.exists(filepath):
            print(f"  [WARN] {crew_stem}.ttl not found, skipping")
            continue
        process_file(filepath, crew_stem, inputs)

    print("\nDone! All TTL files updated.")


if __name__ == "__main__":
    main()
