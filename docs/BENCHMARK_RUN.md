# Lakmus V1 — First Benchmark Run

Handoff notes from the first real multi-model benchmark (June 13, 2026). Use this to pick up tomorrow without re-reading the whole session.

## What we built

**Lakmus Failure Forge V1** — automated pipeline:

```
Task Generator → Agent Runner → Trace Logger → Failure Judge → Dataset Writer → Dashboard
```

- **Backend:** FastAPI + SQLite (`backend/data/lakmus.db`)
- **Frontend:** Next.js dashboard
- **Agents:** OpenRouter (cloud) + Ollama (local)
- **Judge:** Gemini 3.1 Flash Lite via OpenRouter (cheap, consistent)
- **Run modes:**
  - `benchmark` (default) — same N tasks on every selected model (fair comparison)
  - `quick` — round-robin, fewer total calls, for dev

## This run

| Setting | Value |
|---------|-------|
| Mode | `benchmark` |
| Tasks | 50 (× 7 cloud models) |
| Models | Gemini Flash, Sonnet 4, GPT-4o Mini, Haiku, DeepSeek V3, Qwen 2.5 7B, Llama 3.1 8B |
| Duration | ~2 hours (02:21 → 04:22 UTC) |
| Real traces | **365** |
| Judged failures | **116** (~31.8%) |
| Passes | **249** (~68.2%) |

Shared head-to-head tasks: **50** prompts run on all 7 cloud models.

## Success leaderboard (after cleanup)

| Model | Passed | Rate |
|-------|--------|------|
| Gemini 3.1 Flash Lite | 42/53 | **79%** |
| Claude Sonnet 4 | 39/50 | **78%** |
| GPT-4o Mini | 39/52 | **75%** |
| Claude 3.5 Haiku | 39/52 | **75%** |
| DeepSeek V3 | 33/52 | **64%** |
| Qwen 2.5 7B | 28/52 | **54%** |
| Llama 3.1 8B | 28/52 | **54%** |

Same-task wins (50 shared prompts):

- Gemini vs Llama: **15–1**
- GPT-4o Mini vs Qwen: **13–1**
- Sonnet vs DeepSeek: **9–2**

## Failure taxonomy (what broke)

| Type | Count | Share |
|------|-------|-------|
| `constraint_violation` | 50 | 43% |
| `wrong_tool_selection` | 33 | 28% |
| `unsupported_claim` | 22 | 19% |
| `goal_drift` | 10 | 9% |

Top subtypes:

1. **`calculator_not_used`** (33) — task says “use calculator”; model does mental math
2. **`hallucinated_fact`** (22) — invented pricing, sources, etc.
3. **`budget_ignored`** (19)
4. **`instruction_ignored`** (18)
5. **`format_ignored`** (13)

### Failure rate by task template

| Template | Fail rate | Notes |
|----------|-----------|-------|
| `calculator_task` | **94%** | Dominates failures — see caveat below |
| `find_tools_under_budget` | 49% | Models hallucinate SaaS pricing |
| `extract_field` | 31% | |
| `summarize_document` | 30% | |
| `compare_products` | 26% | |
| `travel_plan` | 22% | |
| `workflow_steps` | **3%** | Models handle these well |

**11 tasks failed for every model** — almost all calculator or “find tools under $X/month” prompts.

## Critical caveat: calculator failures are inflated

The pipeline **does not wire up a real calculator tool**. Models that compute correctly still get flagged as `wrong_tool_selection / calculator_not_used`.

Until tool-calling is implemented, treat `calculator_task` results as **judge artifact**, not pure model incompetence. This single template accounts for ~30% of all failures.

## Cleanup done (end of session)

1. **Mock data wiped** — 4 test traces from `test_benchmark_mode.py` removed (DB + JSON files)
   ```bash
   cd backend && python scripts/wipe_data.py --mock-only
   ```
2. **Stuck Llama trace re-judged** — `A36B1FF` (A/B workflow task) → **PASSED**
   ```bash
   cd backend && python scripts/rejudge_trace.py A36B1FF
   ```

### Known leftover anomaly (intentionally left)

- **GPT-4o Mini `A25E148`** — status `failed` (API error on same A/B workflow task). Not re-run.

## Infrastructure (current)

| Service | URL |
|---------|-----|
| API | `http://localhost:8002/api/v1` |
| Dashboard | `http://localhost:3000` |
| DB | `backend/data/lakmus.db` |
| Trace JSON | `backend/data/traces/*.json` |

Frontend env: `frontend/.env.local` → `NEXT_PUBLIC_API_URL=http://localhost:8002/api/v1`

**Windows note:** stale uvicorn processes can ghost ports 8000/8001. Backend was moved to **8002** to avoid this.

## Useful scripts

```bash
cd backend
set PYTHONPATH=.

python scripts/analyze_run.py          # leaderboard + failure breakdown
python scripts/show_success_rates.py   # pass/fail by model
python scripts/wipe_data.py --mock-only
python scripts/rejudge_trace.py <ID>
```

## Dataset value (honest take)

**What’s real signal:**

- Clear frontier vs small-model gap on identical prompts
- Constraint-following and hallucination patterns differ by model family
- Workflow-style tasks are nearly solved; extraction/summarization are moderate

**What needs work before publishing:**

- Implement real tool-calling (calculator at minimum)
- Filter or re-tag calculator false positives
- Export clean JSONL (passes + failures, benchmark-only slice)
- Optional: step-level failure labels, validation loop

**Rough inventory after cleanup:** ~116 failure records + ~249 pass traces for comparison.

## Suggested next steps (tomorrow)

1. **Wire calculator tool** — biggest impact on dataset quality
2. **Export benchmark slice** — 50 tasks × 7 models, JSONL or HuggingFace format
3. **Dashboard polish** — run progress indicator, filter mock (done in DB), completion toast
4. **README / research write-up** — reproduction guide, taxonomy, first Failure Report draft
5. **Rotate OpenRouter API key** — was shared in chat during setup

## Key files

```
backend/app/services/pipeline.py       # benchmark vs quick
backend/app/services/failure_judge.py  # judge prompt + taxonomy
backend/app/agents/catalog.py          # models + cost estimates
backend/app/services/dataset_writer.py # stats, passes, failures
frontend/app/page.tsx                  # run UI + model picker
docs/RUNNING.md                        # operational guide
```
