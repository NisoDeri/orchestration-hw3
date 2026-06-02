# TODO — Task Tracking

Status: ☐ todo · ◐ in-progress · ☑ done. Version 1.00.

## Phase 0 — Planning & docs
- ☑ T-001 Author `BLUEPRINT.md` (content plan / menu)
- ◐ T-002 Author `PRD.md`, `PLAN.md`, `TODO.md`
- ☐ T-003 `README.md` (setup + usage, user-manual level)
- ☐ T-004 Per-mechanism PRDs: `PRD_crew.md`, `PRD_latex_bidi.md`, `PRD_gatekeeper.md`

## Phase 1 — Toolchain
- ☑ T-010 Install `uv`
- ◐ T-011 Install Ollama (background)
- ☐ T-012 Pull models: `qwen2.5:14b` (writer), Hebrew model (translator)
- ☐ T-013 Install MiKTeX + LuaLaTeX + biber + Hebrew fonts (David CLM / Noto Hebrew); UAC prompt
- ☐ T-014 `uv init` project; add deps (crewai, litellm, matplotlib, pydantic, pytest, ruff); commit `uv.lock`

## Phase 2 — Core scaffold (rubric)
- ☐ T-020 `pyproject.toml` (ruff E,F,W,I,N,UP,B,C4,SIM; pytest cov fail_under=85; uv)
- ☐ T-021 `.gitignore`, `.env-example`
- ☐ T-022 `src/chromatic_crew/` package: `sdk/`, `agents/`, `orchestration/`, `services/`, `shared/`, `constants.py`
- ☐ T-023 `shared/config.py` + `version.py` (1.00) + version validation
- ☐ T-024 `shared/gatekeeper.py` (rate-limit, retry, cost/effort logging)

## Phase 3 — Crew
- ☐ T-030 `BaseAgent` + mixins; per-agent modules (Planner, Writer, Figure, TikZ, Translator, Assembler, QA)
- ☐ T-031 CrewAI task graph in `orchestration/`
- ☐ T-032 Architect-authored prompts + few-shot exemplars per agent (`prompts/`)
- ☐ T-033 `config/`: `setup.json`, `models.json`, `rate_limits.json`, `outline.json` (from BLUEPRINT)

## Phase 4 — LaTeX BiDi pipeline
- ☐ T-040 Template: cover, TOC, headers/footers, polyglossia EN+HE, Hebrew font, fancy-math, TikZ, biblatex
- ☐ T-041 `latex_service` (assemble + 4-pass compile) + `bib_service`
- ☐ T-042 `figure_service` (exec matplotlib → PNG)

## Phase 5 — Generate & QA
- ☐ T-050 Run crew → content + figures + diagrams
- ☐ T-051 Assemble + compile; rasterize pages; QA loop (overflow / unresolved refs / BiDi)
- ☐ T-052 Architect editorial pass (English polish)

## Phase 6 — Hebrew
- ☐ T-060 Translator pass on §7–§10 + bilingual abstract/conclusion
- ☐ T-061 Claude proofread + BiDi fixes; user (native) verification

## Phase 7 — Finalize
- ☐ T-070 Tests ≥85%, ruff clean, file-size cap check
- ☐ T-071 `prompts.md` engineering log, `COSTS.md`
- ☐ T-072 `.github/workflows/ci.yml`
- ☐ T-073 git init + push to `NisoDeri/orchestration-hw3`
