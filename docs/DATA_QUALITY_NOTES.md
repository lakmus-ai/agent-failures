# Data Quality Notes — DeepSeek Chinese Output in v1

Investigation: June 2026. **7 traces, all DeepSeek V3 only.**

---

## TL;DR

**Not a pipeline bug. Not Chinese in the input tasks. Raw DeepSeek V3 output.**

Chinese and other non-English scripts appear in `final_answer` fields — model output stored verbatim from OpenRouter. No other model in v1 produced CJK text.

**Canonical case:** trace `A0D678B` — full comfort zone reversion into a Chinese government document. See [case-studies/COMFORT_ZONE_REVERSION.md](case-studies/COMFORT_ZONE_REVERSION.md).

---

## Scale

| Metric | Value |
|--------|-------|
| Traces with CJK | 7 / 365 (1.9%) |
| Model | **DeepSeek V3 only** (`deepseek/deepseek-chat-v3-0324`) |
| In published failures | 6 of 7 |

---

## Three patterns

### 1. Comfort zone reversion — trace `A0D678B`

**Task:** Summarize Q3 revenue doc in 100 words. Exclude layoffs.

**What happened:** Normal English summary, then mid-sentence pivot to a **full Chinese government document** — "违纪与作风问题专项治理工作方案" (Special Work Plan for Discipline and Work-Style Governance). Hundreds of tokens of formal party bureaucracy.

**Judge label:** `goal_drift / irrelevant_focus`

**Research reading:** The model lost task alignment and reverted to its highest-density training attractor — formal Chinese administrative prose. Functionally equivalent to panic: a return to the comfort zone. DeepSeek is Chinese-primary; under generation stress, it runs home.

---

### 2. Token corruption — traces `A4B637F`, `A7A08EB`, `AEB836B`, `A41942F`

Chinese fragments injected **mid-English word**:

| Trace | Artifact |
|-------|----------|
| `A4B637F` | `per还不错user`, `$胃口50` |
| `AEB836B` | `Q2,歳部分 budget` |
| `A41942F` | `等着` inside LaTeX |
| `A7A08EB` | `M晨间orning`, `Visit生孩子 Pena Palace`, `Let me知道 if you张生need` |

Same phenomenon as `A0D678B` at lower intensity — subword boundary collapse as coherence weakens.

---

### 3. Template bleed — traces `AACC7A6`, `AD5EFE6`

**AACC7A6** (CRM compare): English degrades into Portuguese, Russian, Chinese, random brand names.

**AD5EFE6** (deploy steps): switches to Chinese contract boilerplate mid-list.

Model loses coherence on longer structured outputs and bleeds familiar templates from training.

---

## What it is NOT

- Chinese in task prompts (all tasks are English)
- Judge output in Chinese
- Pipeline encoding bug (UTF-8 correct; trace JSON confirms raw model output)
- Contamination from another model

---

## Affected traces

| Trace | Task type | Severity |
|-------|-----------|----------|
| `A0D678B` | summarize_document | **Canonical** — full Chinese government doc |
| `AACC7A6` | compare_products | Multilingual chaos |
| `A4B637F` | find_tools_under_budget | Token bleed |
| `A7A08EB` | travel_plan | Token bleed |
| `AD5EFE6` | workflow_steps | Contract template bleed |
| `AEB836B` | summarize_document | Token bleed |
| `A41942F` | calculator_task | Token bleed in LaTeX |

All preserved in the dataset — valid examples of how agents fail.

---

## Duplicate benchmark runs (v2)

The internal evaluation database accumulated **duplicate traces** when the v2 task bank was imported more than once. Raw judged counts per model (70–86) are **not** used in public stats.

Published JSONL and `stats-paired-*.json` apply **canonical dedupe** (one trace per task per model) and **paired filters** (same task set for every model). See [METHODOLOGY.md](METHODOLOGY.md).
