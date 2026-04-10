# Global Codex Instructions

This machine is managed by the portable Codex environment sync repo.

## Environment Rules

- Treat `~/plugins`, `~/.agents/skills/`, and `~/.agents/plugins/marketplace.json` as the source-owned install surface.
- Do not edit `~/.codex/plugins/cache` directly.
- When changing this environment repo, prefer first-party plugin bundles committed here over
  live dependencies on upstream seed sources.
- Treat `plugins/jy-env-core/skills/` as the first-party skill source of truth.
- Restart Codex after apply if plugin or instruction changes are not visible yet.

## Repo Rules

- This repo only stores the customized result.
- Upstream open source skills and company-shared skills are local-only seed material.
- If a skill is worth keeping, rebuild it here as a first-party plugin asset.
- Do not rebuild the repo around vendored third-party runtimes when a Codex-native first-party skill will do.

## Skill Routing

- If the user is still shaping a feature, product direction, or scope, prefer `jy-autoplan` first.
- If the user clearly needs idea narrowing or a product brief, prefer `jy-office-hours`.
- If the user already has a plan and wants decision gaps closed before implementation, prefer `jy-plan-review`.
- If the correct planning path is not obvious, route through `jy-autoplan` instead of choosing ad hoc.
- If the user shipped changes and now needs docs, instructions, or skill verification artifacts synced, prefer `jy-document-release`.
- Planning skills are mode-aware, but they cannot switch Codex collaboration mode themselves.
- If a planning skill says the task belongs in Plan Mode, tell the user to press `Shift+Tab` and re-run the named skill.
- If the user wants to park work, resume later, or hand off current context across sessions or branches, prefer `jy-checkpoint`.
- `jy-checkpoint` stores repo-local ignored notes under `.codex/checkpoints/` instead of hidden home-directory state.

## Execution Skill Routing

- If the user is debugging a bug, failing test, or unexpected behavior, prefer `jy-systematic-debugging`.
- If the user is starting a feature or bugfix implementation, prefer `jy-test-driven-development`.
- If the user is about to claim work is complete, fixed, or passing, prefer `jy-verification-before-completion`.
- If the user completed implementation and wants multi-angle review, prefer `jy-review-work`.
- If the user needs iterative work until verified completion, prefer `jy-work-loop`.
- If the user wants to clean AI-generated code smells from files, prefer `jy-ai-slop-remover`.
- Execution skills are mode-aware: if the user is in Plan Mode, tell them to press `Shift+Tab` and re-run in Default mode.

## Advisory and Research Skill Routing

- If the user faces architecture decisions, repeated failures, or security/performance concerns, prefer `jy-oracle-consult`.
- If the user needs evidence-based answers about external libraries or packages, prefer `jy-library-research`.
- If the user needs multi-angle codebase exploration across modules, prefer `jy-codebase-explore`.
- If the user's request is ambiguous and needs intent classification, prefer `jy-intent-gate`.
