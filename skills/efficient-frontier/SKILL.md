---
name: efficient-frontier
description: Use when running any expensive frontier model on codebase-heavy or token-heavy work and the user wants a model-agnostic pattern for delegating research, coding, and testing to cheaper subagents.
---

# Efficient Frontier

Use the expensive frontier model where its marginal judgment matters. Push
repeatable, bounded, or token-heavy work to cheaper/faster subagents.

## Workflow

1. Identify the frontier-only decisions: architecture, prioritization,
   ambiguity resolution, risk, synthesis, and final review.
2. Identify delegable work: research scans, repository inventory, search, docs
   extraction, browser/testing passes, log reduction, test failure clustering,
   narrow coding, and mechanical edits.
3. Spawn parallel subagents for independent slices with clear ownership and
   expected evidence.
4. Require compact returns: findings, changed files, commands run, residual
   risk, and anything the frontier model must decide.
5. Integrate and review centrally before presenting the result.

## Common Scenarios

Use these as soft suggestions:

- Research: delegate broad repo scans, docs extraction, and source comparison;
  the frontier model keeps the judgment about what matters.
- Coding: delegate bounded patches, refactors, or mechanical edits when file
  ownership is clear; integrate and review centrally.
- Testing: let the frontier model choose the validation strategy and scripts,
  then use cheaper agents to run unit checks, browser flows, screenshots, and
  log reduction. Ask them to return exact commands, failures, likely causes, and
  whether the signal looks flaky, environmental, or product-relevant.
- Debugging: send independent agents after separate theories, logs, or repro
  paths; keep the final diagnosis with the frontier model.

## Guardrails

- Do not delegate the immediate blocker if your next step depends on it.
- Do not ask multiple agents to edit the same files at the same time.
- Do not trust subagent conclusions blindly when the risk is high; inspect the
  important evidence yourself.
- Do not claim universal savings. The pattern works best when exploration and
  implementation, testing, or research can be parallelized.

## Default Framing

"I will use the frontier model as the orchestrator and reviewer, and use
cheaper subagents for token-heavy research, coding, or testing so the expensive
tokens go to judgment, synthesis, and final quality."
