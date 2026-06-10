# visual-recap

Turn an existing change into a structured review surface.

`visual-recap` is the reverse of `visual-plan`: instead of planning a future
change, it summarizes a diff, branch, commit, or PR after the work exists. The
goal is to help reviewers understand the shape of a change before they dive into
raw line-by-line diffs.

## What It Does

- Reads the actual changed files and diff.
- Publishes an Agent-Native Plan recap with file trees, diagrams, data-model
  changes, API blocks, UI wireframes, and focused key diffs when useful.
- Keeps recaps substantial enough for real review without dumping every line.
- Can be installed with a reusable GitHub Action for PR visual recaps.

## When To Use It

Use it for PRs or work units that are large, multi-file, UI-heavy, or touch
schema, API contracts, permissions, architecture, or review-critical behavior.

Skip it for tiny, obvious diffs that review faster directly in GitHub.

## GitHub Action

When installed with `--with-github-action`, this repo writes a PR workflow that
can generate a visual recap from a pull request diff.

## Install

```sh
agent-native skills add BuilderIO/skills --skill visual-recap --with-github-action
```

The skill expects the Agent-Native Plan MCP connector to be available when it is
used, unless local-files privacy mode is explicitly enabled.
