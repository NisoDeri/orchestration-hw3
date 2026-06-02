# Costs & Resource Analysis

## Headline: $0 to run
The crew runs on **local Ollama** (qwen2.5:14b + aya-expanse:8b) on the author's
GPU. There is **no API spend** — cost is electricity and wall-clock time only. The
gatekeeper still tracks *effort* (calls + seconds per agent) so resource use is
reported regardless of engine.

## Effort profile (local)
A full ~20-page build makes on the order of:
- 10 sections × (1 Writer call + ~1 Translator call for Hebrew/bilingual)
- ~6 Figure calls + ~2 TikZ calls
≈ **25–35 model calls** per build. On a 12 GB RTX 3500 Ada, qwen2.5:14b runs fully on
GPU; expect a few minutes per full build, dominated by the 14B Writer calls.

## If a cloud engine (Claude) were used instead
The same pipeline with `provider="anthropic"` would cost roughly (per full build):

| Model | Est. input | Est. output | Est. cost |
|---|---|---|---|
| Claude Sonnet 4.6 | ~120k tok | ~40k tok | ~$0.96 |
| Claude Haiku 4.5 | ~120k tok | ~40k tok | ~$0.26 |

Over ~20–30 development iterations: ~$5–30 (Sonnet) or ~$1–5 (Haiku). The gatekeeper
enforces `max_cost_usd_per_run` (default $5) and aborts with `CostCapExceededError`.

## Cost-reduction levers (all config-driven, no code change)
1. Use Ollama (default) — $0.
2. Lower `target_words` per section in `config/outline.json`.
3. Assign a cheaper model to non-Writer agents in `config/models.json`.
4. Skip recompilation during drafting (`--no-compile`) and compile only when content is final.
5. Cache: re-run only changed sections (per-section Markdown is saved under `content/`).

## Scaling note
At 1,000 documents/day the bottleneck on local hardware is GPU throughput (serialize
or batch builds), not dollars; on a cloud engine the bottleneck shifts to the
per-run dollar cap and provider rate limits — both enforced by the gatekeeper.
