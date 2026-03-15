# Workflow

## Core Principle

Use the transcript as the backbone of the note. Use handwriting, textbook pages, and screenshots to correct or enrich the backbone. Do not let a noisier visual source override a clearer transcript unless the visual source is clearly more authoritative for notation or layout.

## Recommended Order

1. Identify the course, lecture title, and lecture date.
2. Read the transcript once without editing to understand the lecture arc.
3. Mark the main topic shifts.
4. Check handwriting or screenshots for board structure, formulas, diagrams, and emphasized phrases.
5. Check textbook pages only for exact statements or standard model setup.
6. Draft the LaTeX note from the cleaned structure.
7. Re-read once for notation consistency and once for Chinese readability.

## Source Reconciliation Rules

### Transcript

- Keep the transcript's ordering unless there is a clear reason to reorder for readability.
- Compress repetition, greetings, and filler.
- Keep economically meaningful verbal hedges such as "under this assumption" or "in equilibrium".

### Handwritten Notes

- Use handwriting to repair symbols, variable names, sign conventions, and missing lines in derivations.
- If a handwritten board has a partial derivation, explain the skipped steps in prose rather than pretending the board showed everything.
- Treat highly ambiguous handwriting as evidence, not truth.

### Textbook Pages

- Use textbook pages for exact theorem wording, standard diagrams, and canonical assumptions.
- If the instructor's lecture differs from the textbook, record the lecture version and note the difference briefly when useful.
- Do not expand the note into a full textbook summary unless the user explicitly asks.

### Slide Screenshots

- Use screenshots to reconstruct bullet hierarchy and model assumptions.
- If slides and transcript disagree, prefer the transcript for spoken emphasis and the slides for exact displayed formulas.

## Ambiguity Policy

- Never invent unreadable symbols.
- Prefer a short `% TODO` comment to a confident but wrong equation.
- If the transcript strongly implies a formula form but one symbol is uncertain, write the confirmed part and annotate the uncertain symbol in a comment.

## Default Note Shape

For most lectures, use this order:

1. `本讲概览`
2. `核心概念` or `模型设定`
3. `推导与证明`
4. `经济学直觉` or `结论与应用`
5. `遗留问题` when needed

For short lectures, merge sections. For technical lectures, split assumptions and derivations more aggressively.

## Single-File Course Policy

- Each course must maintain a single cumulative note file in `courses/<course-key>/output/tex/<course-key>-notes.tex`.
- New lecture materials (even on future dates) should be appended as new sections/subsections inside the same course note file.
- If source segments come from different timestamps, note the timestamp briefly inside the document body, not in filenames.
- Recommended command: `python skills/chinese-econ-lecture-notes/scripts/sync_course_notes.py --course <course-key> --compile`.

## PDF Export and Naming

- Compile the cumulative course note PDF to `courses/<course-key>/output/pdf/<course-key>-notes.pdf`.
- Export to top-level outbox with `scripts/refresh_pdf_outbox.py`.
- Outbox filenames must use `course-key.pdf` so there is exactly one exported note file per course.
- If re-exporting a full batch, prefer `scripts/refresh_pdf_outbox.py --clean` to keep `pdf/outgoing/` and `pdf/outgoing/index.json` in sync.

## When to Use External OCR Tools

Use external OCR only when it meaningfully reduces ambiguity:

- Printed Chinese textbook or handout pages: prefer PaddleOCR-style document parsing.
- Mixed formula plus prose images: prefer Pix2Text-style parsing.
- Formula-heavy cropped images: prefer texify-style math OCR.

If Codex vision already resolves the content well, do not add extra tool complexity.
