#!/usr/bin/env python3
"""Sync the root skill payload into the plugin `skills/` directory.

Run this after changing the root `SKILL.md`, `agents/`, `references/`, or `scripts/`
so the repository remains usable both as a direct Codex skill and as a Codex plugin.
"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SKILL = ROOT / "skills" / "blueprint-driven-project-runner"
SYNC_ITEMS = ["SKILL.md", "agents", "references", "scripts"]


def ignore_generated(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name == "__pycache__" or name.endswith(".pyc")}


def ensure_safe_target() -> None:
    skills_root = (ROOT / "skills").resolve()
    target = PLUGIN_SKILL.resolve()
    if not str(target).startswith(str(skills_root)):
        raise RuntimeError(f"unsafe plugin skill target: {target}")


def sync_item(name: str) -> None:
    source = ROOT / name
    destination = PLUGIN_SKILL / name
    if not source.exists():
        raise FileNotFoundError(source)
    if destination.exists():
        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()
    if source.is_dir():
        shutil.copytree(source, destination, ignore=ignore_generated)
    else:
        shutil.copy2(source, destination)


def main() -> int:
    ensure_safe_target()
    PLUGIN_SKILL.mkdir(parents=True, exist_ok=True)
    for item in SYNC_ITEMS:
        sync_item(item)
    print(f"synced plugin skill: {PLUGIN_SKILL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
