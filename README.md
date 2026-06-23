# Agent Failures

**Agents pass demos. They fail in the wild.**

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-agent--failures--v1-yellow)](https://huggingface.co/datasets/lakmus/agent-failures-v1)
[![Release v1.0.0](https://img.shields.io/github/v/release/lakmus-ai/agent-failures?label=v1.0.0)](https://github.com/lakmus-ai/agent-failures/releases/tag/v1.0.0)

A structured dataset and research program on how LLM agents fail — **same tasks, many models**, labeled failures with judge evidence.

Published by **[Lakmus](https://github.com/lakmus-ai)**.

---

## What this is

We run identical agent tasks across multiple LLM APIs, judge each trace against task constraints, and publish **failures with taxonomy labels** (not just pass/fail). The goal is reproducible, comparable failure signal for research, eval, and product hardening.

**Lakmus is the evaluator.** The models under test are commodity agents (Gemini, Claude, GPT, Qwen, Llama, DeepSeek, and others). The benchmark harness is separate from this repo.

| | v1 | v2 |
|---|----|----|
| Tasks | 50 generated → **49 paired** | **56 frozen** (7 domains) |
| Public failures | 110 | 91 |
| Public passes | 233 | 301 |
| Paired failure rate (core 7) | **32%** | **23%** |

Full methodology → [**docs/METHODOLOGY.md**](docs/METHODOLOGY.md) · File reference → [**docs/DATASET.md**](docs/DATASET.md)

---

## Quick start

```bash
# Famous case: DeepSeek comfort zone reversion (trace A0D678B)
jq 'select(.trace_id=="A0D678B")' data/failures-v1.jsonl

# Fair v1 leaderboard (49 identical tasks, 7 models)
jq '.model_comparison' data/stats-paired-v1.json

# Fair v2 leaderboard (56 identical tasks, 7 models)
jq '.model_comparison' data/stats-paired-v2.json

# v2 finance domain failures
jq 'select(.domain=="finance_data")' data/failures-v2.jsonl
```

**Browse:** [Hugging Face v1](https://huggingface.co/datasets/lakmus/agent-failures-v1) · **Notebook:** [`notebooks/quicklook.ipynb`](notebooks/quicklook.ipynb) · **Docs index:** [`docs/README.md`](docs/README.md)

---

## Repository map

### Research reports

| Document | Description |
|----------|-------------|
| [**Failure Report v2**](docs/FAILURE_REPORT_v2.md) | Domain failure profiles — finance, research, docs, code, … |
| [**Failure Report v1**](docs/FAILURE_REPORT_v1.md) | First benchmark — global taxonomy and leaderboard |
| [**Comfort zone case study**](docs/case-studies/COMFORT_ZONE_REVERSION.md) | DeepSeek abandons an English task and writes a Chinese government document |

### Dataset artifacts

| File | Description |
|------|-------------|
| [`data/failures-v1.jsonl`](data/failures-v1.jsonl) | 110 v1 failures (paired benchmark) |
| [`data/passes-v1.jsonl`](data/passes-v1.jsonl) | 233 v1 passes |
| [`data/failures-v2.jsonl`](data/failures-v2.jsonl) | 91 v2 failures |
| [`data/passes-v2.jsonl`](data/passes-v2.jsonl) | 301 v2 passes |
| [`data/stats-paired-v1.json`](data/stats-paired-v1.json) | **Fair v1 leaderboard** — 49 shared tasks |
| [`data/stats-paired-v2.json`](data/stats-paired-v2.json) | **Fair v2 leaderboard** — 56 shared tasks |
| [`data/stats-all-models.json`](data/stats-all-models.json) | All models incl. GPT-4o, Hermes; canonical totals |
| [`data/task-manifest-v2.json`](data/task-manifest-v2.json) | Frozen v2 task bank (56 tasks) |
| [`data/stability-v1.json`](data/stability-v1.json) | Pass@k and reproducibility tiers |
| [`data/taxonomy.json`](data/taxonomy.json) | Failure categories and subtypes |

### Guides

| Document | Description |
|----------|-------------|
| [**METHODOLOGY.md**](docs/METHODOLOGY.md) | Paired vs canonical vs raw — how to compare models fairly |
| [**DATASET.md**](docs/DATASET.md) | Schema, fields, examples for every data file |
| [**DATA_QUALITY_NOTES.md**](docs/DATA_QUALITY_NOTES.md) | DeepSeek Chinese output investigation |

---

## Fair comparison (read this before citing rates)

Public leaderboards use **paired benchmarks**: only tasks where **every** model in the set has exactly one judged trace.

- **Do not** divide failures by raw trace counts (70–86) from partial or duplicate runs.
- **Do** use `stats-paired-v1.json` (49 tasks) or `stats-paired-v2.json` (56 tasks) for core 7.
- **Extended models** (GPT-4o, Hermes): use `stats-all-models.json` → `v2_paired_9` (49 shared tasks).

Duplicate benchmark imports inflated raw DB counts; exports and charts use **canonical dedupe** (one trace per task per model). Details → [METHODOLOGY.md](docs/METHODOLOGY.md).

---

## Headline results

### v2 — 56 shared tasks (core 7)

| Model | Success rate |
|-------|--------------|
| Gemini 3.1 Flash Lite | **84%** (47/56) |
| GPT-4o Mini | **84%** (47/56) |
| Claude Sonnet 4 | **82%** (46/56) |
| DeepSeek V3 | **80%** (45/56) |
| Qwen 2.5 7B | **71%** (40/56) |
| Claude 3.5 Haiku | **70%** (39/56) |
| Llama 3.1 8B | **66%** (37/56) |

v2 adds a real calculator tool and domain-organized tasks — finance failure rates drop vs v1 harness. Full domain breakdown → [FAILURE_REPORT_v2.md](docs/FAILURE_REPORT_v2.md).

### v1 — 49 shared tasks (core 7)

| Model | Success rate |
|-------|--------------|
| Gemini 3.1 Flash Lite | **80%** (39/49) |
| Claude Sonnet 4 | **78%** (38/49) |
| GPT-4o Mini | **78%** (38/49) |
| Claude 3.5 Haiku | **73%** (36/49) |
| DeepSeek V3 | **63%** (31/49) |
| Qwen 2.5 7B | **53%** (26/49) |
| Llama 3.1 8B | **51%** (25/49) |

Top failure modes: constraint violations (43%), wrong tool selection (28%), unsupported claims (19%). Full report → [FAILURE_REPORT_v1.md](docs/FAILURE_REPORT_v1.md).

### Extended models (v2, 49-task 9-model set)

| Model | Success rate | Note |
|-------|--------------|------|
| Hermes 3 70B | **92%** (45/49) | Missing 7 finance `FD-*` tasks |
| GPT-4o | **86%** (42/49) | Same 49-task denominator as Hermes |

---

## v2 task domains

Seven domains × eight tasks each (2 easy, 4 medium, 2 hard):

`code_dev` · `finance_data` · `writing_email` · `research_comparison` · `document_processing` · `assistant_planning` · `support_policy`

Manifest: [`data/task-manifest-v2.json`](data/task-manifest-v2.json)

---

## Failure taxonomy

| Type | Examples |
|------|----------|
| `constraint_violation` | Budget ignored, format ignored, instruction skipped |
| `wrong_tool_selection` | Calculator required but not used |
| `unsupported_claim` | Hallucinated facts, invented citations |
| `goal_drift` | Wrong task, comfort zone reversion, multilingual bleed |
| `tool_failure` | Malformed calls, API errors |
| `other` | Uncategorized |

Full spec → [`data/taxonomy.json`](data/taxonomy.json)

---

## What Lakmus is doing here

Lakmus stress-tests agents on constraint-heavy tasks before shipping its own agent product. This repo is **dataset + research** — the evaluation harness and Lakmus Agent ship separately.

1. **Tasks** — realistic scenarios (extract, summarize, budget, workflows, tools)
2. **Agents tested** — frontier and open models via API
3. **Lakmus judge** — labels *why* a run failed, with evidence
4. **Dataset** — structured records for research, fine-tuning, and eval

---

## Citation

```bibtex
@dataset{agent_failures_v1_2026,
  title   = {Agent Failures v1: A Structured Dataset of LLM Agent Failures},
  author  = {Stern, Paulina and Lakmus},
  year    = {2026},
  publisher = {Lakmus},
  url     = {https://github.com/lakmus-ai/agent-failures},
  note    = {49 paired v1 tasks; see stats-paired-v1.json}
}

@dataset{agent_failures_v2_2026,
  title   = {Agent Failures v2: Domain-Organized LLM Agent Failure Dataset},
  author  = {Stern, Paulina and Lakmus},
  year    = {2026},
  publisher = {Lakmus},
  url     = {https://github.com/lakmus-ai/agent-failures},
  note    = {56 paired v2 tasks; see stats-paired-v2.json}
}
```

---

## License

Dataset and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Links

- **Organization:** [github.com/lakmus-ai](https://github.com/lakmus-ai)
- **Hugging Face:** [lakmus/agent-failures-v1](https://huggingface.co/datasets/lakmus/agent-failures-v1)
- **Documentation:** [docs/README.md](docs/README.md)
- **Lakmus Agent:** coming soon
