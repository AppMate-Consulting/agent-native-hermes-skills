"""CLI helpers for the AppMate Agent-Native Hermes skills plugin."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable

REPO = "AppMate-Consulting/agent-native-hermes-skills"
PLAN_MCP_URL = "https://plan.agent-native.com/_agent-native/mcp"
DEFAULT_CATEGORY = "agent-native"
DEFAULT_SKILLS = ("visual-plan", "visual-recap", "efficient-frontier")
OPTIONAL_SKILLS = ("efficient-fable", "stay-within-limits", "quick-recap")
ALL_SKILLS = DEFAULT_SKILLS + OPTIONAL_SKILLS


@dataclass
class CommandResult:
  label: str
  returncode: int


def register_cli(parser: argparse.ArgumentParser) -> None:
  parser.description = "Install and manage AppMate Agent-Native Hermes skills."
  subs = parser.add_subparsers(dest="agent_native_action")

  setup = subs.add_parser(
    "setup",
    help="Install default skills and optionally configure hosted Plan MCP",
  )
  _add_common_setup_args(setup)
  mcp_group = setup.add_mutually_exclusive_group()
  mcp_group.add_argument(
    "--with-mcp",
    action="store_true",
    help="Also add/test the hosted Agent-Native Plan MCP connector",
  )
  mcp_group.add_argument(
    "--skip-mcp",
    action="store_true",
    help="Install skills only (kept for explicit scripts; this is the default)",
  )
  setup.add_argument(
    "--local-files",
    action="store_true",
    help="Print local-files mode guidance after setup",
  )

  install = subs.add_parser("install-skills", help="Install selected AppMate skills")
  _add_common_setup_args(install)

  mcp = subs.add_parser("mcp", help="Configure/test the hosted Plan MCP connector")
  mcp.add_argument("--dry-run", action="store_true", help="Show commands without running them")
  mcp.add_argument("--no-test", action="store_true", help="Add connector without running mcp test")

  status = subs.add_parser("status", help="Show installed skill and Plan MCP status")
  status.add_argument("--dry-run", action="store_true", help="Show commands without running them")

  parser.set_defaults(func=dispatch)


def _add_common_setup_args(parser: argparse.ArgumentParser) -> None:
  parser.add_argument(
    "--category",
    default=DEFAULT_CATEGORY,
    help=f"Hermes skill category folder (default: {DEFAULT_CATEGORY})",
  )
  parser.add_argument(
    "--skill",
    action="append",
    choices=ALL_SKILLS,
    help="Skill to install; repeatable. Defaults to visual-plan, visual-recap, efficient-frontier.",
  )
  parser.add_argument(
    "--all-skills",
    action="store_true",
    help="Install every skill retained in this fork, including upstream parity skills",
  )
  parser.add_argument("--dry-run", action="store_true", help="Show commands without running them")


def dispatch(args: argparse.Namespace) -> int:
  action = getattr(args, "agent_native_action", None) or "status"
  if action == "setup":
    return _setup(args)
  if action == "install-skills":
    return _install_skills(args)
  if action == "mcp":
    return _configure_mcp(args)
  if action == "status":
    return _status(args)
  print("Unknown agent-native action. Run `hermes agent-native --help`.", file=sys.stderr)
  return 2


def _setup(args: argparse.Namespace) -> int:
  rc = _install_skills(args)
  if rc != 0:
    return rc

  if getattr(args, "with_mcp", False):
    rc = _configure_mcp(args)
    if rc != 0:
      return rc
  else:
    print("\nHosted Plan MCP not configured. Add it later with:")
    print("  hermes agent-native mcp")

  if getattr(args, "local_files", False):
    _print_local_files_guidance()
  else:
    print("\nFor private/client work, use local-files mode:")
    print("  export AGENT_NATIVE_PLANS_MODE=local-files")

  print("\nInside an active Hermes session, run:")
  print("  /reload-skills")
  if getattr(args, "with_mcp", False):
    print("  /reload-mcp")
  return 0


def _install_skills(args: argparse.Namespace) -> int:
  category = getattr(args, "category", DEFAULT_CATEGORY) or DEFAULT_CATEGORY
  skills = _selected_skills(args)
  failures: list[CommandResult] = []

  for skill in skills:
    identifier = f"{REPO}/skills/{skill}"
    cmd = _hermes_cmd(["skills", "install", identifier, "--category", category, "--yes"])
    result = _run(cmd, label=f"install {skill}", dry_run=getattr(args, "dry_run", False))
    if result.returncode != 0:
      failures.append(result)

  if failures:
    print("\nSkill install failures:", file=sys.stderr)
    for failure in failures:
      print(f"  {failure.label}: exit {failure.returncode}", file=sys.stderr)
    return 1

  print("\nInstalled AppMate Agent-Native skills:")
  for skill in skills:
    print(f"  - {skill}")
  return 0


def _configure_mcp(args: argparse.Namespace) -> int:
  dry_run = getattr(args, "dry_run", False)
  add_cmd = _hermes_cmd(["mcp", "add", "plan", "--url", PLAN_MCP_URL, "--auth", "oauth"])
  add_result = _run(add_cmd, label="add Plan MCP", dry_run=dry_run, allow_failure=True)

  if add_result.returncode != 0:
    print(
      "\n`hermes mcp add plan` returned non-zero. This is usually harmless if `plan` already exists; testing next.",
      file=sys.stderr,
    )

  if getattr(args, "no_test", False):
    return 0 if dry_run or add_result.returncode == 0 else add_result.returncode

  test_cmd = _hermes_cmd(["mcp", "test", "plan"])
  test_result = _run(test_cmd, label="test Plan MCP", dry_run=dry_run, allow_failure=True)
  if test_result.returncode != 0:
    print("\nPlan MCP test failed. Check auth/session reload, then run:", file=sys.stderr)
    print("  hermes mcp test plan", file=sys.stderr)
    print("  /reload-mcp", file=sys.stderr)
    return test_result.returncode
  return 0


def _status(args: argparse.Namespace) -> int:
  dry_run = getattr(args, "dry_run", False)
  commands = [
    ("installed skills", _hermes_cmd(["skills", "list"])),
    ("configured MCP servers", _hermes_cmd(["mcp", "list"])),
  ]
  rc = 0
  for label, cmd in commands:
    result = _run(cmd, label=label, dry_run=dry_run, allow_failure=True)
    rc = rc or result.returncode
  print("\nExpected default skills:")
  for skill in DEFAULT_SKILLS:
    print(f"  - {skill}")
  print(f"\nPlan MCP URL: {PLAN_MCP_URL}")
  return rc


def _selected_skills(args: argparse.Namespace) -> tuple[str, ...]:
  if getattr(args, "all_skills", False):
    return ALL_SKILLS
  selected = getattr(args, "skill", None)
  if selected:
    # Preserve order while removing repeated --skill values.
    return tuple(dict.fromkeys(selected))
  return DEFAULT_SKILLS


def _hermes_cmd(parts: Iterable[str]) -> list[str]:
  hermes = shutil.which("hermes") or "hermes"
  cmd = [hermes]
  profile = _active_profile_name()
  if profile and profile not in {"default", "custom"}:
    cmd.extend(["--profile", profile])
  cmd.extend(parts)
  return cmd


def _active_profile_name() -> str:
  try:
    from hermes_cli.profiles import get_active_profile_name

    return str(get_active_profile_name() or "default")
  except Exception:
    return os.getenv("HERMES_PROFILE", "default") or "default"


def _run(
  cmd: list[str],
  *,
  label: str,
  dry_run: bool = False,
  allow_failure: bool = False,
) -> CommandResult:
  printable = " ".join(_quote(part) for part in cmd)
  print(f"\n$ {printable}", flush=True)
  if dry_run:
    return CommandResult(label=label, returncode=0)

  proc = subprocess.run(cmd, text=True)
  if proc.returncode != 0 and not allow_failure:
    print(f"Command failed ({label}) with exit {proc.returncode}", file=sys.stderr)
  return CommandResult(label=label, returncode=proc.returncode)


def _quote(value: str) -> str:
  if not value:
    return "''"
  safe = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_./:-=@"
  if all(ch in safe for ch in value):
    return value
  return "'" + value.replace("'", "'\\''") + "'"


def _print_local_files_guidance() -> None:
  print("\nLocal-files mode:")
  print("  export AGENT_NATIVE_PLANS_MODE=local-files")
  print("\nExpected repo artifacts:")
  print("  plans/<slug>/plan.mdx")
  print("  plans/<slug>/canvas.mdx        # optional")
  print("  plans/<slug>/prototype.mdx     # optional")
  print("  plans/<slug>/.plan-state.json  # optional")
  print("\nPreview:")
  print("  npx @agent-native/core@latest plan local preview --dir plans/<slug> --kind plan")
  print("  npx @agent-native/core@latest plan local preview --dir plans/<slug> --kind recap")
