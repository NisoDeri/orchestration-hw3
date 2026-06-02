# Document Blueprint — "Chromatic Excretion"

> **Purpose of this file.** This is the architect-authored content plan (the "menu page"). The strong model (Claude, acting as Senior Architect) writes this spec; the small local model (qwen2.5:14b, via CrewAI) drafts each section *strictly to this spec*. Every section below states exactly what goes on the page: purpose, key points, the formula(s), the figure/table, length, language, and tone. The Writer agent must not invent structure — it fills these slots. This file is also the source of truth for the document's Table of Contents.

---

## Paper identity

- **Working title (EN):** *Chromatic Excretion: A Quantitative Pharmacokinetic and Colorimetric Analysis of Dietary Pigment Transit in the Human Gastrointestinal Tract*
- **Title (HE):** *הפרשה כרומטית: ניתוח פרמקוקינטי וקולורימטרי כמותי של מעבר פיגמנטים תזונתיים במערכת העיכול האנושית*
- **Fictional venue (deadpan humor):** *Journal of Applied Gastrointestinal Chromatics*, Vol. 1, No. 1.
- **Authors:** Nissim Deri; Yarden Tziar.
- **Course:** 203.3763 — Orchestration of AI Agents. **Instructor:** Dr. Yoram Segal. University of Haifa.
- **Target length:** ~20 pages. **Language split:** ~50% Hebrew (Sections 7–10 + Hebrew halves of Abstract/Conclusion), ~50% English.

## Global tone & style contract (applies to EVERY section)
- **Deadpan clinical register.** Write as a real peer-reviewed article. NO toilet humor, NO slang, NO winking. The comedy is 100% in the contrast between rigorous form and absurd subject. The funnier the premise, the more straight-faced the prose.
- Use precise clinical/scientific terminology: *beeturia, betalain, betacyanin/betanin, anthocyanin, chromophore, luminal transit, spectrophotometric, colorimetric, pharmacokinetic*.
- Hedge like a scientist: "Our model suggests…", "Under the simplifying assumption…", "Results are consistent with…".
- Every claim that *can* carry a citation gets a `\cite{}` (real references — see §13).
- This is a parody; factual correctness is secondary to formal rigor (per the grading rubric: the check is on the envelope, not content correctness). But pigment chemistry, beeturia prevalence, and all math/formulas are *real* and used correctly — that is the joke.

## Required-artifact coverage map (rubric checklist)
| Required artifact | Where it lives |
|---|---|
| ≥1 photo/image | §1 (beetroot), §6 (colour-reference chart), §6 (apparatus photo) |
| ≥1 Python-generated graph | §5 (PK curve), §8/§9 (ΔE-vs-dose, prevalence, transit histogram, heatmap) |
| ≥1 table | §4 (pigment comparison), §6 (method comparison) |
| ≥1 math formula (fancy) | §5 (PK ODE), §5 (Beer–Lambert, Fick), §6 (CIEDE2000), §9 (logistic) |
| TikZ block diagram | §5 (GI transit pipeline), §6 (apparatus schematic) |
| Hebrew↔English BiDi chapter | §7–§10 (Hebrew body) + bilingual Abstract (§2) & Conclusion (§11) |
| Bibliography w/ linked citations | §13 (biblatex + biber, 4-pass compile) |

---

# Section-by-section plan

### §0 — Cover page  · *language: bilingual* · *length: 1 page*
Title (EN + HE), fictional journal + volume, authors, course, instructor, date, university. A small tasteful crest/emblem (TikZ or image). No body text.

### §1 — Abstract / תקציר  · *bilingual (EN then HE)* · *length: ~0.75 page*
- **Purpose:** one-paragraph summary in English, immediately mirrored in Hebrew — the first BiDi showcase.
- **Key points to state:** the phenomenon (dietary pigments visibly altering excreta chromatics), that we build a pharmacokinetic + colorimetric model, that we quantify the shift via CIEDE2000, and headline "findings" (e.g., betanin produces a measurable chromatic shift peaking at ~t hours post-ingestion).
- **Writer instruction:** ≤120 words EN, then a faithful Hebrew rendering (English technical terms kept in Latin script inline: "…מודל פרמקוקינטי (pharmacokinetic)…").

