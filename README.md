# chromatic-crew

A **CrewAI** multi-agent system that authors a full academic article and renders it
to a polished, bilingual (Hebrew/English) **PDF** via **LaTeX** — built for HW3 of
*203.3763 Orchestration of AI Agents* (Dr. Yoram Segal, University of Haifa).

The article it produces, *Chromatic Excretion*, is a **deadpan mock-scientific
paper**: a rigorous pharmacokinetic and colorimetric treatment of dietary-pigment
stool chromatics (beeturia). The humour is entirely in the contrast between an
absurd subject and a completely serious, peer-review form — every formula, table,
figure, and citation is real in structure.

> Authors: Nissim Deri, Yarden Tziar. Engine: local **Ollama** (free); the design is
> provider-agnostic and runs on Claude with a one-line config change.

## What it produces
A ~20-page PDF with a cover page, table of contents, headers/footers, real math
(pharmacokinetic ODE, Beer–Lambert, Fick, the full CIEDE2000 colour-difference
formula), Python-generated graphs, TikZ block diagrams, booktabs tables, a
~50% **Hebrew** body with correct RTL/LTR (BiDi) mixing, and a bibliography with
clickable, resolved citations.

## Prerequisites
- **Python 3.11+**
- **uv** (package manager): `pip install uv`
- **Ollama** + models (free, local): `ollama pull qwen2.5:14b` and `ollama pull aya-expanse:8b`
- **MiKTeX** with **LuaLaTeX** + **biber** and a Hebrew font (Windows ships *David*).
  Install via `winget install MiKTeX.MiKTeX`.

## Setup
```bash
uv sync                      # create the environment from uv.lock
cp .env-example .env         # optional; no API key needed for local Ollama
```

## Usage
```bash
uv run python -m chromatic_crew              # generate content + figures, then compile the PDF
uv run python -m chromatic_crew --no-compile # generate + assemble body.tex, skip compilation
uv run python -m chromatic_crew --version
```
Output: `latex/main.pdf`. Per-section Markdown drafts are saved under `content/`,
figures under `assets/`.

## How it works (architect-led crew)
A **Senior Architect** (the strong model / human-in-the-loop) authors the blueprint
(`docs/BLUEPRINT.md`), the machine-readable `config/outline.json`, the agent
personas (`config/agents.json`), and the per-section prompt briefs
(`orchestration/briefs.py`). The CrewAI agents then execute to spec:

| Agent | Role |
|---|---|
| Planner | turns the blueprint into per-section briefs |
| Writer | drafts each section in deadpan English |
| Figure | writes + executes matplotlib → PNG |
| TikZ | emits block-diagram TikZ |
| Translator | renders Hebrew sections with BiDi-safe Latin terms |
| Assembler | Markdown → LaTeX (`body.tex`) |
| QA | reads the compile log, fixes overflow / unresolved citations |

The pipeline (in `sdk.build_paper`): load + version-validate config → build the
gatekeeper + agents → per section generate content/figures/diagrams → convert to
LaTeX → assemble `body.tex` → compile 4 passes (`lualatex → biber → lualatex → lualatex`).

## Configuration (zero hardcoding)
Everything tunable lives in `config/`: `setup.json` (topic, language split, paths),
`models.json` (model + temperature per agent; switch `provider` to `anthropic` to use
Claude), `rate_limits.json` (gatekeeper limits + cost cap), `agents.json` (personas),
`outline.json` (the document plan). Secrets only via environment (`.env`).

## Project structure
```
config/      setup, models, rate_limits, agents, outline (all versioned)
docs/        BLUEPRINT, PRD, PLAN, TODO, per-mechanism PRDs, COSTS
src/chromatic_crew/  sdk/ agents/ orchestration/ services/ shared/ cli/
latex/       main.tex (template), body.tex (generated), references.bib
assets/      generated figures
tests/       unit + integration
```

## Costs
Running locally on Ollama costs **$0** (electricity + time only). The gatekeeper
tracks effort regardless and enforces a dollar cap if a cloud engine is ever used.
See `docs/COSTS.md`.

## AI-use disclosure
Per course policy: this project was produced with AI assistance. A CrewAI agent team
(local Ollama) generates drafts, figures, and LaTeX; the authors act as architect and
editor (planning, prompt design, Hebrew verification, final edit). See `prompts.md`.

## License
MIT (see `LICENSE`).
