"""Upload Agent Failures v1 JSONL + card to Hugging Face Hub.

Usage:
  set HF_TOKEN=hf_...   # or huggingface-cli login / hf auth login
  python scripts/upload_hf_dataset.py

Optional: HF_REPO=lakmus/agent-failures-v1
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HF_REPO = os.environ.get("HF_REPO", "lakmus/agent-failures-v1")

FILES = [
    ("huggingface/README.md", "README.md"),
    ("data/failures-v1.jsonl", "failures-v1.jsonl"),
    ("data/passes-v1.jsonl", "passes-v1.jsonl"),
    ("data/stats-paired-v1.json", "stats-paired-v1.json"),
    ("data/taxonomy.json", "taxonomy.json"),
]


def main() -> int:
    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("Install: pip install huggingface_hub", file=sys.stderr)
        return 1

    token = os.environ.get("HF_TOKEN")
    api = HfApi(token=token)

    try:
        api.create_repo(HF_REPO, repo_type="dataset", exist_ok=True)
    except Exception as exc:
        print(f"create_repo: {exc}", file=sys.stderr)
        return 1

    for local_rel, remote_name in FILES:
        path = REPO_ROOT / local_rel
        if not path.exists():
            print(f"Missing {path}", file=sys.stderr)
            return 1
        print(f"Uploading {remote_name}...")
        api.upload_file(
            path_or_fileobj=str(path),
            path_in_repo=remote_name,
            repo_id=HF_REPO,
            repo_type="dataset",
        )

    print(f"Done: https://huggingface.co/datasets/{HF_REPO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