### §2 — Table of Contents · *auto-generated* · *length: ~0.5 page*
LaTeX `\tableofcontents`. Lists all sections + figures + tables. (This is the "menu page" rendered.)

### §3 — Introduction · *English* · *length: ~2 pages*
- **Purpose:** motivate the study; introduce beeturia as a real, documented, under-quantified phenomenon.
- **Key points:** (1) ~10–14% of the population exhibits beeturia after beetroot ingestion `\cite{beeturia}`; (2) anecdotal, qualitative observation dominates the "literature" — a quantitative framework is "lacking"; (3) we propose the first unified pharmacokinetic–colorimetric treatment; (4) contributions list.
- **Figure:** **F1 — photograph of raw + cooked beetroot** (betacyanin source). Caption deadpan: "Figure 1. *Beta vulgaris*, the principal betacyanin vector under study."
- **Graph reference:** forward-reference the prevalence chart (F4) appearing later.

### §4 — Background: Pigment Chemistry & Related Work · *English* · *length: ~2 pages*
- **Purpose:** survey the chromophores responsible for dietary excretory coloration.
- **Key points:** betalains (betacyanin/betanin — red/violet), anthocyanins (blueberry — blue/purple), chlorophyll (leafy greens — green), carotenoids (orange), synthetic azo dyes (e.g., E129). Brief, correct chemistry of why each pigment survives or degrades in luminal transit (pH sensitivity of betanin, etc.).
- **TABLE T1 — Pigment comparison:** columns = Food source | Pigment class | Chromophore | Observed coloration | Typical onset (h) | Duration (h) | pH stability. ~6 rows. This is a required table; make it clean and not overflowing margins.
- **Writer instruction:** factual chemistry where possible; cite `\cite{betalain,anthocyanin}`.

### §5 — A Pharmacokinetic Model of Luminal Pigment Transit · *English* · *length: ~3 pages*
- **Purpose:** the mathematical heart. Build a first-order absorption–elimination model of pigment concentration in the gut.
- **FORMULAS (fancy, real):**
  - Mass-balance ODE: `dC/dt = (ka·D/Vd)·e^{-ka·t} - ke·C`.
  - Closed-form solution: `C(t) = (F·D·ka)/(Vd(ka - ke)) · (e^{-ke·t} - e^{-ka·t})`.
  - Beer–Lambert (links concentration → measured colour intensity): `A = ε · c · ℓ`.
  - Fick's first law (pigment diffusion across the luminal wall): `J = -D_f · (dφ/dx)`.
- **TikZ DIAGRAM D1 — GI transit pipeline:** block diagram: Ingestion → Stomach (pH degradation) → Small intestine (absorption ka) → Colon (residence) → Excretion (output), with the rate constants annotated on the arrows. Required block-schema artifact.
- **Python GRAPH F2 — Concentration vs time:** plot C(t) for betanin vs anthocyanin vs azo-dye using distinct ka/ke. Annotate peak time t_max = ln(ka/ke)/(ka−ke). Title: "Predicted luminal pigment concentration profiles."
- **Writer instruction:** derive t_max from the closed form; keep derivation steps visible (rubric likes shown reasoning).

### §6 — Colorimetric Quantification · *English* · *length: ~2.5 pages*
- **Purpose:** define how we *measure* the chromatic shift objectively.
- **Key points:** introduce CIELAB colour space (L*, a*, b*); define the chromatic shift as the distance between baseline and post-ingestion samples.
- **FORMULA (the showpiece) — CIEDE2000 ΔE₀₀:** present the full ΔE₀₀ expression with its ΔL'/ΔC'/ΔH' terms, weighting functions S_L,S_C,S_H, and rotation term R_T. This is the deliberately monstrous "fancy formula."
- **FIGURE F3 — colour-reference chart:** a clinical-style colour swatch chart (rendered in LaTeX/TikZ as graduated swatches, NOT a stool photo) mapping a* values to "observed coloration grades."
- **IMAGE — apparatus:** a deadpan "spectrophotometric sampling apparatus" — either a TikZ schematic (D2) or a CC-licensed photo of a spectrophotometer. Caption straight-faced.
- **TABLE T2 — method comparison:** visual inspection vs colorimeter vs spectrophotometer vs our CIEDE2000 pipeline (columns: method | quantitative? | cost | inter-rater reliability). Required table #2.

