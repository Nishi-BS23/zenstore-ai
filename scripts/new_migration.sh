#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"migration message\""
  exit 1
fi

message="$*"
today="$(date +%Y%m%d)"
versions_dir="alembic/versions"

if [[ ! -d "$versions_dir" ]]; then
  echo "Error: $versions_dir directory not found"
  exit 1
fi

max_seq="$(find "$versions_dir" -maxdepth 1 -type f -name "${today}_*.py" \
  | sed -E 's#.*/[0-9]{8}_([0-9]{4})_.*#\1#' \
  | sort \
  | tail -n 1)"

if [[ -z "$max_seq" ]]; then
  next_seq="0001"
else
  next_seq="$(printf "%04d" $((10#$max_seq + 1)))"
fi

rev_id="${today}_${next_seq}"

python_exec="/home/bs00956/Desktop/Personal/zenstore-ai/venv/bin/python"
"$python_exec" -m alembic revision --autogenerate --rev-id "$rev_id" -m "$message"

echo "Created migration with revision id: $rev_id"
