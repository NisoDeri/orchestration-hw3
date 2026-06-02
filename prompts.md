# Prompt Engineering Log

This log documents how the system is prompted and the engineering decisions behind
it. Per course policy, it also discloses how AI was used.

## Strategy: architect-led crew
The strong model / human acts as **Senior Architect**: it authors the blueprint
(`docs/BLUEPRINT.md`), the machine-readable outline (`config/outline.json`), agent
personas (`config/agents.json`), and the deterministic prompt builders
(`orchestration/briefs.py`). The small local model (qwen2.5:14b via CrewAI) only
**fills predefined slots**. This is the course's own model — "the programmer becomes
a senior architect orchestrating AI agents" — and it makes a weak local model
produce on-spec, publication-form output.

## Key prompt decisions
1. **Deadpan style contract** (in `briefs.STYLE_CONTRACT`): absolute clinical
   seriousness, precise terminology, scientific hedging, Markdown + `$...$` math, and
   an explicit ban on inventing structure. The comedy must come only from rigorous
   treatment of an absurd subject — so the prose must never wink.
2. **English-first, then translate.** Even the ~50% Hebrew sections are drafted in
   English (the model's strongest language), then rendered to Hebrew by the Translator
   agent, then verified by the authors. This maximizes both content and Hebrew quality.
3. **Slot-marker protocol.** The Writer leaves `[[FIGURE:NAME|caption]]`,
   `[[DIAGRAM:NAME|caption]]`, `[[CITE:key]]` markers; downstream agents/converters
   fill them. This decouples prose from figure/diagram/citation generation.
4. **BiDi instruction.** The Translator wraps Latin technical terms as
   `\textenglish{...}` and preserves numbers/units, so RTL/LTR mixing renders cleanly.
5. **Per-agent models** (`config/models.json`): low temperature for QA/assembler,
   higher for the Writer; the Translator can be upgraded to Claude independently.

## Lessons carried from HW1 / HW2
- **Don't over-claim.** HW1's high self-score invited harsher scrutiny; we keep
  documentation honest and let the artifact speak.
- **Cost & quality gates are graded.** We track cost/effort (gatekeeper), enforce
  ruff-clean + ≥85% coverage + the 150-line file cap in CI, and keep planning docs.
- **File-size discipline.** Long content lives in data/`.md`/`.tex`, never in oversized
  Python files (HW2 was flagged for 200-line data modules).

## AI-use disclosure
A CrewAI agent team running on local Ollama generates the drafts, figures, and TikZ;
the authors act as architect and editor (planning, prompt design, Hebrew verification,
and final editorial pass). Responsibility for the submission rests with the authors.
