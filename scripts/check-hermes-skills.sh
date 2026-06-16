#!/usr/bin/env bash
set -euo pipefail

for skill_md in skills/*/SKILL.md; do
  [[ -f "$skill_md" ]] || continue
  if ! head -n 1 "$skill_md" | grep -qx -- '---'; then
    echo "$skill_md: missing opening frontmatter fence" >&2
    exit 1
  fi
  if ! awk 'NR>1 && $0 == "---" { found=1; exit } END { exit found ? 0 : 1 }' "$skill_md"; then
    echo "$skill_md: missing closing frontmatter fence" >&2
    exit 1
  fi
  frontmatter="$(awk 'NR>1 { if ($0 == "---") exit; print }' "$skill_md")"
  grep -q '^name:' <<<"$frontmatter" || { echo "$skill_md: missing name" >&2; exit 1; }
  grep -q '^description:' <<<"$frontmatter" || { echo "$skill_md: missing description" >&2; exit 1; }
  name="$(grep '^name:' <<<"$frontmatter" | head -n1 | sed 's/^name:[[:space:]]*//')"
  if [[ ! "$name" =~ ^[a-z0-9][a-z0-9_-]*$ ]]; then
    echo "$skill_md: invalid Hermes skill name: $name" >&2
    exit 1
  fi
  echo "OK $skill_md"
done

bash -n scripts/install-hermes-skills.sh
python -m py_compile __init__.py agent_native_cli.py
python - <<'PY'
from pathlib import Path
manifest = Path('plugin.yaml')
text = manifest.read_text()
for required in ['name: agent-native-hermes-skills', 'version:', 'description:']:
    if required not in text:
        raise SystemExit(f'plugin.yaml missing {required!r}')
print('OK plugin.yaml')
PY
