# Benchmark Run History

How the Agent Failures datasets were produced — v1 first run, v2 domain expansion, and export rules.

The evaluation harness (FastAPI + SQLite + dashboard) is **not published** in this repo. This document describes what was run and what landed in `data/`.

---

## Pipeline overview

```
Task bank → Agent runner (OpenRouter) → Trace logger → Lakmus judge → Export (canonical dedupe)
```

- **Judge:** Gemini 3.1 Flash Lite via OpenRouter
- **Run mode:** `benchmark` — same task set on every selected model
- **v2 tool calling:** Real calculator wired for finance tasks

---

## v1 benchmark (June 2026)

| Setting | Value |
|---------|-------|
| Tasks | 50 generated |
| Models | Gemini Flash, Sonnet 4, GPT-4o Mini, Haiku, DeepSeek V3, Qwen 2.5 7B, Llama 3.1 8B |
| Paired set | **49** tasks (all 7 models judged) |
| Published | 110 failures + 233 passes |
| Paired failure rate | **32.1%** |

### v1 harness caveat

The v1 pipeline **did not wire a real calculator**. Models that computed correctly in text were still flagged `wrong_tool_selection / calculator_not_used`. Finance/calculator template results are partly **judge artifact** — see original session notes below.

### v1 cleanup performed

- Mock test traces removed
- Stuck traces re-judged where needed
- Public export uses paired + canonical dedupe only

---

## v2 benchmark (domain expansion)

| Setting | Value |
|---------|-------|
| Task bank | [`data/task-manifest-v2.json`](../data/task-manifest-v2.json) — **56 frozen tasks** |
| Domains | 7 × 8 tasks (easy / medium / hard) |
| Models (core) | Same 7 as v1 |
| Paired set | **56** tasks (all core 7 judged) |
| Published | 91 failures + 301 passes |
| Paired failure rate | **23.2%** |

### v2 improvements over v1

- Frozen manifest (reproducible `bank_id` keys like `FD-M01`)
- Domain labels on every task
- Calculator tool via function calling
- Gap-fill scripts for incomplete model×task coverage

### Extended model runs

| Model | v2 canonical judged | In 9-model paired set |
|-------|---------------------|------------------------|
| GPT-4o | 56 | 49 |
| Hermes 3 70B | 49 | 49 |

Hermes is missing **7 finance `FD-*` tasks** — not yet gap-filled. The 9-model paired leaderboard uses **49 tasks** where all nine models have a trace.

Stats: [`data/stats-all-models.json`](../data/stats-all-models.json)

---

## Duplicate runs and canonical dedupe

Early v2 benchmark sessions **re-imported the task bank**, creating duplicate `Task` rows in the internal database. Raw per-model judged counts reached **70–86** while the logical benchmark is **56 tasks**.

**Public artifacts exclude duplicates:**

1. **Canonical dedupe** — one trace per `(task_key, model)`, newest wins
2. **Paired filter** — only tasks where every comparison model has exactly one judged trace

Raw DB totals are **not** exported to JSONL or paired stats. See [METHODOLOGY.md](METHODOLOGY.md).

---

## Export (reproduce public files)

From the private harness workspace:

```bash
cd backend
set PYTHONPATH=.

# Full export (v1 + v2 JSONL + all stats sidecars)
python scripts/export_public_dataset.py

# v2 only
python scripts/export_public_dataset.py --version v2

# Audit model coverage
python scripts/audit_all_models.py
python scripts/audit_v2_run.py

# Gap-fill missing model×task cells
python scripts/run_v2_gap_fill.py --models or-hermes-3-70b
```

Output lands in repo `data/` at the repository root.

---

## Stability study

20 frozen prompts, multiple repeats per model — pass@k and tier estimates.

| Artifact | Description |
|----------|-------------|
| [`data/stability-tasks-v1.json`](../data/stability-tasks-v1.json) | Frozen prompt set |
| [`data/stability-v1.json`](../data/stability-v1.json) | Tier analysis |

Run (harness):

```bash
python scripts/run_stability_study.py --models or-gemini-flash or-claude-haiku or-llama-3.1-8b --repeats 3
python scripts/analyze_stability.py
```

---

## Historical v1 session notes (June 13, 2026)

First multi-model run — preserved for context.

| Metric | Value |
|--------|-------|
| Duration | ~2 hours |
| Raw judged (pre-dedupe) | 365 |
| Failure rate (raw) | ~31.8% |

**Failure taxonomy (v1 raw run):**

| Type | Share |
|------|-------|
| `constraint_violation` | 43% |
| `wrong_tool_selection` | 28% |
| `unsupported_claim` | 19% |
| `goal_drift` | 9% |

**Template hot spots:** `calculator_task` 94% fail (harness artifact), `workflow_steps` 3% fail.

**Infrastructure (internal):** API port 8002, dashboard 3000, SQLite `lakmus.db`.

---

## Related

- [METHODOLOGY.md](METHODOLOGY.md) — paired vs canonical vs raw
- [DATASET.md](DATASET.md) — public file inventory
- [FAILURE_REPORT_v1.md](FAILURE_REPORT_v1.md) · [FAILURE_REPORT_v2.md](FAILURE_REPORT_v2.md)
