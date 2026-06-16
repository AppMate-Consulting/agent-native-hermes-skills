"""Hermes plugin entry point for AppMate Agent-Native skills."""
from __future__ import annotations

from . import agent_native_cli


def register(ctx):
  """Register `hermes agent-native ...` CLI helpers."""
  ctx.register_cli_command(
    name="agent-native",
    help="Install and manage AppMate Agent-Native Hermes skills",
    setup_fn=agent_native_cli.register_cli,
    handler_fn=agent_native_cli.dispatch,
  )
