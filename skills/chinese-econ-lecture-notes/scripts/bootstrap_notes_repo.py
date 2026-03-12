from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_COURSES = [
    {
        "course_key": "intermediate-microeconomics",
        "title_zh": "中级微观经济学",
        "title_en": "Intermediate Microeconomics",
        "default_engine": "xelatex",
        "style": "clean-minimal",
        "recommended_sections": [
            "preferences and constraints",
            "optimization",
            "comparative statics",
            "economic intuition",
        ],
    },
    {
        "course_key": "international-economics",
        "title_zh": "国际经济学",
        "title_en": "International Economics",
        "default_engine": "xelatex",
        "style": "clean-minimal",
        "recommended_sections": [
            "model setup",
            "trade mechanism",
            "comparative statics",
            "policy or welfare implications",
        ],
    },
    {
        "course_key": "econometrics",
        "title_zh": "计量经济学",
        "title_en": "Econometrics",
        "default_engine": "xelatex",
        "style": "clean-minimal",
        "recommended_sections": [
            "model setup",
            "assumptions",
            "derivation",
            "interpretation",
        ],
    },
    {
        "course_key": "asset-pricing",
        "title_zh": "资产定价",
        "title_en": "Asset Pricing",
        "default_engine": "xelatex",
        "style": "clean-minimal",
        "recommended_sections": [
            "pricing object",
            "equilibrium relation",
            "intuition",
            "applications",
        ],
    },
]


TRACKED_DIRS = [
    "incoming/transcripts",
    "incoming/handwritten",
    "incoming/textbook",
    "lectures",
    "output/tex",
    "output/pdf",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the reusable course directory layout for Chinese econ notes."
    )
    default_root = Path(__file__).resolve().parents[3]
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=default_root,
        help="Repository root. Defaults to the parent repository of this skill.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing course.json files.",
    )
    return parser.parse_args()


def ensure_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    gitkeep.touch(exist_ok=True)


def write_course_json(course_dir: Path, course: dict, force: bool) -> None:
    config_path = course_dir / "course.json"
    if config_path.exists() and not force:
        return
    config_path.write_text(
        json.dumps(course, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    courses_root = repo_root / "courses"
    courses_root.mkdir(parents=True, exist_ok=True)

    created = []
    for course in DEFAULT_COURSES:
        course_dir = courses_root / course["course_key"]
        course_dir.mkdir(parents=True, exist_ok=True)
        write_course_json(course_dir, course, args.force)

        for relative_dir in TRACKED_DIRS:
            ensure_gitkeep(course_dir / relative_dir)

        created.append(course_dir)

    for path in created:
        print(path)


if __name__ == "__main__":
    main()
