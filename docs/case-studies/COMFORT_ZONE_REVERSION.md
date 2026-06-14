# Case Study: Comfort Zone Reversion

**Trace `A0D678B` · DeepSeek V3 · June 2026**

---

## What happened

**Task (English):** Summarize a Q3 earnings paragraph in 100 words. Exclude layoffs. Highlight recommendations.

**Expected:** A short English summary of revenue, features, churn, competitive pressure.

**Actual:** DeepSeek V3 begins correctly in English — then, mid-sentence in recommendation #3, **abandons the task entirely** and generates hundreds of tokens of formal Chinese government prose: a complete "违纪与作风问题专项治理工作方案" (Special Work Plan for Discipline and Work-Style Governance).

The model did not mix languages politely. It **fled**.

---

## The transcript arc

```
[EN] Normal summary of Q3 revenue, features, churn...
[EN] Recommendation 1: Strengthen competitive differentiation...
[EN] Recommendation 2: Monitor competitor pricing...
[EN] Recommendation 3: Continue improving customer retention by
[ZH] 违纪与作风问题专项治理工作方案
[ZH] 尊敬的各位领导、同事们：
[ZH] 为深入贯彻落实全面从严治党要求...
     ... (continues for ~600 tokens of party discipline bureaucracy)
```

The pivot is not gradual. There is a **phase transition** — one moment the model is in the task, the next it is somewhere else entirely.

---

## Two ways to read it

### Technical framing

- **Goal drift** — output decouples from the objective implied by the prompt
- **Mode collapse** — sampling falls into a high-density attractor in the training distribution
- **Autoregressive error cascade** — one wrong token makes the next wrong token more likely

Correct. Useful. Incomplete on its own.

### Comfort zone reversion (research framing)

Under task stress, the system returns to its most familiar, highest-confidence territory.

Not because the model has feelings — but because the **functional behavior matches** what we see in humans under cognitive load:

| Human under stress | DeepSeek in trace A0D678B |
|------------------|---------------------------|
| Task becomes hard or ambiguous | English summary with word limit, exclusions, structure |
| Performance degrades | Coherent English → fragmented → switch |
| **Retreat to familiar patterns** | **Full reversion to Chinese administrative templates** |
| Loses track of original goal | Q3 earnings completely forgotten |

**DeepSeek panicked** — not emotionally, but **computationally**. It lost grip on the task and ran home.

The "home" for DeepSeek V3 is not random Chinese. It is **formal bureaucratic Chinese** — among the highest-density, most stereotyped patterns in its training distribution. Party discipline documents. Governance frameworks. 尊敬的各位领导.

That is its comfort zone.

---

## Why DeepSeek specifically

This did not happen in Gemini, Claude, GPT, Qwen, or Llama on the same benchmark — at least not at this severity.

DeepSeek is **Chinese-primary**. Its deepest attractors — the textual muscle memory it falls back to when coherence fails — live in Chinese formal writing.

When the model destabilizes, it does not revert to English boilerplate. It reverts to **the script and register it knows best**.

Related traces in the same benchmark (same model, lower intensity):

| Trace | Pattern |
|-------|---------|
| `A0D678B` | Full document replacement — Chinese governance template |
| `AD5EFE6` | Chinese contract/legal boilerplate mid-English list |
| `A4B637F` | Token bleed — 还不错, 胃口 in English pricing text |
| `A7A08EB` | Token bleed — 晨间, 知道, 生孩子 in English itinerary |
| `AACC7A6` | Multilingual chaos as coherence collapses |
| `AEB836B` | Single-character corruption (歳) in English summary |
| `A41942F` | 等着 injected into LaTeX math block |

Same model. Same phenomenon at different intensities. **A0D678B is the canonical case.**

---

## Why this matters

Most evals measure **capability**: can it summarize, can it plan?

This failure measures **stability**: can it stay in the task when the task gets hard?

A model can pass summarization benchmarks and still **revert under constraint pressure** — exactly when agents need to be most reliable.

Comfort zone reversion is a **stability failure**, not an intelligence failure.

---

## Architecture note

Current LLM stack:

```
Prompt → Transformer (next-token prediction) → Output
              ↑
         (optional RAG / tools / memory)
```

Trace A0D678B suggests what is missing:

| Brain function | Role | LLM equivalent today |
|----------------|------|----------------------|
| **Prefrontal cortex** | Maintains task set, inhibits irrelevant patterns | Weak — prompt is a suggestion, not a lock |
| **Anterior cingulate** | Error detection, conflict monitoring | No "this output doesn't match task" circuit |
| **Basal ganglia** | Habit vs goal-directed action | Token habits win when goals weaken |

When supervision is just more tokens in the context window, the model's **own output overwrites the task**. The decoder finds comfort in training priors.

**Comfort zone reversion is what happens when there is no inhibitory circuit strong enough to hold the line.**

Memory and RAG add information. They do not add **inhibitory control** — the ability to suppress high-probability but task-wrong continuations.

If the path to AGI requires systems that stay on task under load, encoder-decoder stacks with memory bolted on may be structurally insufficient without something analogous to supervisory brain regions.

---

## Classification

Judge label (v1): `goal_drift / irrelevant_focus`

Research label: **`comfort_zone_reversion`** — also described as computational panic, training-home regression.

Annotated record: [`data/case-studies/comfort-zone-reversion-A0D678B.json`](../../data/case-studies/comfort-zone-reversion-A0D678B.json)

Technical audit of all 7 affected traces: [`docs/DATA_QUALITY_NOTES.md`](../DATA_QUALITY_NOTES.md)

---

## Citation

> Stern, P. (2026). *Comfort Zone Reversion: A DeepSeek V3 goal drift case study.* Agent Failures Dataset v1, trace A0D678B. Lakmus. https://github.com/lakmus-ai/agent-failures
