# Development Log — failures encountered and how we fixed them

This log documents the real engineering process: what broke, why, and the fix. It
complements `prompts.md` and is reflected in the git commit history. (The grading
guidelines value visible, AI-assisted iteration — not a polished result with no trail.)

## Environment & toolchain
1. **Python `site` crash on a Hebrew project path.** The project lives under a path
   containing Hebrew (`…\לימודים\…`). uv's editable-install `.pth` embedded that path
   in UTF-8; Python's `site` reads `.pth` with the Windows `cp1252` codec and died with
   `UnicodeDecodeError: 'charmap' ... byte 0x9d`. **Fix:** set `[tool.uv] package = false`
   (tests import via pytest `pythonpath`, CLI via `PYTHONPATH=src`) and rebuilt the venv,
   removing the offending `.pth`.
2. **venv deletion blocked by Windows MAX_PATH.** `litellm` ships benchmark files with
   paths > 260 chars; PowerShell `Remove-Item` couldn't delete them. **Fix:** `uv venv --clear`
   (Rust, long-path aware).
3. **MiKTeX first run hung.** The first `lualatex` invocation stalled (no `.log` after 13 min)
   waiting on an interactive "install package?" prompt in a non-interactive shell. **Fix:**
   `initexmf --set-config-value [MPM]AutoInstall=1`, killed the stuck process, and ran a
   trivial warm-up compile to build the format + fetch base packages unattended.

## Crew / model behaviour
4. **Figure agents ignored `out_path`.** They called `plt.savefig('their_name.png')`, dumping
   PNGs into the project root instead of `assets/Fx.png`. **Fix:** `figure_service` now forces
   every `savefig` to the target path, with a fallback that saves the current figure if the
   model never calls `savefig`.
5. **Local models cannot do Hebrew.** `aya-expanse:8b` rambled, repeated, and leaked Chinese;
   `qwen2.5:14b` collapsed into a ~20× repetition loop with Chinese/Cyrillic and a corrupted
   heading. **Decision:** `hebrew_strategy = "editor"` — the crew drafts English (which it does
   excellently); the architect/editor (Claude) authors the Hebrew; the translator agent is
   retained in the codebase (and the `"agent"` path) for code review.
6. **One figure crashed mid-run.** A matplotlib broadcast-shape error killed `F6`. **Fix:**
   wrapped figure/diagram generation in try/except (log + skip), and authored the specialized
   figures (CIELAB chart, transit histogram, Bristol scale, pH–ΔE, correlation heatmap) directly.

## LaTeX / converter fixes (first compile)
7. `$$\tag*{\blacksquare}$$` — `\tag` is illegal in `$$…$$`; removed.
8. TikZ `rounded rectangle` unknown — added `\usetikzlibrary{shapes.misc}`.
9. CIELAB `L*a*b*` corrupted — the Markdown→LaTeX converter's `*italic*` rule ate the asterisks
   in scientific notation and inside math. **Fix:** removed single-`*` italic handling.
10. Unescaped `%` commented out text; literal Greek `β`/`Δ` missing in Latin Modern. **Fix:**
    escape `%`/`#` in the converter; use `$\beta$`, `$\Delta E$` in content.
11. Hebrew section headings/captions rendered in Latin Modern (no glyphs). **Fix:** wrap
    Hebrew-containing headings/captions in `\texthebrew{}` so polyglossia applies RTL + font.
12. Reversed cover subtitle — raw `\hebrewfont` set the font but not direction. **Fix:** `\texthebrew{}`.
13. 7-column table overflowed the margin (+44 pt); long inline-math bullets overflowed (+100 pt).
    **Fix:** converter wraps tables in `\small` + tighter `\tabcolsep`; converted the bullet
    definitions to an `aligned` display block.

## Scope pivot
14. **Urine → stool.** The model leaned into *beeturia* (red urine); the intended subject is
    **faecal chromatics**. Re-anchored the blueprint/brief on STOOL, added measures beyond colour
    (Bristol Stool Scale consistency, faecal pH, transit, a Faecal Chromatics Index), and expanded
    from 10 → 14 sections (~12 → ~21 pages).
