from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy generated lecture PDFs into a shallow top-level pdf/outgoing folder."
    )
    default_root = Path(__file__).resolve().parents[3]
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=default_root,
        help="Repository root. Defaults to the parent repository of this skill.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove previously exported PDFs in pdf/outgoing before copying current ones.",
    )
    return parser.parse_args()


def export_name(course_key: str) -> str:
    return f"{course_key}.pdf"


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    outgoing_dir = repo_root / "pdf" / "outgoing"
    outgoing_dir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        for old_pdf in outgoing_dir.glob("*.pdf"):
            old_pdf.unlink()

    exported = []
    courses_root = repo_root / "courses"
    for course_dir in sorted(courses_root.glob("*")):
        if not course_dir.is_dir():
            continue

        course_key = course_dir.name
        canonical_pdf = course_dir / "output" / "pdf" / f"{course_key}-notes.pdf"
        selected_pdf = None
        source_type = None

        if canonical_pdf.exists():
            selected_pdf = canonical_pdf
            source_type = "course_notes"
        else:
            lecture_pdfs = sorted(
                course_dir.glob("lectures/*/main.pdf"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if lecture_pdfs:
                selected_pdf = lecture_pdfs[0]
                source_type = "latest_lecture_fallback"

        if selected_pdf is None:
            continue

        target_path = outgoing_dir / export_name(course_key)
        shutil.copy2(selected_pdf, target_path)
        exported.append(
            {
                "source": str(selected_pdf.relative_to(repo_root)).replace("\\", "/"),
                "export": str(target_path.relative_to(repo_root)).replace("\\", "/"),
                "course_key": course_key,
                "source_type": source_type,
            }
        )

    index_path = outgoing_dir / "index.json"
    index_path.write_text(
        json.dumps(exported, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for item in exported:
        print(json.dumps(item, ensure_ascii=False))
    print(f"Index: {index_path}")


if __name__ == "__main__":
    main()
