# Create GitHub release v1.0.0 (run after committing public data changes)
#
# Prerequisites: gh auth login, git tag not already on remote
#
#   git add data/ docs/ README.md notebooks/ huggingface/ scripts/
#   git commit -m "Release Agent Failures v1.0.0 with paired benchmark stats"
#   git tag -a v1.0.0 -F docs/RELEASE_v1.0.0.md
#   git push origin main
#   git push origin v1.0.0
#   gh release create v1.0.0 --title "Agent Failures v1.0.0" --notes-file docs/RELEASE_v1.0.0.md `
#     data/failures-v1.jsonl data/passes-v1.jsonl data/stats-paired-v1.json data/taxonomy.json

Write-Host "See comments in this script for release steps."
Write-Host "Release notes: docs/RELEASE_v1.0.0.md"
