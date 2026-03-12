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


def export_name(course_key: str, lecture_slug: str) -> str:
    return f"{course_key}--{lecture_slug}.pdf"


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    outgoing_dir = repo_root / "pdf" / "outgoing"
    outgoing_dir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        for old_pdf in outgoing_dir.glob("*.pdf"):
            old_pdf.unlink()

    exported = []
    for pdf_path in repo_root.glob("courses/*/lectures/*/main.pdf"):
        course_key = pdf_path.parts[-4]
        lecture_slug = pdf_path.parts[-2]
        target_path = outgoing_dir / export_name(course_key, lecture_slug)
        shutil.copy2(pdf_path, target_path)
        exported.append(
            {
                "source": str(pdf_path.relative_to(repo_root)).replace("\\", "/"),
                "export": str(target_path.relative_to(repo_root)).replace("\\", "/"),
                "course_key": course_key,
                "lecture_slug": lecture_slug,
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
