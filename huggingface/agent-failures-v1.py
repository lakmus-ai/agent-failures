"""Hugging Face dataset loader for Agent Failures v1."""

import json
from pathlib import Path

import datasets


_REPO = "https://raw.githubusercontent.com/lakmus-ai/agent-failures/v1.0.0/data"


def _load_jsonl_url(name: str) -> list[dict]:
    import urllib.request

    url = f"{_REPO}/{name}"
    with urllib.request.urlopen(url) as resp:
        text = resp.read().decode("utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


class AgentFailuresV1(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="default", version=VERSION),
    ]

    def _info(self) -> datasets.DatasetInfo:
        return datasets.DatasetInfo(
            description="Labeled LLM agent failures from a 49-task paired benchmark.",
            features=datasets.Features(
                {
                    "trace_id": datasets.Value("string"),
                    "task_id": datasets.Value("string"),
                    "bank_id": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                    "template_id": datasets.Value("string"),
                    "task_version": datasets.Value("string"),
                    "task": datasets.Value("string"),
                    "model_display_name": datasets.Value("string"),
                    "model_id": datasets.Value("string"),
                    "model_family": datasets.Value("string"),
                    "provider": datasets.Value("string"),
                    "failed": datasets.Value("bool"),
                    "final_answer": datasets.Value("string"),
                    "status": datasets.Value("string"),
                    "created_at": datasets.Value("string"),
                    "failure_type": datasets.Value("string"),
                    "failure_subtype": datasets.Value("string"),
                    "severity": datasets.Value("string"),
                    "confidence": datasets.Value("float64"),
                    "evidence": datasets.Value("string"),
                    "suggested_fix": datasets.Value("string"),
                }
            ),
            homepage="https://github.com/lakmus-ai/agent-failures",
            license="cc-by-4.0",
            citation="""@dataset{agent_failures_v1_2026,
  title   = {Agent Failures v1: A Structured Dataset of LLM Agent Failures},
  author  = {Stern, Paulina and Lakmus},
  year    = {2026},
  publisher = {Lakmus},
  url     = {https://github.com/lakmus-ai/agent-failures}
}""",
        )

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"split": "failures"},
            ),
            datasets.SplitGenerator(
                name="passes",
                gen_kwargs={"split": "passes"},
            ),
        ]

    def _generate_examples(self, split: str):
        local_data = Path(__file__).resolve().parent.parent / "data"
        local_file = local_data / f"{split}-v1.jsonl"
        if local_file.exists():
            rows = [json.loads(line) for line in local_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        else:
            rows = _load_jsonl_url(f"{split}-v1.jsonl")

        for idx, row in enumerate(rows):
            yield idx, {
                "trace_id": row.get("trace_id") or "",
                "task_id": row.get("task_id") or "",
                "bank_id": row.get("bank_id") or "",
                "domain": row.get("domain") or "",
                "template_id": row.get("template_id") or "",
                "task_version": row.get("task_version") or "",
                "task": row.get("task") or "",
                "model_display_name": row.get("model_display_name") or "",
                "model_id": row.get("model_id") or "",
                "model_family": row.get("model_family") or "",
                "provider": row.get("provider") or "",
                "failed": bool(row.get("failed", split == "failures")),
                "final_answer": row.get("final_answer") or "",
                "status": row.get("status") or "",
                "created_at": row.get("created_at") or "",
                "failure_type": row.get("failure_type") or "",
                "failure_subtype": row.get("failure_subtype") or "",
                "severity": row.get("severity") or "",
                "confidence": float(row.get("confidence") or 0.0),
                "evidence": json.dumps(row.get("evidence") or ""),
                "suggested_fix": row.get("suggested_fix") or "",
            }
