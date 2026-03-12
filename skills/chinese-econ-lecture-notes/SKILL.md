---
name: chinese-econ-lecture-notes
description: Convert Chinese economics lecture materials into clean, concise LaTeX notes. Use when Codex needs to turn a Chinese `.txt` transcript (for example, from iFlytek), handwritten note images, textbook pages, slide screenshots, or mixed course materials into structured lecture notes for intermediate microeconomics, international economics, econometrics, asset pricing, or similar economics courses. This skill is especially useful when transcript text should be the main backbone, while images and textbook pages are used to correct notation, formulas, diagrams, and definitions.
---

# Chinese Econ Lecture Notes

## Overview

Use this skill to build lecture notes that are readable in Chinese, mathematically correct, and visually restrained. Treat the transcript as the time-ordered spine, then use images, handwritten notes, and textbook pages to repair symbols, formulas, diagrams, and exact statements.

## Quick Start

1. Identify the course and check whether a course workspace exists under `courses/`.
2. If new files have been dropped into `inbox/dropbox/` or `pdf/incoming/`, run `scripts/intake_inbox.py` first.
3. If the repository has not been scaffolded yet, run `scripts/bootstrap_notes_repo.py`.
4. If the lecture folder does not exist, run `scripts/new_lecture.py --course <course-key> --title "<lecture title>"`.
5. If the main input is a raw `.txt` transcript, optionally normalize it with `scripts/clean_transcript.py`.
6. Read `references/workflow.md` for source prioritization.
7. Read `references/latex-style.md` before writing or editing the `.tex` file.
8. Read `references/course-conventions.md` when notation or structure depends on the course.
9. Read `references/intake-guide.md` when the user asks how to hand materials over efficiently.
10. Use `assets/templates/lecture-note.tex` as the default LaTeX baseline unless the user provides another template.

## Workflow

### 1. Build the Lecture Spine from Text

- Start from the transcript, even if it is noisy.
- Remove timestamps, filler speech, repeated restarts, and obvious ASR errors only when the intended meaning is clear.
- Segment the lecture into 3 to 6 logical chunks based on topic changes, not on transcript paragraph breaks.
- Preserve Chinese terminology exactly when it is domain-specific. If useful, add the English term on first mention.

### 2. Repair the Spine with Visual Sources

- Use handwritten notes to recover notation, board structure, quick derivations, and emphasis.
- Use textbook pages to confirm formal definitions, theorem statements, and standard diagrams.
- Use slide screenshots to recover model setup, bullet structure, or equation numbering.
- If handwriting is unclear, cross-check against the transcript first, then the textbook.
- If a symbol remains ambiguous after cross-checking, leave a brief LaTeX comment such as `% TODO: verify symbol from handwriting` rather than hallucinating.

### 3. Write the Note in Clean Chinese LaTeX

- Prefer a simple `ctexart` document with restrained packages and no decorative theme.
- Use sections and subsections for logic, not for visual ornament.
- Put formulas in proper math mode; never leave symbolic expressions inline as plain text when display math is clearer.
- Summarize spoken repetition into compact prose, but keep proof logic, derivation order, and economic intuition.
- When the lecture is conceptual, write denser prose with short bullet lists.
- When the lecture is technical, separate assumptions, derivation steps, results, and intuition.

### 4. Verify Before Handing Off

- Check equation delimiters, braces, labels, and theorem environments.
- Ensure notation is consistent from start to finish.
- If a LaTeX toolchain is available, compile with `latexmk -xelatex` or `xelatex`.
- If compilation is unavailable, still deliver a compile-ready `.tex` file and mention that compilation was not run.

## Source Priority Rules

- Transcript only: produce the full note, but flag any likely notation gaps.
- Transcript + handwriting: trust the transcript for ordering and the handwriting for formulas and board emphasis.
- Transcript + textbook: trust the transcript for what the instructor emphasized; trust the textbook for exact standard statements.
- Handwriting only: produce a sparse but structured note and mark unresolved symbols explicitly.
- Textbook only: produce a study note, not a fake lecture transcript; make it clear the output is textbook-driven.

## Output Standard

Every note should aim for:

- A clear Chinese title with course and lecture metadata.
- A short opening overview of the lecture question or objective.
- Logical sections with compact prose.
- Displayed equations only when they carry real content.
- Definitions, propositions, examples, or remarks only when they improve clarity.
- Minimal visual styling and strong Chinese typesetting.

## Resources

### scripts/

- `bootstrap_notes_repo.py`: create the reusable course directory layout and course metadata files.
- `new_lecture.py`: create a lecture workspace and a starter `.tex` file from the bundled template.
- `clean_transcript.py`: lightly normalize raw transcript text before drafting.
- `intake_inbox.py`: route new files from `inbox/dropbox/` or `pdf/incoming/` into the correct course and material folders.
- `refresh_pdf_outbox.py`: copy compiled lecture PDFs into a shallow top-level `pdf/outgoing/` folder.

### references/

- `workflow.md`: source reconciliation rules for transcript, handwriting, textbook, and screenshots.
- `latex-style.md`: the house style for Chinese LaTeX notes.
- `course-conventions.md`: notation and structure defaults by course.
- `intake-guide.md`: recommended file naming and handoff formats, especially for GoodNotes, PDFs, and transcript exports.
- `github-sources.md`: upstream GitHub projects that informed this skill.

### assets/

- `templates/lecture-note.tex`: the default, compile-ready note template.
