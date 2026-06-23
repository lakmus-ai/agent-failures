#!/usr/bin/env bash
# Upload Agent Failures v1 to Hugging Face Hub.
# Requires: pip install huggingface_hub datasets
# Auth: huggingface-cli login

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HF_REPO="${HF_REPO:-lakmus/agent-failures-v1}"

echo "Uploading dataset card and JSONL to ${HF_REPO}..."

huggingface-cli upload "${HF_REPO}" \
  "${REPO_ROOT}/huggingface/README.md" README.md \
  --repo-type dataset

huggingface-cli upload "${HF_REPO}" \
  "${REPO_ROOT}/data/failures-v1.jsonl" failures-v1.jsonl \
  --repo-type dataset

huggingface-cli upload "${HF_REPO}" \
  "${REPO_ROOT}/data/passes-v1.jsonl" passes-v1.jsonl \
  --repo-type dataset

huggingface-cli upload "${HF_REPO}" \
  "${REPO_ROOT}/data/stats-paired-v1.json" stats-paired-v1.json \
  --repo-type dataset

huggingface-cli upload "${HF_REPO}" \
  "${REPO_ROOT}/data/taxonomy.json" taxonomy.json \
  --repo-type dataset

echo "Done. View at https://huggingface.co/datasets/${HF_REPO}"
