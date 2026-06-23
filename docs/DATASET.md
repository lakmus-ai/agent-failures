# Dataset Guide

Every public artifact in `data/` — what it contains and how to use it.

---

## Quick pick

| Goal | Start here |
|------|------------|
| Fair model leaderboard (v1) | [`stats-paired-v1.json`](../data/stats-paired-v1.json) |
| Fair model leaderboard (v2) | [`stats-paired-v2.json`](../data/stats-paired-v2.json) |
| Include GPT-4o / Hermes | [`stats-all-models.json`](../data/stats-all-models.json) → `v2_paired_9` |
| Train on failures only | [`failures-v1.jsonl`](../data/failures-v1.jsonl) + [`failures-v2.jsonl`](../data/failures-v2.jsonl) |
| Failure + pass for contrastive work | All four `*-v1.jsonl` and `*-v2.jsonl` files |
| Domain breakdown | [`stats-v2-by-domain.json`](../data/stats-v2-by-domain.json) |
| Reproducibility tiers | [`stability-v1.json`](../data/stability-v1.json) |
| Task prompts (v2) | [`task-manifest-v2.json`](../data/task-manifest-v2.json) |
| Failure taxonomy spec | [`taxonomy.json`](../data/taxonomy.json) |

Methodology (paired vs canonical vs raw): [METHODOLOGY.md](METHODOLOGY.md)

---

## Trace files (JSONL)

One JSON object per line. UTF-8. Exported from canonical deduped traces.

### v1 benchmark

| File | Records | Description |
|------|---------|-------------|
| [`failures-v1.jsonl`](../data/failures-v1.jsonl) | 110 | Judged failures on the 49-task paired set |
| [`passes-v1.jsonl`](../data/passes-v1.jsonl) | 233 | Judge-confirmed passes on the same set |

### v2 benchmark

| File | Records | Description |
|------|---------|-------------|
| [`failures-v2.jsonl`](../data/failures-v2.jsonl) | 91 | Failures on the 56-task v2 paired set (core 7) |
| [`passes-v2.jsonl`](../data/passes-v2.jsonl) | 301 | Passes on the same set |

**Combined:** 201 failures, 534 passes across v1+v2 public exports.

### Common fields

| Field | Description |
|-------|-------------|
| `trace_id` | Short ID (e.g. `A0D678B`) — use for citations |
| `task` | Full prompt text |
| `bank_id` | v2 preset ID (e.g. `FD-M01`); null for v1 |
| `domain` | v2 domain slug; v1 inferred from template |
| `template_id` | Task template (e.g. `calculator_task`) |
| `task_version` | `v1.0` or `v2.0` |
| `model_display_name` | Human-readable model name |
| `model_id` | API model ID (OpenRouter) |
| `failed` | `true` in failures files, `false` in passes |
| `final_answer` | Raw model output |

Failures only:

| Field | Description |
|-------|-------------|
| `failure_type` | Top-level category (`constraint_violation`, etc.) |
| `failure_subtype` | Specific mode (`calculator_not_used`, `comfort_zone_reversion`, …) |
| `severity` | `low` / `medium` / `high` |
| `confidence` | Judge confidence 0–1 |
| `evidence` | Structured judge rationale |
| `suggested_fix` | Optional remediation hint |

### Example

```bash
# Comfort zone reversion — canonical research case
jq 'select(.trace_id=="A0D678B")' data/failures-v1.jsonl

# All v2 finance failures
jq 'select(.domain=="finance_data")' data/failures-v2.jsonl

# Count by model
jq -r '.model_display_name' data/failures-v2.jsonl | sort | uniq -c
```

---

## Statistics files (JSON)

### Paired leaderboards (use for rankings)

| File | Paired tasks | Models |
|------|--------------|--------|
| [`stats-paired-v1.json`](../data/stats-paired-v1.json) | 49 | Core 7 |
| [`stats-paired-v2.json`](../data/stats-paired-v2.json) | 56 | Core 7 |

Structure:

```json
{
  "paired_task_count": 56,
  "paired_task_keys": ["bank:CD-E01", "..."],
  "comparison_models": ["Gemini 3.1 Flash Lite", "..."],
  "model_comparison": {
    "Gemini 3.1 Flash Lite": {
      "paired_tasks": 56,
      "passed": 47,
      "failed": 9,
      "success_rate": 0.8393,
      "failure_rate": 0.1607
    }
  },
  "methodology": "Includes only tasks where every comparison model has exactly one judged trace."
}
```

### All-models rollup

[`stats-all-models.json`](../data/stats-all-models.json) — single file for cross-version analysis:

| Key | Contents |
|-----|----------|
| `v1_paired_7` | Same as `stats-paired-v1.json` |
| `v2_paired_7` | Same as `stats-paired-v2.json` |
| `v2_paired_9` | 49-task set including GPT-4o + Hermes |
| `combined_canonical_per_model` | Deduped v1+v2 totals per model |
| `core_7_v1_v2_paired_pool_failure_rate` | Pooled rate across paired v1+v2 (core 7) |
| `all_canonical_v1_v2_failure_rate` | Pooled rate on all canonical traces |

### Domain and aggregate stats

| File | Description |
|------|-------------|
| [`stats-v2-by-domain.json`](../data/stats-v2-by-domain.json) | Failure rates and types per v2 domain |
| [`stats-v1.json`](../data/stats-v1.json) | v1 aggregate (category, severity, templates) |

---

## Task banks

### v2 frozen manifest

[`task-manifest-v2.json`](../data/task-manifest-v2.json) — **56 tasks**, 7 domains × 8 tasks:

```
code_dev, finance_data, writing_email, research_comparison,
document_processing, assistant_planning, support_policy
```

Each entry: `id`, `domain`, `template_id`, `difficulty` (easy/medium/hard), `prompt`, `constraints`, `expected_tools`.

Bank IDs (`CD-E01`, `FD-M03`, …) map to `bank_id` in exported traces.

### Stability study tasks

[`stability-tasks-v1.json`](../data/stability-tasks-v1.json) — 20 frozen prompts for pass@k reproducibility runs.

[`stability-v1.json`](../data/stability-v1.json) — tier estimates (structural fail vs unstable vs stable pass).

---

## Taxonomy and case studies

| File | Description |
|------|-------------|
| [`taxonomy.json`](../data/taxonomy.json) | Failure types, subtypes, descriptions |
| [`case-studies/comfort-zone-reversion-A0D678B.json`](../data/case-studies/comfort-zone-reversion-A0D678B.json) | Structured case record for trace `A0D678B` |

Narrative write-up: [case-studies/COMFORT_ZONE_REVERSION.md](case-studies/COMFORT_ZONE_REVERSION.md)

---

## Hugging Face

Dataset card and upload script: [`huggingface/README.md`](../huggingface/README.md)

Current HF release covers **v1** (110 failures, 233 passes). v2 JSONL is in this repo; HF v2 upload is planned.

---

## Versioning

| Version | Task source | Public traces | Paired N |
|---------|-------------|---------------|----------|
| v1.0.0 | 50 generated tasks | failures-v1 + passes-v1 | 49 |
| v2 (repo) | 56 frozen manifest | failures-v2 + passes-v2 | 56 |

Git tag `v1.0.0` points at the v1-only release. The repo `main` branch includes v2 artifacts.

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — dataset and documentation.
