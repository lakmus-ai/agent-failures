# Publishing checklist — Agent Failures

## Documentation (current)

| Doc | Purpose |
|-----|---------|
| [README.md](../README.md) | Repo overview |
| [docs/README.md](README.md) | Documentation index |
| [docs/METHODOLOGY.md](METHODOLOGY.md) | Paired vs canonical vs raw stats |
| [docs/DATASET.md](DATASET.md) | File inventory and schemas |
| [docs/FAILURE_REPORT_v2.md](FAILURE_REPORT_v2.md) | v2 domain report |

## 1. Commit public artifacts

```powershell
git add README.md data/ docs/ notebooks/ huggingface/ scripts/
git commit -m "Document v2 benchmark, paired methodology, and extended model stats"
```

Suggested commit includes v2 JSONL, stats sidecars, and new methodology docs.

If tag `v1.0.0` was created on an earlier commit, move it:

```powershell
git tag -d v1.0.0
git tag -a v1.0.0 -F docs/RELEASE_v1.0.0.md
git push origin main
git push origin v1.0.0
```

## 2. GitHub release (v1.0.0)

With [GitHub CLI](https://cli.github.com/):

```powershell
gh release create v1.0.0 --title "Agent Failures v1.0.0" --notes-file docs/RELEASE_v1.0.0.md `
  data/failures-v1.jsonl data/passes-v1.jsonl data/stats-paired-v1.json data/taxonomy.json
```

Or create the release manually on GitHub and attach the four files above.

**v2 on main:** `failures-v2.jsonl`, `passes-v2.jsonl`, `stats-paired-v2.json`, `stats-all-models.json`, `task-manifest-v2.json` — consider a `v2.0.0` tag when ready.

## 3. Hugging Face (v1)

```powershell
$env:HF_TOKEN = "hf_..."   # from https://huggingface.co/settings/tokens
python scripts/upload_hf_dataset.py
```

Or:

```powershell
.\scripts\upload_hf_dataset.ps1
```

## 4. v2 benchmark (if incomplete)

```powershell
cd backend
.\.venv\Scripts\python.exe -m scripts.run_v2_gap_fill --models or-llama-3.1-8b
.\.venv\Scripts\python.exe -m scripts.export_public_dataset --version v2
```

Full clean re-run (392 API calls):

```powershell
.\.venv\Scripts\python.exe -m scripts.run_v2_benchmark
```

## 5. Launch

Draft posts: [`docs/LAUNCH.md`](LAUNCH.md)
