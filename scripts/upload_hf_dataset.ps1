# Upload Agent Failures v1 to Hugging Face Hub.
# Requires: pip install huggingface_hub
# Auth: huggingface-cli login

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$HfRepo = if ($env:HF_REPO) { $env:HF_REPO } else { "lakmus/agent-failures-v1" }

Write-Host "Uploading to $HfRepo..."

huggingface-cli upload $HfRepo "$RepoRoot\huggingface\README.md" README.md --repo-type dataset
huggingface-cli upload $HfRepo "$RepoRoot\data\failures-v1.jsonl" failures-v1.jsonl --repo-type dataset
huggingface-cli upload $HfRepo "$RepoRoot\data\passes-v1.jsonl" passes-v1.jsonl --repo-type dataset
huggingface-cli upload $HfRepo "$RepoRoot\data\stats-paired-v1.json" stats-paired-v1.json --repo-type dataset
huggingface-cli upload $HfRepo "$RepoRoot\data\taxonomy.json" taxonomy.json --repo-type dataset

Write-Host "Done. https://huggingface.co/datasets/$HfRepo"
