from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


COURSE_KEYWORDS = {
    "asset-pricing": [
        "资产定价",
        "asset pricing",
        "ap",
        "bond",
        "bonds",
        "债券",
        "利率债",
        "收益率",
        "yield",
        "capm",
        "sdf",
        "随机贴现因子",
        "无套利",
        "套利",
        "euler",
        "factor model",
        "因子",
    ],
    "econometrics": [
        "计量",
        "econometrics",
        "ols",
        "iv",
        "2sls",
        "rdd",
        "did",
        "面板",
        "panel",
        "fixed effect",
        "回归",
        "内生",
        "工具变量",
        "异方差",
        "时间序列",
    ],
    "intermediate-microeconomics": [
        "中级微观",
        "中微",
        "微观",
        "microeconomics",
        "consumer",
        "producer",
        "utility",
        "效用",
        "无差异曲线",
        "预算约束",
        "一般均衡",
        "edgeworth",
        "福利",
        "成本最小化",
    ],
    "international-economics": [
        "国际经济学",
        "国际",
        "international economics",
        "trade",
        "贸易",
        "汇率",
        "exchange rate",
        "ricardian",
        "heckscher",
        "ohlin",
        "specific factors",
        "terms of trade",
        "开放经济",
        "国际收支",
    ],
}


TRANSCRIPT_KEYWORDS = [
    "转写",
    "文本",
    "transcript",
    "audio",
    "录音",
    "听见",
    "speech",
    "asr",
]

HANDWRITTEN_KEYWORDS = [
    "goodnotes",
    "goodnote",
    "笔记",
    "手写",
    "note",
    "notes",
    "手稿",
]

TEXTBOOK_KEYWORDS = [
    "课本",
    "教材",
    "chapter",
    "textbook",
    "reading",
    "讲义",
    "课件",
    "slides",
    "slide",
    "ppt",
]

TRANSCRIPT_EXTS = {".txt", ".md", ".srt", ".vtt"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
PDF_EXTS = {".pdf"}
ZIP_EXTS = {".zip"}


@dataclass
class IntakeResult:
    source: str
    status: str
    course: str | None
    material_type: str | None
    destination: str | None
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move files from inbox/dropbox into course-specific incoming folders."
    )
    default_root = Path(__file__).resolve().parents[3]
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=default_root,
        help="Repository root. Defaults to the parent repository of this skill.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the routing plan without moving files.",
    )
    parser.add_argument(
        "--keep-originals",
        action="store_true",
        help="Copy files instead of moving them out of inbox/dropbox.",
    )
    return parser.parse_args()


def normalize_text(text: str) -> str:
    lowered = text.lower()
    lowered = lowered.replace("_", " ")
    lowered = lowered.replace("-", " ")
    return lowered


def score_keywords(text: str, keywords: list[str]) -> int:
    haystack = normalize_text(text)
    score = 0
    for keyword in keywords:
        if keyword.lower() in haystack:
            score += 1
    return score


def read_text_preview(path: Path, limit: int = 4000) -> str:
    if path.suffix.lower() not in TRANSCRIPT_EXTS:
        return ""
    try:
        return path.read_text(encoding="utf-8")[:limit]
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")[:limit]
        except UnicodeDecodeError:
            return ""


def read_zip_preview(path: Path, limit: int = 4000) -> str:
    if path.suffix.lower() not in ZIP_EXTS:
        return ""
    try:
        with zipfile.ZipFile(path) as archive:
            parts: list[str] = []
            for name in archive.namelist()[:5]:
                parts.append(name)
                if name.lower().endswith(".txt"):
                    try:
                        text = archive.read(name).decode("utf-8-sig")
                        parts.append(text[:limit])
                    except UnicodeDecodeError:
                        continue
            return "\n".join(parts)
    except zipfile.BadZipFile:
        return ""


def classify_course(path: Path) -> tuple[str | None, str]:
    filename_text = str(path)
    preview = read_text_preview(path) or read_zip_preview(path)
    combined = f"{filename_text}\n{preview}"

    best_course = None
    best_score = 0
    for course, keywords in COURSE_KEYWORDS.items():
        score = score_keywords(combined, keywords)
        if score > best_score:
            best_course = course
            best_score = score

    if best_score == 0:
        return None, "No clear course keyword found."
    return best_course, f"Matched course keywords with score {best_score}."


def zip_namelist(path: Path) -> list[str]:
    if path.suffix.lower() not in ZIP_EXTS:
        return []
    try:
        with zipfile.ZipFile(path) as archive:
            return archive.namelist()
    except zipfile.BadZipFile:
        return []


