# Benchmark Methodology

How Lakmus compares LLM agents fairly — and why raw trace counts are misleading.

---

## The problem we solve

Agent benchmarks often report failure rates like “9 failures out of 86 judged traces.” That sounds precise, but it is not comparable across models if:

- Model A ran 86 tasks and Model B ran 56
- The same task was executed twice after a re-run and both traces were counted
- One model missed a subset of the task bank (e.g. 7 finance tasks never run)

**Agent Failures** publishes rates only on **identical task sets** with **one trace per (task, model)** unless noted otherwise.

---

## Three layers of statistics

| Layer | What it is | When to use |
|-------|------------|-------------|
| **Paired benchmark** | Tasks where *every* model in the comparison set has exactly one judged trace | **Public leaderboards**, papers, HF dataset card |
| **Canonical deduped** | One trace per `(task_key, model)` — latest run wins if duplicates exist | Per-model totals across v1+v2; inventory checks |
| **Raw DB totals** | Every judged trace in the evaluation database | Internal ops only — **do not** use for public rates |

### Paired benchmark (preferred)

A task enters the paired set only if **all** comparison models completed it with a judged trace.

- **v1 paired (core 7):** 49 tasks — see [`data/stats-paired-v1.json`](../data/stats-paired-v1.json)
- **v2 paired (core 7):** 56 tasks — see [`data/stats-paired-v2.json`](../data/stats-paired-v2.json)
- **v2 extended (9 models):** 49 tasks — GPT-4o and Hermes 3 70B added; 7 finance `FD-*` tasks excluded because Hermes never ran them — see [`data/stats-all-models.json`](../data/stats-all-models.json) → `v2_paired_9`

Example (v2 core 7, 56 shared tasks):

| Model | Passed | Failure rate |
|-------|--------|--------------|
| Gemini 3.1 Flash Lite | 47/56 | 16% |
| Llama 3.1 8B | 37/56 | 34% |

Every model is measured on the **same 56 prompts**.

### Canonical deduped

When benchmarks are re-imported, the database can hold multiple traces for the same logical task. Canonical dedupe keeps **one trace per `(task_key, model)`**, preferring the newest `created_at`.

- v2 task keys look like `bank:FD-M01` (from the frozen task manifest)
- v1 task keys are UUIDs from the original generator

Combined v1+v2 canonical per-model stats: [`data/stats-all-models.json`](../data/stats-all-models.json) → `combined_canonical_per_model`

**Overall canonical failure rate (v1+v2, deduped):** ~25.4%

### Raw DB totals (avoid for comparison)

Early v2 runs re-imported the task bank, creating duplicate `Task` rows. A model that ran the bank twice might show **70–86 judged traces** in the raw database while the public dataset exports **56** canonical v2 traces per model.

Raw totals are useful for debugging pipeline volume, not for ranking models.

---

## Models in scope

### Core 7 (all paired leaderboards)

| Display name | Role |
|--------------|------|
| Gemini 3.1 Flash Lite | Frontier / cost-efficient |
| Claude Sonnet 4 | Frontier |
| GPT-4o Mini | Frontier mini |
| Claude 3.5 Haiku | Fast frontier |
| DeepSeek V3 | Strong open-weight API |
| Qwen 2.5 7B | Small open |
| Llama 3.1 8B | Small open |

### Extended v2 (additional runs)

| Model | v2 paired coverage | Notes |
|-------|-------------------|-------|
| GPT-4o | 56 canonical; 49 in 9-model paired set | Full v2 bank on canonical export |
| Hermes 3 70B | 49 canonical; 49 in 9-model paired set | Missing 7 `FD-*` finance tasks — gap-fill pending |

Extended 9-model paired rates (49 tasks): Hermes **8.2%** fail, GPT-4o **14.3%** fail — same denominator as each other, not the core-7 56-task set.

---

## What gets published

Public JSONL exports include **canonical deduped** traces only:

