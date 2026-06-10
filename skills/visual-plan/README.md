# /visual-plan

Publish a reviewable Agent-Native Plan before risky implementation work starts.

`/visual-plan` turns the plan an agent would normally write in chat into a
structured, interactive document. It can include inline diagrams, file trees,
annotated code, API and data-model blocks, open questions, comments, and optional
UI canvases or prototypes.

## What It Does

- Grounds plans in real repo files, schemas, actions, and symbols.
- Chooses the right review surface: document-only, UI canvas, prototype, design
  direction, or visual intake.
- Publishes the result as an Agent-Native Plan instead of inline Markdown.
- Keeps the plan as the approval gate before source edits begin.

## When To Use It

Use it for multi-file, ambiguous, risky, architecture-heavy, data-heavy, or
UI-heavy work where the wrong direction would be expensive. It is also useful
when a pasted text plan needs a richer review surface.

Skip it for trivial fixes, single-line changes, or anything whose diff is easier
to review than a plan.

## What Reviewers Get

Reviewers get a plan link they can scan and comment on: decisions, files,
diagrams, contracts, UI states, and unresolved questions live in one place.

## Install

```sh
agent-native skills add BuilderIO/skills --skill visual-plan
```

The skill expects the Agent-Native Plan MCP connector to be available when it is
used.
