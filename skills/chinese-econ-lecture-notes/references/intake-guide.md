# Intake Guide

## Fixed Drop Location

Use one of these fixed drop locations:

- `inbox/dropbox/`: the general intake path for transcripts, zips, screenshots, and mixed materials
- `pdf/incoming/`: the shallow intake path for GoodNotes PDFs, textbook PDFs, and slide PDFs

After files are placed there, run:

```bash
python skills/chinese-econ-lecture-notes/scripts/intake_inbox.py
```

The script will:

1. Guess the course from the filename and, for text-like files, from a short content preview.
2. Guess the material type.
3. Move the file into the corresponding `courses/<course>/incoming/` folder.
4. Write a routing manifest into `inbox/processed/`.
5. Move unclear files into `inbox/review/`.

Use `--dry-run` to preview the routing plan first.

## Shallow PDF Access

If you only care about PDF in and PDF out, use:

- `pdf/incoming/` to drop new PDF materials
- `pdf/outgoing/` to quickly open compiled lecture PDFs

After a lecture PDF is compiled, run:

```bash
python skills/chinese-econ-lecture-notes/scripts/refresh_pdf_outbox.py --clean
```

This copies each lecture `main.pdf` into a shallow top-level PDF folder with names like:

- `asset-pricing--2026-03-12-pricing-framework-bonds.pdf`

## Recommended Naming

The file name should make at least two things obvious:

1. Which course it belongs to
2. What kind of material it is

Examples:

- `资产定价-第03讲-转写.txt`
- `资产定价-第03讲-goodnotes笔记.pdf`
- `计量经济学-ols-遗漏变量偏误-转写.zip`
- `国际经济学-ricardian-课本第2章.pdf`
- `中级微观-消费者理论-板书1.jpg`

## GoodNotes Recommendation

For handwritten notes from GoodNotes, prefer one of these:

- Export the relevant pages as a single PDF when the handwriting is reasonably clear and the page order matters.
- Export hard-to-read formula pages as PNG or JPG in addition to the PDF when symbols are dense.

The most useful file naming pattern is:

`课程名-讲次或主题-goodnotes笔记.pdf`

Examples:

- `资产定价-第03讲-goodnotes笔记.pdf`
- `计量经济学-OLS-goodnotes笔记.pdf`

If you want the shortest path, drop GoodNotes PDFs directly into `pdf/incoming/`.

## Transcript Recommendation

For iFlytek or other speech-to-text output:

- Prefer `.txt`
- Keep the raw export if possible
- If the platform gives you a `.zip` with text files, that is also fine

Recommended names:

- `资产定价-第03讲-转写结果.txt`
- `计量经济学-面板数据-讯飞转写.zip`

## Textbook and Slides Recommendation

Use PDF whenever possible. If the source is long, include chapter or page hints in the file name.

Examples:

- `国际经济学-课本-ch04.pdf`
- `资产定价-第03讲-课件.pdf`

## What to Avoid

- Generic names like `IMG_1234.jpg`
- Only using dates without course names
- Mixing many lectures into one file without a topic hint

When the name is weak, the script may still route the file into `inbox/review/` instead of guessing aggressively.