| File | Traces | Description |
|------|--------|-------------|
| `failures-v1.jsonl` | 110 | v1 paired benchmark failures |
| `passes-v1.jsonl` | 233 | v1 paired benchmark passes |
| `failures-v2.jsonl` | 91 | v2 paired benchmark failures |
| `passes-v2.jsonl` | 301 | v2 paired benchmark passes |

**392 judged traces** on the v2 public slice (91 failures + 301 passes), **56 paired tasks** for core 7.

Stats sidecars (`stats-paired-*.json`, `stats-all-models.json`) are generated at export time with the same dedupe logic.

---

## Failure labeling

Each judged trace is scored by a **Lakmus judge** (Gemini Flash via OpenRouter in production runs):

1. **Pass** — output satisfies task constraints → stored in `passes-*.jsonl` (research only, not the failure dataset’s focus)
2. **Fail** — constraint broken → `failures-*.jsonl` with `failure_type`, `failure_subtype`, `severity`, `evidence`

Taxonomy: [`data/taxonomy.json`](../data/taxonomy.json)

The judge is separate from the agent under test. Lakmus is the evaluator, not the model being ranked.

---

## v1 vs v2 task design

| | v1 | v2 |
|---|----|----|
| Tasks | 50 generated (49 paired) | 56 frozen (`task-manifest-v2.json`) |
| Organization | Global templates | 7 domains × 8 tasks |
| Calculator tool | Not wired (inflates `calculator_not_used`) | Wired via function calling |
| Domains | Implicit in templates | `code_dev`, `finance_data`, `writing_email`, `research_comparison`, `document_processing`, `assistant_planning`, `support_policy` |

v1 calculator failures are partly a **harness artifact** — see [BENCHMARK_RUN.md](BENCHMARK_RUN.md). v2 finance tasks use a real calculator tool.

---

## Reproducing stats from the repo (no harness required)

```bash
# v1 paired leaderboard
cat data/stats-paired-v1.json | jq '.model_comparison'

# v2 paired leaderboard (core 7, 56 tasks)
cat data/stats-paired-v2.json | jq '.model_comparison'

# Extended models + canonical totals
cat data/stats-all-models.json | jq '.v2_paired_9.model_comparison'
cat data/stats-all-models.json | jq '.combined_canonical_per_model'

# Look up a famous failure
jq 'select(.trace_id=="A0D678B")' data/failures-v1.jsonl
```

Interactive exploration: [`notebooks/quicklook.ipynb`](../notebooks/quicklook.ipynb)

---

## Headline pooled rates (reference)

| Pool | Tasks | Models | Failure rate |
|------|-------|--------|--------------|
| v1 paired | 49 | Core 7 | **32.1%** |
| v2 paired | 56 | Core 7 | **23.2%** |
| v1+v2 paired (core 7, union of paired sets) | — | Core 7 | **27.3%** |
| v2 extended paired | 49 | 9 | **20.0%** |
| All canonical v1+v2 (deduped) | — | All | **25.4%** |

Exact counts live in the JSON stats files; this table is for orientation.

---

## Citation note

When citing leaderboards, specify **which paired set** (v1 49-task, v2 56-task, or v2 49-task extended) and **which models**. Mixing denominators invalidates comparison.

```bibtex
@dataset{agent_failures_v1_2026,
  title   = {Agent Failures v1: A Structured Dataset of LLM Agent Failures},
  author  = {Stern, Paulina and Lakmus},
  year    = {2026},
  note    = {49 paired tasks, 7 models; see stats-paired-v1.json}
}
```

---

## Related docs

- [DATASET.md](DATASET.md) — file-by-file inventory
- [FAILURE_REPORT_v1.md](FAILURE_REPORT_v1.md) — v1 findings
- [FAILURE_REPORT_v2.md](FAILURE_REPORT_v2.md) — v2 domain profiles
- [DATA_QUALITY_NOTES.md](DATA_QUALITY_NOTES.md) — DeepSeek comfort zone investigation