### §7 — שיטות / Methodology · *HEBREW* · *length: ~2 pages* · **[BiDi core chapter]**
- **Purpose:** the "experimental protocol," in Hebrew with inline English terms — the primary RTL↔LTR demonstration.
- **Key points (in Hebrew):** participant "cohort," controlled betanin dosing (D mg), sampling schedule (t = 0,6,12,24,48 h), colorimetric measurement per CIEDE2000, statistical plan. Keep English technical terms in Latin script inline to force BiDi transitions ("…נמדד באמצעות CIEDE2000 ביחס ל-baseline…").
- **Writer/translator instruction:** generate in Hebrew (translator agent); Claude verifies naturalness; ensure numbers/units and Latin terms sit correctly within RTL flow.

### §8 — תוצאות / Results · *HEBREW* · *length: ~2 pages*
- **Purpose:** present the (fabricated-but-plausible) findings in Hebrew.
- **Python GRAPH F4 — prevalence:** bar/pie of beeturia prevalence by genotype/iron-status subgroup.
- **Python GRAPH F5 — ΔE₀₀ vs dose:** sigmoid; threshold dose for "visible coloration."
- **Python GRAPH F6 — transit-time histogram** and/or **heatmap F7** (a* over time × dose).
- **Writer instruction (HE):** reference each figure by number in Hebrew ("איור 5 מראה…"); report mock statistics (mean ± SD, p-values) deadpan.

### §9 — דיון / Discussion · *HEBREW* · *length: ~1.5 pages*
- **Purpose:** interpret results in Hebrew; connect back to the model.
- **FORMULA — dose–response logistic:** `P(visible) = 1 / (1 + e^{-(β0 + β1·dose)})`; estimate the threshold dose where P=0.5.
- **Key points (HE):** agreement between predicted t_max and "observed" peak; limitations (inter-individual ka variation, pH); clinical reassurance that beeturia is benign.

### §10 — מסקנות והשלכות / Implications · *HEBREW* · *length: ~1 page*
- Future work (HE): real-time wearable colorimetry; multi-pigment superposition models; an ML classifier for dietary reconstruction from chromatic output. Deadpan grant-proposal voice.

### §11 — Conclusion / סיכום · *bilingual* · *length: ~0.5 page*
Short EN paragraph + Hebrew mirror. Restate contribution and the headline number. Final BiDi showcase.

### §12 — Acknowledgements / Reproducibility · *English* · *length: ~0.25 page*
Deadpan: data/code available at the project repo; "no beets were harmed beyond culinary norms." Note AI-agent authorship per course policy (honest disclosure).

### §13 — Bibliography · *auto* · *length: ~1 page*
- biblatex + biber, ≥8 references, **linked citations** (clickable `\cite` → entry). Mix of real refs: beeturia/betalain medical literature, Sharma & Bhat on betalains, CIE colorimetry standards, Beer–Lambert, pharmacokinetics text, plus 1–2 deadpan fictional entries from the *Journal of Applied Gastrointestinal Chromatics*.
- **Compile note:** requires 4 passes (lualatex → biber → lualatex → lualatex) so all `\ref`/`\cite` resolve.

---

## Small-model drafting protocol (how the Writer agent consumes this)
1. The Planner agent loads this blueprint and emits one task per section with the slot-spec above.
2. The Writer agent drafts **one section at a time** in Markdown, obeying language, length, and the exact formula/figure/table placeholders (`[[FORMULA: PK_ODE]]`, `[[FIGURE: F2]]`, `[[TABLE: T1]]`).
3. The Figure agent fills `[[FIGURE: Fn]]` by writing + executing matplotlib, saving PNG to `assets/`.
4. The TikZ agent fills `[[DIAGRAM: Dn]]`.
5. The Translator agent renders Hebrew sections (§7–§10) + Hebrew halves.
6. The LaTeX assembler stitches sections into the template; the QA agent compiles and reads the log.
7. Claude (architect) reviews rendered pages, fixes BiDi/overflow, verifies Hebrew with the user.

> Keep each Markdown section file ≤150 lines where it is *code/template*; prose content files are data, but we will externalize long content to `.md`/`.tex` data files, not Python, to respect the 150-line code cap.
