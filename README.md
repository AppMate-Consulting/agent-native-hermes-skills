# AppMate Agent-Native Hermes Skills

AppMate-maintained fork of [`BuilderIO/skills`](https://github.com/BuilderIO/skills), adapted for Hermes Agent.

The upstream skills are excellent agent workflow instructions. This fork keeps the useful planning and recap discipline, but documents the Hermes install path, Hermes MCP setup, and repo-owned local-files workflow we need for client/private work.

## Recommended Hermes install

Install the skills directly from this fork:

```sh
hermes skills install AppMate-Consulting/agent-native-hermes-skills/skills/visual-plan --category agent-native --yes
hermes skills install AppMate-Consulting/agent-native-hermes-skills/skills/visual-recap --category agent-native --yes
hermes skills install AppMate-Consulting/agent-native-hermes-skills/skills/efficient-frontier --category agent-native --yes
```

Or add the repo as a tap first:

```sh
hermes skills tap add AppMate-Consulting/agent-native-hermes-skills
hermes skills install AppMate-Consulting/agent-native-hermes-skills/skills/visual-plan --category agent-native --yes
```

Reload an active Hermes session after installing:

```txt
/reload-skills
```

## Plan MCP connector

Hosted Agent-Native Plans need the Plan MCP connector:

```sh
hermes mcp add plan --url https://plan.agent-native.com/_agent-native/mcp --auth oauth
hermes mcp test plan
```

Then start a fresh session or run:

```txt
/reload-mcp
```

Use hosted mode when the plan/recap can live in Agent-Native's hosted review surface.

## Local-files mode for private/client work

For AppMate client repos and sensitive work, prefer repo-owned local files unless the hosted surface is explicitly approved:

```sh
export AGENT_NATIVE_PLANS_MODE=local-files
```

The agent should write portable plan artifacts under `plans/<slug>/`:

```txt
plans/<slug>/plan.mdx
plans/<slug>/canvas.mdx        # optional
plans/<slug>/prototype.mdx     # optional
plans/<slug>/.plan-state.json  # optional
```

Preview locally with Agent-Native tooling:

```sh
npx @agent-native/core@latest plan local preview --dir plans/<slug> --kind plan
npx @agent-native/core@latest plan local preview --dir plans/<slug> --kind recap
```

Local-files mode prevents plan content from being written to the hosted Plan database. It does **not** make the LLM local; model routing/privacy is controlled by the Hermes profile/provider in use.

## Skills kept from upstream

- `visual-plan` — turn normal implementation plans into structured review artifacts.
- `visual-recap` — turn a branch/PR/diff into a structured review artifact.
- `efficient-frontier` — use the frontier model as orchestrator/reviewer and delegate token-heavy bounded work to cheaper subagents.
- `efficient-fable`, `stay-within-limits`, and `quick-recap` are retained for upstream parity but are not AppMate defaults.

## Upstream sync

Upstream has a small sync script for the Agent-Native visual skills:

```sh
npm run check
npm run sync:agent-native-plan-skills
```

After syncing, re-apply/verify the Hermes-specific sections in this fork before publishing updates.

## License

MIT, inherited from upstream.
