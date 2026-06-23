# Agent Failures v1.0.0

First public release of the Agent Failures dataset and paired benchmark stats.

> **Note:** The repository `main` branch now also includes **v2** artifacts (`failures-v2.jsonl`, `stats-paired-v2.json`, domain reports). This release tag covers **v1 only**. See [DATASET.md](DATASET.md) for the full inventory.

## What's included

| File | Description |
|------|-------------|
| `data/failures-v1.jsonl` | 110 judged failures (paired benchmark) |
| `data/passes-v1.jsonl` | 233 passing traces (paired benchmark) |
| `data/stats-paired-v1.json` | Fair leaderboard — 49 shared tasks, 7 models |
| `data/stats-v1.json` | Full aggregate statistics |
| `data/taxonomy.json` | Failure type definitions |
| `data/task-manifest-v2.json` | Frozen v2 task bank (56 tasks) |
| `docs/FAILURE_REPORT_v1.md` | Research report |

## Paired benchmark (49 shared tasks)

| Model | Success rate |
|-------|--------------|
| Gemini 3.1 Flash Lite | 80% (39/49) |
| Claude Sonnet 4 | 78% (38/49) |
| GPT-4o Mini | 78% (38/49) |
| Claude 3.5 Haiku | 73% (36/49) |
| DeepSeek V3 | 63% (31/49) |
| Qwen 2.5 7B | 53% (26/49) |
| Llama 3.1 8B | 51% (25/49) |

## Quick reproduce

```bash
jq 'select(.trace_id=="A0D678B")' data/failures-v1.jsonl
```

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

## Hugging Face

https://huggingface.co/datasets/lakmus/agent-failures-v1
