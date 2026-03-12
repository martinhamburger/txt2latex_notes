from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.strip().lower())
    slug = slug.strip("-")
    return slug or "lecture"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a lecture workspace and starter LaTeX file."
    )
    default_root = Path(__file__).resolve().parents[3]
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=default_root,
        help="Repository root. Defaults to the parent repository of this skill.",
    )
    parser.add_argument(
        "--course",
        required=True,
        help="Course key, for example 'econometrics'.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Lecture title shown in the starter LaTeX file.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Lecture date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--lecture-slug",
        help="Optional explicit lecture folder slug.",
    )
    parser.add_argument(
        "--transcript",
        type=Path,
        help="Optional path to a raw transcript to copy into the new lecture folder.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the starter main.tex if it already exists.",
    )
    return parser.parse_args()


def load_course_config(repo_root: Path, course_key: str) -> dict:
    config_path = repo_root / "courses" / course_key / "course.json"
    if not config_path.exists():
        raise FileNotFoundError(
            f"Course config not found: {config_path}. Run bootstrap_notes_repo.py first."
        )
    return json.loads(config_path.read_text(encoding="utf-8"))


def build_summary_items(course_config: dict) -> str:
    items = []
    for entry in course_config.get("recommended_sections", []):
        items.append(f"  \\item 待补充：{entry}")
    if not items:
        items.append("  \\item 待根据课程材料整理本讲要点。")
    return "\n".join(items)


def render_template(template_path: Path, course_config: dict, lecture_title: str, lecture_date: str) -> str:
    template = template_path.read_text(encoding="utf-8")
    replacements = {
        "{{COURSE_TITLE_ZH}}": course_config["title_zh"],
        "{{LECTURE_TITLE}}": lecture_title,
        "{{LECTURE_DATE}}": lecture_date,
        "{{SUMMARY_ITEMS}}": build_summary_items(course_config),
    }

    output = template
    for key, value in replacements.items():
        output = output.replace(key, value)
    return output


def touch_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / ".gitkeep").touch(exist_ok=True)


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    course_key = args.course
    course_config = load_course_config(repo_root, course_key)

    lecture_slug = args.lecture_slug or f"{args.date}-{slugify(args.title)}"
    lecture_dir = repo_root / "courses" / course_key / "lectures" / lecture_slug
    lecture_dir.mkdir(parents=True, exist_ok=True)

    sources_dir = lecture_dir / "sources"
    handwritten_dir = sources_dir / "handwritten"
    textbook_dir = sources_dir / "textbook"
    drafts_dir = lecture_dir / "drafts"

    for path in (handwritten_dir, textbook_dir, drafts_dir):
        touch_gitkeep(path)

    main_tex_path = lecture_dir / "main.tex"
    if args.overwrite or not main_tex_path.exists():
        template_path = Path(__file__).resolve().parents[1] / "assets" / "templates" / "lecture-note.tex"
        rendered = render_template(
            template_path,
            course_config=course_config,
            lecture_title=args.title,
            lecture_date=args.date,
        )
        main_tex_path.write_text(rendered, encoding="utf-8")

    transcript_path = sources_dir / "transcript.txt"
    if args.transcript:
        shutil.copyfile(args.transcript.resolve(), transcript_path)
    else:
        transcript_path.parent.mkdir(parents=True, exist_ok=True)
        transcript_path.touch(exist_ok=True)

    manifest = {
        "course_key": course_key,
        "lecture_title": args.title,
        "lecture_date": args.date,
        "transcript": str(transcript_path.relative_to(repo_root)).replace("\\", "/"),
        "handwritten_dir": str(handwritten_dir.relative_to(repo_root)).replace("\\", "/"),
        "textbook_dir": str(textbook_dir.relative_to(repo_root)).replace("\\", "/"),
        "main_tex": str(main_tex_path.relative_to(repo_root)).replace("\\", "/"),
    }
    (lecture_dir / "lecture.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(lecture_dir)


if __name__ == "__main__":
    main()
