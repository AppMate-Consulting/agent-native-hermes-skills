#!/usr/bin/env bash
set -euo pipefail

repo="AppMate-Consulting/agent-native-hermes-skills"
category="agent-native"
skills=(visual-plan visual-recap efficient-frontier)

if ! command -v hermes >/dev/null 2>&1; then
  echo "hermes CLI not found on PATH" >&2
  exit 1
fi

for skill in "${skills[@]}"; do
  hermes skills install "${repo}/skills/${skill}" --category "$category" --yes

done

cat <<'MSG'

Installed AppMate Agent-Native Hermes skills.

Next steps inside an active Hermes session:
  /reload-skills

Optional hosted Plan MCP connector:
  hermes mcp add plan --url https://plan.agent-native.com/_agent-native/mcp --auth oauth
  hermes mcp test plan
  /reload-mcp

For private/client work:
  export AGENT_NATIVE_PLANS_MODE=local-files
MSG
