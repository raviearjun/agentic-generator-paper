from pathlib import Path
import json

from src.core.extractor import extract_project
from src.autogen.adapter import adapt
from src.autogen.generator import generate_project


KG_DIR = Path("kgs_original/AutoGen")
OUTPUT_ROOT = Path("output_files/autogen")


def process_kg(ttl_file: Path):

    print("\n" + "=" * 80)
    print(f"Processing: {ttl_file.name}")
    print("=" * 80)

    try:
        project = adapt(extract_project(str(ttl_file)))

        output_dir = OUTPUT_ROOT / ttl_file.stem

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # Save IR dump
        with open(
            output_dir / "project.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                project.model_dump(),
                f,
                indent=2,
                default=str
            )

        generate_project(
            project,
            str(output_dir)
        )

        print(
            f"✓ SUCCESS: {ttl_file.name}"
        )

        print(
            f"  Agents: {len(project.agents)}"
        )

        print(
            f"  Tasks: {len(project.tasks)}"
        )

        print(
            f"  Tools: {len(project.tools)}"
        )

        return True

    except Exception as e:
        print(
            f"✗ FAILED: {ttl_file.name}"
        )

        print(e)

        return False


def main():

    ttl_files = sorted(
        KG_DIR.glob("*.ttl")
    )

    print(
        f"\nFound {len(ttl_files)} KG files"
    )

    success = 0
    failed = 0

    for ttl_file in ttl_files:

        if process_kg(ttl_file):
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"Successful: {success}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
