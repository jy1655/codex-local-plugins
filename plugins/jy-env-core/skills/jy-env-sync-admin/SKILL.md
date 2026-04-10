---
name: jy-env-sync-admin
description: Use when working on this portable Codex environment repo, validating plugin bundle layout, or reapplying local changes into the home Codex install surface.
---

# JY Env Sync Admin

## Overview

This skill helps inspect and reapply the portable Codex environment defined by this repo.
It is meant for maintenance work inside this environment repo, not for arbitrary project setup.

## When to Use

- You are editing `codex-env.toml`, `plugins/`, or `instructions/`
- You want to verify which plugin bundles and instruction files this repo will install
- You need to reapply local changes without cloning the repo again

## Quick Reference

- Inspect the current repo definition:
  `python3 -m codex_env_sync.cli inspect --repo-root .`
- Apply the local checkout into your home directory:
  `python3 -m codex_env_sync.cli apply --repo-root .`
- Bootstrap from a Git URL on a fresh machine:
  `./scripts/bootstrap.sh <git-url>` or `.\scripts\bootstrap.ps1 -GitUrl <git-url>`

## Output Template

- Render the headings and short status phrases in the user's language unless the user explicitly asks for English.
- Keep the structure stable even when the labels are localized.

- `Repo:` resolved repo root
- `Install Surface:` plugin root, skills root, marketplace path, instruction targets
- `Action:` inspect, apply, or bootstrap result with next step if restart is required

## Guardrails

- Treat `~/plugins`, `~/.agents/skills/`, and `~/.agents/plugins/marketplace.json` as the install surface
- Do not edit `~/.codex/plugins/cache` directly
- Keep upstream seed material local-only; only first-party results belong in this repo
- Restart Codex after apply if plugin or instruction changes are not visible yet

## Common Mistakes

- Editing `~/.codex/plugins/cache` instead of the repo-owned plugin, instruction, or skill source
- Treating this skill like a general project bootstrap instead of an environment maintenance tool
- Forgetting that plugin or instruction changes may require a fresh Codex session to become visible
