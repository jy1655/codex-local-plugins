---
name: jy-env-sync-admin
description: Use when working on this portable Codex environment repo, validating plugin bundle layout, or reapplying local changes into the home Codex install surface.
---

# JY Env Sync Admin

## Overview

Inspect, apply, or bootstrap this repository's Codex install surface. Local development and
portable installation intentionally use different modes: local `apply` may link plugin
sources and instructions from the live checkout, while bootstrap and `--snapshot` stage
stable copies. Marketplace policy selects which staged plugins `apply` installs through the
Codex CLI; a second native skill link is never used.

## Quick Reference

- Read-only manifest, path, source, marketplace, and managed-state validation:
  `python3 -m codex_env_sync.cli inspect --repo-root .`
- Apply the live local checkout:
  `python3 -m codex_env_sync.cli apply --repo-root .`
- Install a detached copy from the current checkout:
  `python3 -m codex_env_sync.cli apply --repo-root . --snapshot`
- Bootstrap a fresh machine from Git:
  `./scripts/bootstrap.sh <git-url>` or `./scripts/bootstrap.ps1 -GitUrl <git-url>`

## Install Semantics

- On macOS/Linux, normal local `apply` uses symlinks for plugin sources and instructions.
- Windows local mode follows the manifest copy override.
- `--snapshot` forces copies on every platform.
- Bootstrap clones once and applies a snapshot; the managed clone is not the live runtime
  surface.
- All pack sources are staged under `~/plugins`; `apply` installs or refreshes core-lite
  with `codex plugin add`, while optional packs remain available through the marketplace.
- The apply engine removes its legacy `~/.agents/skills/<plugin>` overlays after drift
  validation so each skill has one discovery source.
- Installed plugin changes require the cachebuster/reinstall flow and a fresh thread.
- Preflight validation completes before stale managed paths or installed files are changed.
- Modified stale managed copies are preserved and reported instead of being deleted.

## Guardrails

- Edit `plugins/jy-env-*/skills/`, `instructions/`, or the apply engine, never
  `~/.codex/plugins/cache`.
- Preserve unrelated user marketplace entries and user-owned hooks.
- Treat source, manifest, marketplace, and prior ownership-state errors as apply blockers.
- Restart Codex after discovery metadata or instructions change if the current session does
  not refresh them.

## Mode-Aware Behavior

### If current collaboration mode is Default

Run inspect, tests, and the authorized apply/bootstrap operation for real.

### If current collaboration mode is Plan

Do not mutate the home install surface. Tell the user to leave Plan mode with `Shift+Tab`
and re-run this skill in Default mode; provide the resolved command as a preview.

## Output Template

Render labels in the user's language unless English was requested.

- `Repo:` resolved checkout
- `Install Mode:` live link / platform copy / snapshot
- `Install Surface:` staged plugins, marketplace policies, instructions; legacy skills root
  cleanup-only
- `Validation:` PASS / blocker
- `Action:` inspected / applied / bootstrapped / no change

## Common Mistakes

- Editing generated plugin cache
- Using bootstrap for an already-open local development checkout
- Assuming bootstrap links a mutable clone into production
- Running mutations before preflight validation
