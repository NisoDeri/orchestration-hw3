# PRD — Product Requirements Document

**Project:** `chromatic-crew` — a CrewAI multi-agent system that authors a full academic article and renders it to a polished, BiDi (Hebrew/English) PDF via LaTeX.
**Course:** 203.3763 Orchestration of AI Agents · Dr. Yoram Segal · University of Haifa.
**Authors:** Nissim Deri, Yarden Tziar. **Version:** 1.00.

## 1. Context & motivation
HW3 requires a CrewAI agent team to write an article on a topic of our choice and emit a respectable PDF via LaTeX (not Overleaf), with images, a Python-generated graph, a table, math formulas, a Hebrew↔English BiDi chapter, and a linked bibliography. Grading is **technical/visual on the rendered "envelope"** (citations resolve, formulas are real math, tables fit margins, BiDi not garbled, looks clean) and **creativity is explicitly valued**.

The chosen article is a **deadpan mock-scientific paper**, *Chromatic Excretion* — a rigorous pharmacokinetic + colorimetric treatment of dietary-pigment stool chromatics (beeturia). Humor lives entirely in the contrast between absurd subject and rigorous form. See `docs/BLUEPRINT.md` for the full content plan.

## 2. Goals & KPIs (acceptance criteria)
- **G1** A single command produces `output/chromatic_excretion.pdf` (~20 pages).
- **G2** PDF contains, and they render correctly: ≥1 photo, ≥1 Python-generated graph, ≥1 table, ≥1 "fancy" math formula, ≥1 TikZ block diagram, a Hebrew BiDi chapter (~50% of the document in Hebrew), and a bibliography with **clickable, resolved** citations (4-pass compile).
- **G3** Zero LaTeX `Overfull \hbox` over margin / no table exceeds page width; no unresolved `??` refs/cites.
- **G4** The CrewAI crew genuinely generates content (drafts, figures, TikZ, translation, assembly, QA) — not a passthrough.
- **G5** Rubric gates pass: SDK entry point, API gatekeeper, config-driven (zero hardcoding), ≤150-line code files, ruff-clean, tests ≥85%, uv-managed, version-tracked, cost/effort tracked, CI green.

## 3. Functional requirements
- **FR1** Config-driven crew: topic, language split, page target, and **model-per-agent** all from `config/*.json` (no hardcoding).
- **FR2** Agents: Planner, Writer, Figure (writes+executes matplotlib), TikZ-diagram, Hebrew Translator, LaTeX-assembler, QA (reads compile log, fixes overflow/citation issues).
- **FR3** Provider-agnostic engine via LiteLLM: default **Ollama** (local, free); Anthropic path supported in config but unused (no API key).
- **FR4** Markdown-first: agents emit Markdown + asset files; assembler converts to LaTeX; only then compile to PDF.
- **FR5** Architect/editor (Claude) authors the blueprint, prompts, exemplars, formulas, and performs the final editorial + Hebrew pass.
- **FR6** Cost/effort tracking per agent (tokens where applicable, wall-clock always — meaningful even on free local models).

## 4. Non-functional requirements
- **NFR1** Professional-software rubric compliance (see `grading-rubric`): SDK layer, gatekeeper, OOP no-duplication, TDD ≥85%, ruff zero violations, ≤150-line files, uv, versioning from 1.00, secrets via env.
- **NFR2** Reproducible: `uv run` for everything; `uv.lock` committed; deterministic seeds where randomness exists (figure data).
- **NFR3** Portable: runs on a fresh Windows machine with MiKTeX + Ollama; README documents setup.

## 5. Constraints, assumptions, out-of-scope
- **C1** No paid API, no API key (enterprise key gated; user won't pay). Engine = local Ollama; Claude quality delivered via architect/editor pass.
- **C2** LaTeX engine = **LuaLaTeX** (best Hebrew/BiDi) via MiKTeX; bibliography via biber. Not Overleaf.
- **C3** Hebrew quality lever = translator drafts + Claude/architect rewrite + Hebrew-native (user) verification.
- **Out of scope:** real human-subjects data (the paper is parody; figure data is synthetic-but-plausible and labeled as modeled).

## 6. Milestones
1. Planning docs + blueprint (this). 2. Toolchain (uv/Ollama/MiKTeX). 3. Crew + config + SDK + gatekeeper. 4. LaTeX BiDi template. 5. Content generation + figures + compile/QA loop. 6. Hebrew pass + verification. 7. Cost tracking + CI + git submission.
