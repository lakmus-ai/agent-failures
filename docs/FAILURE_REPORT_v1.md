# Agent Failures Report v1

**How LLM agents break on identical tasks**

Published by [Lakmus](https://github.com/lakmus-ai) · June 2026

---

## Summary

Agents look reliable in demos. Under constraint-heavy tasks, they fail in predictable ways.

We ran **50 identical tasks** across **7 LLM agents** (same prompt, every model) and recorded **343 judged traces** on the **49-task paired benchmark** — tasks where every model has exactly one judged run. Each run was judged for failure type, subtype, severity, and evidence — not just pass/fail.

| Metric | Value |
|--------|-------|
| Paired benchmark tasks | **49** (all 7 models judged) |
| Published failures | 110 |
| Published passes | 233 |
| Models | Gemini Flash, Claude Sonnet 4, GPT-4o Mini, Claude Haiku, DeepSeek V3, Qwen 2.5 7B, Llama 3.1 8B |

> **Fair comparison:** Public leaderboards use **paired success rate** only — same tasks, all models. Raw per-model totals (uneven trace counts from partial runs or duplicate imports) are omitted. See [`data/stats-paired-v1.json`](../data/stats-paired-v1.json) and [METHODOLOGY.md](METHODOLOGY.md).

---

## What Lakmus did here

**Lakmus is the evaluator, not the agent under test.**

1. **Tasks** — realistic agent scenarios: extraction, summarization, budgeting, workflows, tool use
2. **Agents tested** — commodity LLMs via API (OpenRouter)
3. **Lakmus judge** — scores each run against task constraints; labels *why* it failed
4. **Output** — structured failure records for analysis and training

This report is the first public slice. The benchmark harness that produced it is not open-sourced yet. **Lakmus Agent** (open source + Pro) ships separately.

---

## Success rates (49 shared tasks)

| Model | Passed | Paired success rate |
|-------|--------|---------------------|
| Gemini 3.1 Flash Lite | 39/49 | **80%** |
| Claude Sonnet 4 | 38/49 | **78%** |
| GPT-4o Mini | 38/49 | **78%** |
| Claude 3.5 Haiku | 36/49 | **73%** |
| DeepSeek V3 | 31/49 | **63%** |
| Qwen 2.5 7B | 26/49 | **53%** |
| Llama 3.1 8B | 25/49 | **51%** |

Head-to-head on the same 49 prompts:

- Gemini vs Llama: **15–1** (33 ties)
- GPT-4o Mini vs Qwen: **13–1** (35 ties)
- Sonnet vs DeepSeek: **9–2** (38 ties)

Frontier models cluster at ~73–80%. Small open models sit near ~51–53%.

---

## How agents fail

### By failure type

| Type | Count | Share |
|------|-------|-------|
| `constraint_violation` | 50 | 43% |
| `wrong_tool_selection` | 33 | 28% |
| `unsupported_claim` | 22 | 19% |
| `goal_drift` | 10 | 9% |

### Top subtypes

1. **`calculator_not_used`** (33) — task required calculator; model computed in text
2. **`hallucinated_fact`** (22) — invented pricing, facts, sources
3. **`budget_ignored`** (19) — ignored explicit budget caps
4. **`instruction_ignored`** (18) — skipped explicit instructions
5. **`format_ignored`** (13) — wrong output format

### By task template

| Template | Failure rate |
|----------|--------------|
| `calculator_task` | **94%** |
| `find_tools_under_budget` | 49% |
| `extract_field` | 31% |
| `summarize_document` | 30% |
| `compare_products` | 26% |
| `travel_plan` | 22% |
| `workflow_steps` | **3%** |

**11 tasks failed for every model** — almost all calculator or “find SaaS tools under $X/month” prompts.

---

## Important caveat

`calculator_task` failures are **partially inflated**. The v1 evaluation setup did not expose a real calculator tool. Models that computed correctly were still flagged as `wrong_tool_selection / calculator_not_used`.

Treat calculator-template results as a **methodology artifact** until tool-calling is wired (fixed in v2). Even so, the pattern is informative: agents routinely ignore explicit tool constraints.

---

## What this means

**Real signal**

- Constraint-following separates frontier from small models more than fluency
- Hallucinated pricing/facts dominate “research-like” tasks
- Workflow planning is largely solved; constrained extraction and budgeting are not

**Not surprising, but under-documented**

- Failures are **typed and repeatable**, not random
- Same-task comparison exposes model gaps that aggregate benchmarks hide

---

## Dataset

| File | Description |
|------|-------------|
| [`data/failures-v1.jsonl`](../data/failures-v1.jsonl) | Judged failures on paired benchmark (110 records) |
| [`data/passes-v1.jsonl`](../data/passes-v1.jsonl) | Passing traces on paired benchmark (233 records) |
| [`data/stats-paired-v1.json`](../data/stats-paired-v1.json) | **Fair leaderboard** — 49 shared tasks |
| [`data/taxonomy.json`](../data/taxonomy.json) | Failure type + subtype definitions |
| [`data/stats-v1.json`](../data/stats-v1.json) | Full aggregate stats (includes unpaired traces) |

Each record includes: `trace_id`, `task`, `model_id`, `final_answer`, and for failures: `failure_type`, `failure_subtype`, `severity`, `confidence`, `evidence`.

**Reproduce a famous failure:**

```bash
jq 'select(.trace_id=="A0D678B")' data/failures-v1.jsonl
```

Browse on [Hugging Face](https://huggingface.co/datasets/lakmus/agent-failures-v1) · Quick start: [`notebooks/quicklook.ipynb`](../notebooks/quicklook.ipynb)

---

## Citation

```bibtex
@dataset{agent_failures_v1_2026,
  title   = {Agent Failures v1: A Structured Dataset of LLM Agent Failures},
  author  = {Stern, Paulina and Lakmus},
  year    = {2026},
  publisher = {Lakmus},
  url     = {https://github.com/lakmus-ai/agent-failures},
  note    = {49 paired benchmark tasks, 7 models}
}
```

---

## What's next

- **Lakmus Agent** — open-source agent + Pro tier (built to fail less on constraints)
- **Lakmus Benchmark** — open-source reproduction harness (later)
- **Agent Failures v2** — real tool-calling, 56 frozen tasks, domain breakdown
