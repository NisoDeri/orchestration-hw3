# PRD — API Gatekeeper

## Purpose
A single centralized chokepoint (`shared/gatekeeper.py`) through which **every**
external model/tool call is routed — required by the grading rubric and good practice.
Even with the free local Ollama engine the path is always used, so behavior is
identical and correct the instant the engine is swapped to a metered cloud model
(Claude).

## Responsibilities
- **Rate limiting** — per-service sliding-window limiter (`requests_per_minute`) plus a
  semaphore bounding `concurrent_max`; callers queue on the semaphore when full.
- **Retry** — transient failures retried up to `max_retries` with linear backoff
  (`retry_after_seconds * attempt`); exhaustion re-raises.
- **Cost & effort tracking** — `CostTracker` accumulates per-service calls, tokens,
  wall-clock seconds, and USD; enforces `max_cost_usd_per_run` (cloud only; local = $0).
- **Logging** — every call logs service, duration, tokens, and cost.

## Configuration (`config/rate_limits.json`, versioned)
Per-service `requests_per_minute`, `concurrent_max`, `retry_after_seconds`,
`max_retries`; global `cost.max_cost_usd_per_run`. Nothing hardcoded.

## Interface
`Gatekeeper.execute(fn, *args, service="...", usage_of=None, **kwargs)` runs `fn`
under the named service's limits + tracking; `usage_of` optionally extracts a `Usage`
from the result for cost accounting. `cost_report` returns per-service totals.

## Acceptance
No model/tool call bypasses the gatekeeper; limits are read from config; transient
failures recover; the run aborts cleanly (`CostCapExceededError`) if a cloud cap is hit.
