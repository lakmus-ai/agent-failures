---
license: cc-by-4.0
task_categories:
  - text-generation
  - question-answering
language:
  - en
tags:
  - agents
  - evaluation
  - failure-analysis
  - llm
  - benchmark
pretty_name: Agent Failures v1
size_categories:
  - n<1K
---

# Agent Failures v1

Structured dataset of **110 labeled LLM agent failures** and **233 passes** from a **49-task paired benchmark** — identical prompts across 7 models.

Published by [Lakmus](https://github.com/lakmus-ai). Full report: [FAILURE_REPORT_v1.md](https://github.com/lakmus-ai/agent-failures/blob/main/docs/FAILURE_REPORT_v1.md).

**v2 data** (56 tasks, domain-organized) is in the GitHub repo: [`failures-v2.jsonl`](https://github.com/lakmus-ai/agent-failures/blob/main/data/failures-v2.jsonl), [`stats-paired-v2.json`](https://github.com/lakmus-ai/agent-failures/blob/main/data/stats-paired-v2.json). HF v2 upload planned.

Methodology: [METHODOLOGY.md](https://github.com/lakmus-ai/agent-failures/blob/main/docs/METHODOLOGY.md)

## Dataset summary

| Split | Records | Description |
|-------|---------|-------------|
| `failures` | 110 | Judged failures with taxonomy labels |
| `passes` | 233 | Judge-confirmed correct runs |

**Paired benchmark:** 49 tasks where Gemini, Claude Sonnet 4, GPT-4o Mini, Claude Haiku, DeepSeek V3, Qwen 2.5 7B, and Llama 3.1 8B each have exactly one judged trace.

## Load in Python

```python
from datasets import load_dataset

ds = load_dataset("lakmus/agent-failures-v1")
print(ds["failures"][0])  # first failure record
```

Or load JSONL directly from the [GitHub release](https://github.com/lakmus-ai/agent-failures/releases/tag/v1.0.0):

```python
import json
from pathlib import Path

failures = [json.loads(line) for line in Path("failures-v1.jsonl").read_text().splitlines() if line]
comfort_zone = next(r for r in failures if r["trace_id"] == "A0D678B")
print(comfort_zone["failure_type"], comfort_zone["task"][:80])
```

## Schema (failures)

| Field | Type | Description |
|-------|------|-------------|
| `trace_id` | string | Unique trace ID (e.g. `A0D678B`) |
| `task` | string | Full task prompt |
| `model_display_name` | string | Model name |
| `model_id` | string | OpenRouter model ID |
| `failed` | bool | Always `true` for this split |
| `failure_type` | string | Top-level taxonomy category |
| `failure_subtype` | string | Specific failure mode |
| `severity` | string | `low`, `medium`, `high` |
| `confidence` | float | Judge confidence 0–1 |
| `evidence` | object | Judge rationale |
| `final_answer` | string | Model output |

Full taxonomy: [taxonomy.json](https://github.com/lakmus-ai/agent-failures/blob/main/data/taxonomy.json)

## Paired leaderboard (49 shared tasks)

| Model | Success rate |
|-------|--------------|
| Gemini 3.1 Flash Lite | 80% |
| Claude Sonnet 4 | 78% |
| GPT-4o Mini | 78% |
| Claude 3.5 Haiku | 73% |
| DeepSeek V3 | 63% |
| Qwen 2.5 7B | 53% |
| Llama 3.1 8B | 51% |

Source: [`stats-paired-v1.json`](https://github.com/lakmus-ai/agent-failures/blob/main/data/stats-paired-v1.json)

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

## Links

- GitHub: https://github.com/lakmus-ai/agent-failures
- Case study (trace A0D678B): https://github.com/lakmus-ai/agent-failures/blob/main/docs/case-studies/COMFORT_ZONE_REVERSION.md
- Quicklook notebook: https://github.com/lakmus-ai/agent-failures/blob/main/notebooks/quicklook.ipynb
