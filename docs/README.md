# Documentation

Agent Failures — research reports, methodology, and dataset reference.

---

## Start here

| Doc | Audience | Summary |
|-----|----------|---------|
| [**METHODOLOGY.md**](METHODOLOGY.md) | Researchers, reviewers | Paired vs canonical vs raw stats; fair comparison rules |
| [**DATASET.md**](DATASET.md) | ML engineers, dataset users | Every file in `data/`, schemas, examples |
| [../README.md](../README.md) | Everyone | Repo overview and quick start |

---

## Research reports

| Report | Scope |
|--------|-------|
| [**FAILURE_REPORT_v2.md**](FAILURE_REPORT_v2.md) | Domain-organized failure profiles (7 categories, 56 tasks) |
| [**FAILURE_REPORT_v1.md**](FAILURE_REPORT_v1.md) | First benchmark — global findings (49 paired tasks) |
| [**case-studies/COMFORT_ZONE_REVERSION.md**](case-studies/COMFORT_ZONE_REVERSION.md) | DeepSeek trace `A0D678B` — comfort zone reversion |

---

## Data quality & operations

| Doc | Topic |
|-----|-------|
| [**DATA_QUALITY_NOTES.md**](DATA_QUALITY_NOTES.md) | Chinese output in DeepSeek v1 traces |
| [**BENCHMARK_RUN.md**](BENCHMARK_RUN.md) | How benchmarks were run; v1 history and v2 notes |

---

## Publishing

| Doc | Topic |
|-----|-------|
| [**RELEASE_v1.0.0.md**](RELEASE_v1.0.0.md) | v1.0.0 release contents |
| [**PUBLISH.md**](PUBLISH.md) | Hugging Face + GitHub release checklist |
| [**LAUNCH.md**](LAUNCH.md) | Launch copy (HN, X, Reddit) |

---

## Interactive

- [`notebooks/quicklook.ipynb`](../notebooks/quicklook.ipynb) — load JSONL, plot taxonomy, paired leaderboard

---

## Key numbers (reference)

| Pool | Failure rate | File |
|------|--------------|------|
| v1 paired (49 tasks, core 7) | 32.1% | `stats-paired-v1.json` |
| v2 paired (56 tasks, core 7) | 23.2% | `stats-paired-v2.json` |
| v2 extended (49 tasks, 9 models) | 20.0% | `stats-all-models.json` |
| All canonical v1+v2 | 25.4% | `stats-all-models.json` |

Always cite the paired task count when reporting rates — see [METHODOLOGY.md](METHODOLOGY.md).
