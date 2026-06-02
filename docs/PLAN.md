# PLAN — Architecture & Design

**Project:** `chromatic-crew` · **Version:** 1.00 · See `PRD.md` and `BLUEPRINT.md`.

## 1. C4 — Context
```
[User / CLI] --> [chromatic-crew SDK] --> [CrewAI orchestration] --> [LLM engine (Ollama, via LiteLLM)]
                                   |                               --> [Tools: web/Wikipedia search, Python exec, file I/O]
                                   v
                          [LaTeX pipeline: MiKTeX/LuaLaTeX + biber] --> output/chromatic_excretion.pdf
                                   ^
                   [Architect/Editor (Claude): blueprint, prompts, exemplars, final edit + Hebrew]
```

## 2. C4 — Containers / layers
- **SDK layer** (`src/chromatic_crew/sdk/sdk.py`): single entry point — `build_paper(config) -> PaperResult`. All consumers (CLI, tests) go through it. No business logic elsewhere.
- **Orchestration** (`orchestration/`): CrewAI crew + task graph; sequences Planner → Writer → Figure/TikZ → Translator → Assembler → QA.
- **Agents** (`agents/`): one module per agent role, subclassing a shared `BaseAgent` (mixins for prompt-loading, cost tracking). Mirrors HW2's pattern.
- **Services** (`services/`): `latex_service` (assemble + compile, 4 passes), `figure_service` (exec matplotlib), `bib_service`.
- **Shared** (`shared/`): `gatekeeper.py` (all LLM/tool calls routed here: rate-limit, retry, cost/effort logging), `config.py` (loader + version validation), `version.py`, `seeding.py`, `exceptions.py`.
- **Content/assets**: `content/*.md` (per-section drafts), `assets/*.png` (figures/photos), `latex/` (template, .tex, .bib), `output/` (PDF).

## 3. Data flow
1. Planner loads `BLUEPRINT.md` + config → emits per-section task specs with slot placeholders (`[[FORMULA:…]]`, `[[FIGURE:…]]`, `[[TABLE:…]]`).
2. Writer drafts each section (Markdown) to spec; Figure/TikZ agents fill visual slots (execute code, save assets); Translator renders Hebrew sections.
3. LaTeX assembler injects content + assets into the BiDi template → `.tex`; bib_service emits `.bib`.
4. latex_service compiles: `lualatex → biber → lualatex → lualatex` (4 passes); QA agent parses the `.log` for `Overfull \hbox`, unresolved `??`, missing fonts → feeds fixes back.
5. Architect/Editor (Claude) reviews rasterized pages, finalizes prose + Hebrew, re-compiles.

## 4. Architectural decisions (ADRs)
- **ADR-1 — Engine = local Ollama via LiteLLM, provider-agnostic.** *Rationale:* no API key/budget; CrewAI+LiteLLM make model a config value; Claude quality delivered via architect editing. *Trade-off:* weaker raw Hebrew → mitigated by editor pass.
- **ADR-2 — Architect-led crew (not hollow).** *Rationale:* real generation survives code review + honors course ethic; strong prompts/exemplars from Claude make a 14B model viable. *Trade-off:* more prompt-engineering up front.
- **ADR-3 — LuaLaTeX + polyglossia/bidi for BiDi.** *Rationale:* best Hebrew shaping + RTL/LTR mixing; deterministic typesetting independent of authoring model. *Alt rejected:* XeLaTeX (allowed, slightly weaker luatex font handling), pdfLaTeX (poor Hebrew).
- **ADR-4 — Markdown-first, convert late.** *Rationale:* fast iteration/review before LaTeX brittleness (professor's own recommendation). 
- **ADR-5 — Model-per-agent.** Writer/Planner/QA = `qwen2.5:14b`; Translator = Hebrew-capable model (DictaLM/Aya); cheap roles = 7–8B. Mirrors HW2.

## 5. Key contracts
- `PaperConfig` (pydantic): topic, language_split, page_target, models{per-agent}, paths, versions.
- `SectionSpec`: id, title_en, title_he, language, length, slots[].
- `PaperResult`: pdf_path, page_count, compile_warnings[], cost_report.

## 6. Testing strategy
Unit tests mirror `src/`; mock LLM + subprocess (lualatex) calls. Cover config validation, gatekeeper (rate/cost/retry), section-spec parsing, latex assembly, log parsing. Integration test compiles a tiny 2-page fixture end-to-end (no live LLM). Coverage gate ≥85%.
