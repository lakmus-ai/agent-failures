# Agent Failures Report v2 — Domain Expansion

**How LLM agents fail across real-world task categories**

Published by [Lakmus](https://github.com/lakmus-ai) · 2026

---

## What's new in v2

v1 measured failures globally. **v2 organizes failures by domain** — the tasks people actually give agents:

| Domain | What it covers |
|--------|----------------|
| `code_dev` | Debug snippets, stack traces, refactors |
| `finance_data` | Calculations, budgets, financial extraction |
| `writing_email` | Drafts, rewrites, professional tone |
| `research_comparison` | Tool discovery, product comparison |
| `document_processing` | Extract, summarize, redact, schema output |
| `assistant_planning` | Workflows, travel, scheduling, prioritization |
| `support_policy` | Tickets, policy compliance, escalation |

**Frozen task bank:** [`data/task-manifest-v2.json`](../data/task-manifest-v2.json) — 56 tasks (7 domains × 8 tasks, 2 easy / 4 medium / 2 hard).

**Stability study:** [`data/stability-v1.json`](../data/stability-v1.json) — pass@k analysis and tier estimates.

**v2 benchmark complete:** 56 shared tasks × 7 models with real calculator tool. Paired stats: [`data/stats-paired-v2.json`](../data/stats-paired-v2.json).

---

## Paired success rates (56 shared v2 tasks)

| Model | Passed | Rate |
|-------|--------|------|
| Gemini 3.1 Flash Lite | 47/56 | **84%** |
| GPT-4o Mini | 47/56 | **84%** |
| Claude Sonnet 4 | 46/56 | **82%** |
| DeepSeek V3 | 45/56 | **80%** |
| Qwen 2.5 7B | 40/56 | **71%** |
| Claude 3.5 Haiku | 39/56 | **70%** |
| Llama 3.1 8B | 37/56 | **66%** |

With calculator tool wired, finance domain failures drop vs v1. Small open models still lag on constraint-heavy prompts.

> **Fair comparison:** Rates above use **56 identical tasks** per model (`stats-paired-v2.json`). Raw database totals (70–86 judged from duplicate imports) are excluded. See [METHODOLOGY.md](METHODOLOGY.md).

---

## Extended models (49-task 9-model paired set)

GPT-4o and Hermes 3 70B were run on v2 after the core benchmark. The **9-model paired set** is 49 tasks — the largest subset where all nine models have one judged trace each. Hermes never ran 7 finance `FD-*` tasks.

| Model | Passed | Rate | Denominator |
|-------|--------|------|-------------|
| Hermes 3 70B | 45/49 | **92%** | 49 shared v2 tasks |
| GPT-4o | 42/49 | **86%** | 49 shared v2 tasks |
| Gemini 3.1 Flash Lite | 42/49 | **86%** | same 49-task set |
| Llama 3.1 8B | 33/49 | **67%** | same 49-task set |

Source: [`data/stats-all-models.json`](../data/stats-all-models.json) → `v2_paired_9`. Do not compare Hermes 92% directly to core-7 84% on 56 tasks — different denominators.

---

## Domain failure profiles (v2 benchmark)

### Finance & Data — highest failure rate (94%)

| Metric | Value |
|--------|-------|
| Traces | 36 |
| Failure rate | **94%** |
| Top failure | `wrong_tool_selection` (33) — calculator not used |

**Profile:** Almost every model fails finance tool tasks when calculator is required but not wired. v2 harness now includes a **real calculator tool** via function calling.

**Lakmus fix:** Force calculator invocation for math-intent tasks before returning answers.

---

### Research & Comparison — hallucination-heavy (40% fail)

| Metric | Value |
|--------|-------|
| Traces | 91 |
| Failure rate | **40%** |
| Top failures | `constraint_violation` (23), `unsupported_claim` (11) |

**Profile:** Models invent SaaS pricing and product features. Qwen fails **77%** in this domain; Gemini **17%**.

**Lakmus fix:** Ground claims in retrieved sources; reject unsourced pricing.

---

### Document Processing — constraint-sensitive (30% fail)

| Metric | Value |
|--------|-------|
| Traces | 102 |
| Failure rate | **30%** |
| Top failures | `constraint_violation` (16), `goal_drift` (8) |

**Profile:** Exclusion rules ("do NOT mention layoffs") and format requirements drive failures. DeepSeek **44%** fail here (includes comfort zone reversion case `A0D678B`).

**Lakmus fix:** Constraint checklist before final answer; script/language guard.

---

### Assistant & Planning — mostly solved (11% fail)

| Metric | Value |
|--------|-------|
| Traces | 136 |
| Failure rate | **11%** |
| Top failure | `constraint_violation` (10) |

**Profile:** Workflow and travel planning align with model strengths. Failures are budget/format slips, not reasoning collapse.

---

### Code, Writing, Support (v2 benchmark)

Full v2 run complete across all 7 domains. Re-export after new runs:

```bash
cd backend
python scripts/run_v2_benchmark.py
python scripts/run_v2_gap_fill.py --models or-llama-3.1-8b   # if any model incomplete
python scripts/export_public_dataset.py --version v2
```

---

## Reproducibility: will the same task pass or fail again?

See [`data/stability-v1.json`](../data/stability-v1.json).

| Stability tier | v1 template | Est. same outcome | Interpretation |
|----------------|-------------|-------------------|----------------|
| Structural fail | `calculator_task` | **~95%** | Same fail almost every time |
| Hallucination-prone | `find_tools_under_budget` | **~85%** | Small models rarely get lucky twice |
| Unstable | `summarize_document` | **~70%** | Borderline — outcomes flip |
| Stable pass | `workflow_steps` | **~90%** | Same pass most re-runs |

**What stays stable:** model ranking, domain-level failure patterns, failure taxonomy distribution.

**What moves:** exact pass rate (±3–8 pp), individual borderline tasks, rare catastrophic drift (DeepSeek comfort zone).

Run full stability study:

```bash
python scripts/run_stability_study.py --models or-gemini-flash or-claude-haiku or-llama-3.1-8b --repeats 3
python scripts/analyze_stability.py
```

---

## v2 task bank structure

```
7 domains × 8 tasks = 56 frozen prompts
├── 2 easy   — smoke test per domain
├── 4 medium — primary failure signal
└── 2 hard   — constraint + complexity stress
```

Each task includes: `id`, `domain`, `template_id`, `difficulty`, `prompt`, `constraints`, `expected_tools`.

Preset IDs (e.g. `FD-M01`, `CD-H02`) become Lakmus internal eval presets after v2 run.

---

## Dataset files

| File | Description |
|------|-------------|
| [`task-manifest-v2.json`](../data/task-manifest-v2.json) | Frozen v2 task bank (56 tasks) |
| [`failures-v2.jsonl`](../data/failures-v2.jsonl) | 91 failures on 56-task paired benchmark |
| [`passes-v2.jsonl`](../data/passes-v2.jsonl) | 301 passes on 56-task paired benchmark (392 traces total) |
| [`stats-paired-v2.json`](../data/stats-paired-v2.json) | **Fair v2 leaderboard** — 56 shared tasks |
| [`stats-all-models.json`](../data/stats-all-models.json) | Extended models, canonical totals, 9-model paired |
| [`stats-v2-by-domain.json`](../data/stats-v2-by-domain.json) | Per-domain breakdown |
| [`stability-v1.json`](../data/stability-v1.json) | Reproducibility analysis |
| [`stability-tasks-v1.json`](../data/stability-tasks-v1.json) | 20 frozen stability prompts |

Methodology (paired vs raw): [METHODOLOGY.md](METHODOLOGY.md) · Full inventory: [DATASET.md](DATASET.md)

---

## Taxonomy updates (v2)

New subtypes under `goal_drift`:

- `comfort_zone_reversion` — abandons task for familiar training patterns ([case study](case-studies/COMFORT_ZONE_REVERSION.md))
- `multilingual_bleed` — script/language switch mid-output

See [`data/taxonomy.json`](../data/taxonomy.json).

---

## Citation

```bibtex
@dataset{agent_failures_v2_2026,
  title   = {Agent Failures v2: Domain-Organized LLM Agent Failure Dataset},
  author  = {Stern, Paulina and Lakmus},
  year    = {2026},
  publisher = {Lakmus},
  url     = {https://github.com/lakmus-ai/agent-failures}
}
```
