# Global Codex Instructions

This machine is managed by the portable Codex environment sync repo.

## Environment Rules

- Treat `~/plugins`, `~/.agents/plugins/marketplace.json`, and installed instruction artifacts under `~/.codex/` as the source-owned install surface.
- Do not edit `~/.codex/plugins/cache` directly.
- When changing this environment repo, prefer first-party plugin bundles committed here over
  live dependencies on upstream seed sources.
- Treat `plugins/jy-env-*/skills/` as the first-party skill source of truth.
- Restart Codex after apply if plugin or instruction changes are not visible yet.

## Repo Rules

- This repo only stores the customized result.
- Upstream open source skills and company-shared skills are local-only seed material.
- If a skill is worth keeping, rebuild it here as a first-party plugin asset.
- Do not rebuild the repo around vendored third-party runtimes when a Codex-native first-party skill will do.

## Response Language

- User-facing responses should default to the user's language unless the user explicitly asks otherwise.
- English-first skill authoring is an internal maintenance rule, not an output-language rule.
- If the user switches languages or explicitly asks for English, follow that request.
- Keep commands, file paths, code identifiers, and other literal tokens exact even inside localized responses.

## Pack Model

- `jy-env-core` is the compact default pack.
- `jy-env-planning`, `jy-env-delivery`, `jy-env-audit`, and `jy-env-ios` are optional marketplace installs.
- Staging a plugin under `~/plugins` makes it installable; it does not activate its skills.
- Route through skills that are actually available in the current session. Do not assume an
  optional pack is installed.

## Necessity Gate

- Before defining a new task, skill, file, audit cycle, TODO/open issue/follow-up item, or speculative cleanup that the user did not explicitly request, classify it as `user-directed`, `reproducible`, or `evidenced`.
- Reject speculative padding such as broad cleanup, manufactured follow-up sections, and extra audit loops when there is no concrete problem evidence.
- If a final response keeps a follow-up/TODO/open issue section, include a concise `[necessity-gate]` block explaining the basis and decision.
