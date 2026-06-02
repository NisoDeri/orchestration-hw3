# PRD — CrewAI Multi-Agent Mechanism

## Purpose
Generate a full academic article section-by-section using a team of specialized
CrewAI agents, under tight architect-authored guidance so a small local model
(qwen2.5:14b) produces on-spec, publication-form output.

## Agents (config-driven personas in `config/agents.json`)
- **Planner** — converts `docs/BLUEPRINT.md` / `config/outline.json` into per-section briefs.
- **Writer** — drafts each section in deadpan clinical English to the brief's slots.
- **Figure** — emits self-contained matplotlib code (executed by `figure_service`).
- **TikZ** — emits compilable TikZ block diagrams.
- **Translator** — renders English → academic Hebrew, wrapping Latin terms `\textenglish{}` for BiDi.
- **Assembler** — Markdown → LaTeX fragment (handled deterministically by `markdown_to_latex`).
- **QA** — parses the compile log, proposes overflow/citation fixes.

## Design decisions
- **Architect-led, not autonomous.** Structure, formulas, slots, and Hebrew/English
  split are fixed by the architect; agents fill predefined slots. This makes a weak
  local model viable and keeps output deterministic and on-rubric.
- **English-first.** Even Hebrew sections are drafted in English (the model's strongest
  language) then translated, then editor-verified — maximizing quality.
- **Per-agent models.** `config/models.json` assigns a model + temperature per agent;
  the translator can be upgraded to Claude independently.
- **Every model call routes through the gatekeeper** (see `PRD_gatekeeper.md`).

## Inputs / outputs
- Input: `config/outline.json` (SectionSpec list with slots), agent personas, models.
- Output: per-section Markdown (`content/<id>.md`), figure PNGs (`assets/`), TikZ source,
  consumed by the LaTeX pipeline.

## Acceptance
Each configured section yields Markdown obeying its language + slots; figures render;
the run is reproducible (seeded) and cost/effort-tracked.
