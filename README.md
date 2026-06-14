# Agent Failures

**Agents pass demos. They fail in the wild.**

A structured dataset and research report on how LLM agents fail — same tasks, many models, labeled failures with evidence.

Published by **[Lakmus](https://github.com/lakmus-ai)**.

---

## What's in this repo

| Artifact | Description |
|----------|-------------|
| [**Failure Report v1**](docs/FAILURE_REPORT_v1.md) | Findings: what breaks, which models break most, why it matters |
| [**Case study: Comfort zone reversion**](docs/case-studies/COMFORT_ZONE_REVERSION.md) | DeepSeek V3 abandons an English task and writes a Chinese government document |
| [**DeepSeek output audit**](docs/DATA_QUALITY_NOTES.md) | Technical notes on Chinese text in 7 DeepSeek traces |
| [**Benchmark notes**](docs/BENCHMARK_RUN.md) | Run methodology and internal notes |
| **`data/failures-v1.jsonl`** | 116 judged failures with taxonomy labels |
| **`data/passes-v1.jsonl`** | 249 passing traces (same tasks, for comparison) |
| **`data/taxonomy.json`** | Failure categories and subtypes |
| **`data/case-studies/`** | Annotated research cases (e.g. trace `A0D678B`) |
| **`data/stats-v1.json`** | Model-level success/failure breakdown |

This repo is **dataset + research**. The evaluation harness and Lakmus Agent are not included here — they ship separately.

---

## Headline findings (v1)

50 identical tasks × 7 LLM agents → **365 traces**, **116 failures**.

| Model | Success rate |
|-------|--------------|
| Gemini 3.1 Flash Lite | **79%** |
| Claude Sonnet 4 | **78%** |
| GPT-4o Mini / Claude Haiku | **~75%** |
| DeepSeek V3 | **64%** |
| Qwen 2.5 7B / Llama 3.1 8B | **~54%** |

**Top failure modes:** constraint violations (43%), wrong tool selection (28%), unsupported claims (19%).

Read the full report → [**docs/FAILURE_REPORT_v1.md**](docs/FAILURE_REPORT_v1.md)

---

## What Lakmus is doing here

Lakmus stress-tests agents on constraint-heavy tasks before shipping its own agent product.

In this release:

1. **Tasks** — realistic scenarios (extract, summarize, budget, workflows, tools)
2. **Agents tested** — Gemini, Claude, GPT, Qwen, Llama, DeepSeek
3. **Lakmus judge** — labels *why* a run failed, not just that it failed
4. **Dataset** — structured records for research, fine-tuning, and eval

**Lakmus Agent** (open source + Pro) and the **Lakmus Benchmark** will be released separately.

---

## Failure taxonomy

| Type | Examples |
|------|----------|
| `constraint_violation` | Budget ignored, format ignored, instruction skipped |
| `wrong_tool_selection` | Calculator required but not used |
| `unsupported_claim` | Hallucinated facts, invented citations |
| `goal_drift` | Wrong task, partial completion, lost intent |
| `tool_failure` | Malformed calls, API errors |
| `other` | Uncategorized |

Full spec → [`data/taxonomy.json`](data/taxonomy.json)

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

## License

Dataset and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (recommended — confirm before launch).

---

## Links

- **Organization:** [github.com/lakmus-ai](https://github.com/lakmus-ai)
- **Hugging Face:** coming soon
- **Lakmus Agent:** coming soon
