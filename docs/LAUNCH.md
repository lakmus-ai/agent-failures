# Launch burst — Agent Failures v1

Draft posts for Show HN, X, and r/LocalLLaMA. Link to **dataset first**, story second.

**Primary links:**
- Hugging Face: https://huggingface.co/datasets/lakmus/agent-failures-v1
- GitHub: https://github.com/lakmus-ai/agent-failures
- Notebook: https://github.com/lakmus-ai/agent-failures/blob/main/notebooks/quicklook.ipynb
- Case study: https://github.com/lakmus-ai/agent-failures/blob/main/docs/case-studies/COMFORT_ZONE_REVERSION.md

**First comment / pinned repro:**
```bash
jq 'select(.trace_id=="A0D678B")' data/failures-v1.jsonl
```

---

## Show HN

**Title:** Agent Failures v1 — 110 labeled agent failures, 49 shared tasks, JSONL

**Post body:**

We benchmarked 7 LLM agents on 50 identical constraint-heavy tasks and published every judged failure with taxonomy labels (not just pass/fail).

**What's in the release:**
- 110 failures + 233 passes on the **49-task paired set** (every model judged on the same prompts)
- Failure types: constraint violations, wrong tool use, hallucinated facts, goal drift
- Paired leaderboard: Gemini 80%, Sonnet/GPT-4o Mini 78%, Llama 51% on identical tasks
- JSONL + Hugging Face + quicklook notebook

**Links:**
- Dataset (HF): https://huggingface.co/datasets/lakmus/agent-failures-v1
- Repo: https://github.com/lakmus-ai/agent-failures
- Notebook: https://github.com/lakmus-ai/agent-failures/blob/main/notebooks/quicklook.ipynb

**Reproduce the viral DeepSeek trace in one command:**
```bash
jq 'select(.trace_id=="A0D678B")' data/failures-v1.jsonl
```
(English summary task → model writes a Chinese government discipline document mid-sentence)

Happy to answer methodology questions. v2 with real calculator tool + 56 domain tasks is next.

---

## X thread

**Tweet 1 (hook + chart):**
We ran 7 models on 49 identical agent tasks.

Same prompts. Judged failures with evidence — not vibes.

Paired success rates:
• Gemini Flash 80%
• Sonnet / GPT-4o Mini 78%
• DeepSeek 63%
• Llama 3.1 8B 51%

Download 110 labeled failures ↓

**Tweet 2:**
Most failures aren't random. Top modes on 49 shared tasks:
→ constraint violations (43%)
→ wrong tool selection (28%)
→ hallucinated facts (19%)

**Tweet 3:**
DeepSeek trace A0D678B: asked for a 100-word English earnings summary.

Mid-sentence it abandons the task and generates a full Chinese government discipline document.

Goal drift → comfort zone reversion.

**Tweet 4:**
Reproduce in one line:
```
jq 'select(.trace_id=="A0D678B")' data/failures-v1.jsonl
```

**Tweet 5 (CTA):**
Full dataset:
🤗 https://huggingface.co/datasets/lakmus/agent-failures-v1
📦 https://github.com/lakmus-ai/agent-failures
📓 quicklook notebook included

Case study pinned: Comfort Zone Reversion (A0D678B)

---

## r/LocalLLaMA

**Title:** Small models hallucinate pricing on the same tasks — 49-task paired benchmark (JSONL)

**Body:**

We published **Agent Failures v1** — same agent tasks run across Gemini, Claude, GPT-4o Mini, DeepSeek, Qwen 2.5 7B, and Llama 3.1 8B. Only tasks where **all 7 models** have a judged trace (49 prompts).

**Paired results (identical prompts):**
| Model | Success |
|-------|---------|
| Gemini 3.1 Flash Lite | 80% (39/49) |
| Claude Sonnet 4 | 78% |
| GPT-4o Mini | 78% |
| DeepSeek V3 | 63% |
| Qwen 2.5 7B | 53% |
| Llama 3.1 8B | 51% |

Llama and Qwen lose hardest on budget-constrained "find tools under $X" and calculator tasks. Frontier models cluster ~75–80% but still fail on constraints.

**Get the data:**
- JSONL: https://github.com/lakmus-ai/agent-failures/releases/tag/v1.0.0
- Hugging Face: https://huggingface.co/datasets/lakmus/agent-failures-v1
- Jupyter quicklook: `notebooks/quicklook.ipynb`

Each failure has `failure_type`, `failure_subtype`, judge evidence, and full model output.

Not a leaderboard post — it's labeled failure traces for eval/fine-tuning research. CC BY 4.0.

---

## LinkedIn (optional)

Same as Tweet 1–5 but prose format. Lead with "49 identical prompts, 7 models" and link HF dataset.

---

## First-comment checklist (Show HN)

- [ ] HF dataset link
- [ ] Notebook link
- [ ] jq one-liner for A0D678B
- [ ] Clarify paired N = 49 (1 task missing judged trace for one model)
- [ ] Calculator caveat for v1 (no real tool until v2)
