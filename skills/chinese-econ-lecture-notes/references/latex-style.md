# LaTeX Style

## Design Goal

Produce notes that are clean, stable, and easy to revise. Prefer clarity over decoration.

## Engine and Base Class

- Default engine: `xelatex`
- Preferred build command: `latexmk -xelatex main.tex`
- Default class: `ctexart`

Use `ctexart` because the notes are primarily Chinese and should compile reliably with Chinese text, equations, and occasional English terminology.

## Layout Rules

- Use A4 paper and moderate margins.
- Avoid colored boxes unless the user explicitly asks.
- Avoid complex page themes, shaded theorem blocks, or presentation-style effects.
- Use `enumitem`, `booktabs`, `amsmath`, `amssymb`, `amsthm`, and `mathtools` as the core package set.

## Chinese Writing Rules

- Write the main prose in Chinese.
- On first use, optionally format a technical term as `中文 (English)` if that improves recall.
- Keep punctuation natural for Chinese prose.
- Do not force English-only section names in a Chinese note.

## Math Rules

- Use `align` or `aligned` for multi-line derivations.
- Use `equation` only when a single numbered equation is needed.
- Label only equations that will actually be referenced later.
- Define reusable macros for expectations, variances, sets, derivatives, and operators.
- Never use `$$ ... $$`.

## Tables and Figures

- Use `booktabs` for tables.
- Use tables only when the lecture genuinely compares assumptions, estimators, equilibria, or cases.
- Include figures only when a diagram materially helps understanding, such as offer curves, indifference curves, or payoff trees.

## Tone

- Convert spoken language into concise written Chinese.
- Keep intuition paragraphs short and concrete.
- Prefer short bullet lists to long dense paragraphs when summarizing assumptions or cases.

## Compilation Checklist

1. Check for unmatched braces.
2. Check that theorem environments are closed.
3. Check that math macros used in the body are defined in the preamble.
4. Check that `\ref` targets exist.
5. Check that Chinese text does not appear inside math mode unless it is wrapped with `\text{}`.
