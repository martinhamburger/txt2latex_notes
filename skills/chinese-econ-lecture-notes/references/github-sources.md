# GitHub Sources

This skill was designed by borrowing workflow ideas from upstream GitHub projects while keeping the repository lightweight and easy to maintain. No third-party code is vendored into this skill.

## Skill Structure

- `openai/skills`: used as the structural reference for how a Codex skill should separate `SKILL.md`, scripts, references, and assets.
  - URL: <https://github.com/openai/skills>

## Chinese LaTeX Baseline

- `CTeX-org/ctex-kit`: used as the rationale for choosing a `ctex`-based Chinese LaTeX workflow instead of retrofitting an English article class.
  - URL: <https://github.com/CTeX-org/ctex-kit>

## OCR and Document Parsing References

- `PaddlePaddle/PaddleOCR`: used as the reference point for printed Chinese, structured page parsing, and document-level OCR.
  - URL: <https://github.com/PaddlePaddle/PaddleOCR>
- `breezedeus/Pix2Text`: used as the reference point for mixed prose plus formula images and Markdown-oriented extraction.
  - URL: <https://github.com/breezedeus/Pix2Text>
- `VikParuchuri/texify`: used as a formula-first fallback reference for math OCR workflows.
  - URL: <https://github.com/VikParuchuri/texify>

## Economics LaTeX Style Reference

- `talgross-bu/Template-for-Overleaf`: used as a reminder that economics-facing LaTeX templates should compile simply and stay visually restrained.
  - URL: <https://github.com/talgross-bu/Template-for-Overleaf>

## How These Sources Were Applied

- The repository uses a clean local template instead of copying a third-party note style wholesale.
- OCR tools are treated as optional helpers, not mandatory dependencies.
- The core workflow prioritizes transcript-first drafting because the user already has reliable speech-to-text from iFlytek.
