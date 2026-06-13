# Agent Failures Report v1

**How LLM agents break on identical tasks**

Published by [Lakmus](https://github.com/lakmus-ai) · June 2026

---

## Summary

Agents look reliable in demos. Under constraint-heavy tasks, they fail in predictable ways.

We ran **50 identical tasks** across **7 LLM agents** (same prompt, every model) and recorded **365 traces**. Each run was judged for failure type, subtype, severity, and evidence — not just pass/fail.

| Metric | Value |
|--------|-------|
| Traces | 365 |
| Judged failures | 116 (31.8%) |
| Passes | 249 (68.2%) |
| Models | Gemini Flash, Claude Sonnet 4, GPT-4o Mini, Claude Haiku, DeepSeek V3, Qwen 2.5 7B, Llama 3.1 8B |

---

## What Lakmus did here

**Lakmus is the evaluator, not the agent under test.**

1. **Tasks** — realistic agent scenarios: extraction, summarization, budgeting, workflows, tool use
2. **Agents tested** — commodity LLMs via API (OpenRouter)
3. **Lakmus judge** — scores each run against task constraints; labels *why* it failed
4. **Output** — structured failure records for analysis and training

This report is the first public slice. The benchmark harness that produced it is not open-sourced yet. **Lakmus Agent** (open source + Pro) ships separately.

---

## Success rates (same 50 tasks)

| Model | Passed | Rate |
|-------|--------|------|
| Gemini 3.1 Flash Lite | 42/53 | **79%** |
| Claude Sonnet 4 | 39/50 | **78%** |
| GPT-4o Mini | 39/52 | **75%** |
| Claude 3.5 Haiku | 39/52 | **75%** |
| DeepSeek V3 | 33/52 | **64%** |
| Qwen 2.5 7B | 28/52 | **54%** |
| Llama 3.1 8B | 28/52 | **54%** |

Head-to-head on shared prompts:

- Gemini vs Llama: **15–1**
- GPT-4o Mini vs Qwen: **13–1**
- Sonnet vs DeepSeek: **9–2**

Frontier models cluster at ~75–79%. Small open models sit near ~54%.

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

`calculator_task` failures are **partially inflated**. The evaluation setup did not expose a real calculator tool. Models that computed correctly were still flagged as `wrong_tool_selection / calculator_not_used`.

Treat calculator-template results as a **methodology artifact** until tool-calling is wired. Even so, the pattern is informative: agents routinely ignore explicit tool constraints.

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
| [`data/failures-v1.jsonl`](../data/failures-v1.jsonl) | 116 judged failures with taxonomy labels |
| [`data/passes-v1.jsonl`](../data/passes-v1.jsonl) | 249 passing traces for comparison |
| [`data/taxonomy.json`](../data/taxonomy.json) | Failure type + subtype definitions |
| [`data/stats-v1.json`](../data/stats-v1.json) | Aggregate stats and model breakdown |

Each record includes: `trace_id`, `task`, `model_id`, `final_answer`, and for failures: `failure_type`, `failure_subtype`, `severity`, `confidence`, `evidence`.

---

## Citation

```bibtex
@dataset{agent_failures_v1_2026,
  title   = {Agent Failures v1: A Structured Dataset of LLM Agent Failures},
  author  = {Stern, Paulina and Lakmus},
  year    = {2026},
  publisher = {Lakmus},
  url     = {https://github.com/lakmus-ai/agent-failures}
}
```

---

## What's next

- **Lakmus Agent** — open-source agent + Pro tier (built to fail less on constraints)
- **Lakmus Benchmark** — open-source reproduction harness (later)
- **Agent Failures v2** — real tool-calling, larger task set, step-level labels
