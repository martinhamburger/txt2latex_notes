from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LectureEntry:
    lecture_dir: Path
    lecture_slug: str
    lecture_date: str
    lecture_title: str
    main_tex: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge lecture notes into one per-course cumulative note file."
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
        help="Optional course key. If omitted, all courses are processed.",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile merged TeX into course output PDF using xelatex.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def extract_preamble(tex_text: str) -> str:
    marker = "\\begin{document}"
    idx = tex_text.find(marker)
    if idx == -1:
        raise ValueError("Invalid TeX: missing \\begin{document}")
    preamble = tex_text[:idx]
    # Remove per-lecture metadata so the cumulative file can set its own title block.
    preamble = re.sub(r"^\\title\{.*?\}\s*$", "", preamble, flags=re.MULTILINE)
    preamble = re.sub(r"^\\author\{.*?\}\s*$", "", preamble, flags=re.MULTILINE)
    preamble = re.sub(r"^\\date\{.*?\}\s*$", "", preamble, flags=re.MULTILINE)
    return preamble


def extract_body(tex_text: str) -> str:
    begin_doc = tex_text.find("\\begin{document}")
    end_doc = tex_text.rfind("\\end{document}")
    if begin_doc == -1 or end_doc == -1 or end_doc <= begin_doc:
        raise ValueError("Invalid TeX document structure")

    body = tex_text[begin_doc + len("\\begin{document}"):end_doc]
    body = re.sub(r"\\maketitle\s*", "", body, flags=re.MULTILINE)
    return body.strip() + "\n"


def collect_lectures(course_dir: Path) -> list[LectureEntry]:
    lectures_root = course_dir / "lectures"
    if not lectures_root.exists():
        return []

    entries: list[LectureEntry] = []
    for lecture_dir in sorted(lectures_root.glob("*")):
        if not lecture_dir.is_dir():
            continue

        main_tex = lecture_dir / "main.tex"
        if not main_tex.exists():
            continue

        meta = load_json(lecture_dir / "lecture.json")
        if meta and meta.get("is_primary_output") is False:
            continue

        lecture_slug = lecture_dir.name
        lecture_date = str(meta.get("lecture_date", lecture_slug[:10]))
        lecture_title = str(meta.get("lecture_title", lecture_slug))

        entries.append(
            LectureEntry(
                lecture_dir=lecture_dir,
                lecture_slug=lecture_slug,
                lecture_date=lecture_date,
                lecture_title=lecture_title,
                main_tex=main_tex,
            )
        )

    entries.sort(key=lambda e: (e.lecture_date, e.lecture_slug))
    return entries


def build_course_notes(course_dir: Path, compile_pdf: bool) -> dict | None:
    course_key = course_dir.name
    course_meta = load_json(course_dir / "course.json")
    course_title = str(course_meta.get("title_zh", course_key))

    lectures = collect_lectures(course_dir)
    if not lectures:
        return None

    first_tex_text = lectures[0].main_tex.read_text(encoding="utf-8")
    preamble = extract_preamble(first_tex_text)

    sections: list[str] = []
    for entry in lectures:
        tex_text = entry.main_tex.read_text(encoding="utf-8")
        body = extract_body(tex_text)
        header = (
            f"\\section{{讲次：{entry.lecture_date} {entry.lecture_title}}}\n"
            f"\\textit{{来源讲次：{entry.lecture_slug}。若原始资料包含多个时间片段，已在正文中合并。}}\n\n"
        )
        sections.append(header + body)

    merged = (
        preamble
        + "\\title{ " + course_title + " \\\\ \\large 课程总笔记 }\n"
        + "\\author{}\n"
        + "\\date{}\n\n"
        + "\\begin{document}\n\n"
        + "\\maketitle\n\n"
        + "\\tableofcontents\n\n"
        + "\\newpage\n\n"
        + "\n\\newpage\n\n".join(sections)
        + "\n\\end{document}\n"
    )

    output_tex_dir = course_dir / "output" / "tex"
    output_pdf_dir = course_dir / "output" / "pdf"
    output_tex_dir.mkdir(parents=True, exist_ok=True)
    output_pdf_dir.mkdir(parents=True, exist_ok=True)

    out_tex = output_tex_dir / f"{course_key}-notes.tex"
    out_pdf = output_pdf_dir / f"{course_key}-notes.pdf"
    out_tex.write_text(merged, encoding="utf-8")

    if compile_pdf:
        subprocess.run(
            [
                "xelatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                out_tex.name,
            ],
            cwd=output_tex_dir,
            check=True,
            capture_output=True,
            text=True,
        )

        generated_pdf = output_tex_dir / f"{course_key}-notes.pdf"
        if generated_pdf.exists():
            out_pdf.write_bytes(generated_pdf.read_bytes())

    return {
        "course_key": course_key,
        "lectures_merged": len(lectures),
        "output_tex": str(out_tex).replace("\\", "/"),
        "output_pdf": str(out_pdf).replace("\\", "/"),
    }


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    courses_root = repo_root / "courses"

    if args.course:
        course_dirs = [courses_root / args.course]
    else:
        course_dirs = [p for p in sorted(courses_root.glob("*")) if p.is_dir()]

    results = []
    for course_dir in course_dirs:
        if not course_dir.exists():
            continue
        result = build_course_notes(course_dir, compile_pdf=args.compile)
        if result:
            results.append(result)
            print(json.dumps(result, ensure_ascii=False))

    if not results:
        print("No course notes generated.")


if __name__ == "__main__":
    main()