def classify_material_type(path: Path) -> tuple[str | None, str]:
    suffix = path.suffix.lower()
    text = str(path)
    preview = read_text_preview(path) or read_zip_preview(path)
    combined = f"{text}\n{preview}"

    if score_keywords(combined, HANDWRITTEN_KEYWORDS) > 0 and suffix in PDF_EXTS.union(IMAGE_EXTS, ZIP_EXTS):
        return "handwritten", "Filename suggests handwritten or GoodNotes material."

    if score_keywords(combined, TRANSCRIPT_KEYWORDS) > 0 and suffix in TRANSCRIPT_EXTS.union(ZIP_EXTS):
        return "transcripts", "Filename suggests transcript or audio text export."

    if score_keywords(combined, TEXTBOOK_KEYWORDS) > 0 and suffix in PDF_EXTS.union(IMAGE_EXTS, ZIP_EXTS):
        return "textbook", "Filename suggests textbook, slides, or handout material."

    if suffix in TRANSCRIPT_EXTS:
        return "transcripts", "Text-like file extension routed as transcript."

    if suffix in IMAGE_EXTS:
        return "handwritten", "Image file routed as handwritten note by default."

    if suffix in PDF_EXTS:
        return "textbook", "PDF routed as textbook/handout by default."

    if suffix in ZIP_EXTS:
        names = "\n".join(zip_namelist(path))
        if score_keywords(names, TRANSCRIPT_KEYWORDS) > 0 or ".txt" in names.lower():
            return "transcripts", "Zip appears to contain transcript text."
        if score_keywords(names, HANDWRITTEN_KEYWORDS) > 0 or re.search(r"\.(png|jpg|jpeg|pdf)\b", names.lower()):
            return "handwritten", "Zip appears to contain note images or exported note files."
        return None, "Zip content type is ambiguous."

    return None, "Unsupported file extension."


def ensure_unique_path(target_dir: Path, filename: str) -> Path:
    candidate = target_dir / filename
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    counter = 2
    while True:
        alt = target_dir / f"{stem}-{counter}{suffix}"
        if not alt.exists():
            return alt
        counter += 1


def move_or_copy(source: Path, destination: Path, keep_originals: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if keep_originals:
        shutil.copy2(source, destination)
    else:
        shutil.move(str(source), str(destination))


def collect_files(dropbox: Path) -> list[Path]:
    files = []
    for path in dropbox.rglob("*"):
        if path.is_file() and path.name != ".gitkeep":
            files.append(path)
    return sorted(files)


def write_manifest(processed_dir: Path, results: list[IntakeResult]) -> Path:
    processed_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    manifest_path = processed_dir / f"intake-{timestamp}.json"
    payload = [result.__dict__ for result in results]
    manifest_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    dropbox = repo_root / "inbox" / "dropbox"
    review_dir = repo_root / "inbox" / "review"
    processed_dir = repo_root / "inbox" / "processed"

    dropbox.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    files = collect_files(dropbox)
    if not files:
        print("No files found in inbox/dropbox.")
        return

    results: list[IntakeResult] = []
    for path in files:
        course, course_reason = classify_course(path)
        material_type, type_reason = classify_material_type(path)

        if course and material_type:
            target_dir = repo_root / "courses" / course / "incoming" / material_type
            destination = ensure_unique_path(target_dir, path.name)
            status = "planned" if args.dry_run else "routed"
            reason = f"{course_reason} {type_reason}"
            if not args.dry_run:
                move_or_copy(path, destination, keep_originals=args.keep_originals)
            results.append(
                IntakeResult(
                    source=str(path.relative_to(repo_root)).replace("\\", "/"),
                    status=status,
                    course=course,
                    material_type=material_type,
                    destination=str(destination.relative_to(repo_root)).replace("\\", "/"),
                    reason=reason,
                )
            )
        else:
            destination = ensure_unique_path(review_dir, path.name)
            status = "needs_review" if args.dry_run else "review"
            reason = f"{course_reason} {type_reason}"
            if not args.dry_run:
                move_or_copy(path, destination, keep_originals=args.keep_originals)
            results.append(
                IntakeResult(
                    source=str(path.relative_to(repo_root)).replace("\\", "/"),
                    status=status,
                    course=course,
                    material_type=material_type,
                    destination=str(destination.relative_to(repo_root)).replace("\\", "/"),
                    reason=reason,
                )
            )

    manifest_path = write_manifest(processed_dir, results)
    for result in results:
        print(json.dumps(result.__dict__, ensure_ascii=False))
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
