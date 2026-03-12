from __future__ import annotations

import argparse
import re
from pathlib import Path


TIMESTAMP_PATTERNS = [
    re.compile(r"^\s*\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*"),
    re.compile(r"^\s*\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s*"),
]

SPEAKER_PATTERN = re.compile(
    r"^\s*(speaker\s*\d+|spk\s*\d+|说话人\s*\d+|讲话人\s*\d+)\s*[:：]\s*",
    re.IGNORECASE,
)

MULTI_BLANKS = re.compile(r"\n{3,}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize a raw lecture transcript without changing its meaning."
    )
    parser.add_argument("input_path", type=Path, help="Path to the raw transcript.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output path. Defaults to '<input stem>_clean.txt' next to the input.",
    )
    parser.add_argument(
        "--keep-speakers",
        action="store_true",
        help="Do not remove generic speaker labels such as 'Speaker 1:'.",
    )
    parser.add_argument(
        "--keep-timestamps",
        action="store_true",
        help="Do not remove leading timestamps.",
    )
    return parser.parse_args()


def strip_prefixes(line: str, keep_speakers: bool, keep_timestamps: bool) -> str:
    cleaned = line

    if not keep_timestamps:
        for pattern in TIMESTAMP_PATTERNS:
            cleaned = pattern.sub("", cleaned)

    if not keep_speakers:
        cleaned = SPEAKER_PATTERN.sub("", cleaned)

    return cleaned.rstrip()


def clean_text(text: str, keep_speakers: bool, keep_timestamps: bool) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").replace("\ufeff", "")
    lines = [
        strip_prefixes(line, keep_speakers=keep_speakers, keep_timestamps=keep_timestamps)
        for line in normalized.split("\n")
    ]

    compact_lines = []
    for line in lines:
        compact = re.sub(r"[ \t]+", " ", line).strip()
        compact_lines.append(compact)

    result = "\n".join(compact_lines).strip()
    result = MULTI_BLANKS.sub("\n\n", result)
    return result + "\n"


def main() -> None:
    args = parse_args()
    input_path = args.input_path.resolve()
    output_path = args.output
    if output_path is None:
        output_path = input_path.with_name(f"{input_path.stem}_clean.txt")
    else:
        output_path = output_path.resolve()

    cleaned = clean_text(
        input_path.read_text(encoding="utf-8"),
        keep_speakers=args.keep_speakers,
        keep_timestamps=args.keep_timestamps,
    )
    output_path.write_text(cleaned, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
