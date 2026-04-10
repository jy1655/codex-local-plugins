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

## Response Language

- User-facing responses should default to the user's language unless the user explicitly asks otherwise.
- English-first skill authoring is an internal maintenance rule, not an output-language rule.
- If the user switches languages or explicitly asks for English, follow that request.
- Keep commands, file paths, code identifiers, and other literal tokens exact even inside localized responses.

## Skill Routing

- If the user is still shaping a feature, product direction, or scope, prefer `jy-autoplan` first.
- If the user clearly needs idea narrowing or a product brief, prefer `jy-framing`.
- If the user already has a plan and wants decision gaps closed before implementation, prefer `jy-plan-review`.
- If the user has approved requirements and now needs a detailed implementation plan, prefer `jy-writing-plans`.
- If the user wants an isolated feature branch or worktree before implementation, prefer `jy-worktrees`.
- If the correct planning path is not obvious, route through `jy-autoplan` instead of choosing ad hoc.
- If the user shipped changes and now needs docs, instructions, or skill verification artifacts synced, prefer `jy-document-release`.
- If the user wants to ship a ready branch, push verified changes, or create/update a PR/MR, prefer `jy-ship`.
- Planning skills are mode-aware, but they cannot switch Codex collaboration mode themselves.
- If a planning skill says the task belongs in Plan Mode, tell the user to press `Shift+Tab` and re-run the named skill.
- If the user wants to park work, resume later, or hand off current context across sessions or branches, prefer `jy-checkpoint`.
- `jy-checkpoint` stores repo-local ignored notes under `.codex/checkpoints/` instead of hidden home-directory state.

## Execution Skill Routing

- If the user is debugging a bug, failing test, or unexpected behavior, prefer `jy-debugging`.
- If the user is starting a feature or bugfix implementation, prefer `jy-test-driven`.
- If the user wants an existing written plan executed task-by-task, prefer `jy-executing-plans`.
- If the user is about to claim work is complete, fixed, or passing, prefer `jy-verification-before-completion`.
- If the user completed implementation and wants multi-angle review, prefer `jy-review-work`.
- If the user is responding to review feedback or PR comments, prefer `jy-receiving-review`.
- If the user needs iterative work until verified completion, prefer `jy-loop`.
- If the user wants to clean AI-generated code smells from files, prefer `jy-slop-remover`.
- If the user wants the current branch pushed and a PR/MR created after fresh gates pass, prefer `jy-ship`.
- Execution skills are mode-aware: if the user is in Plan Mode, tell them to press `Shift+Tab` and re-run in Default mode.

## Advisory and Research Skill Routing

- If the user faces architecture decisions, repeated failures, or security/performance concerns, prefer `jy-consult`.
- If the user needs evidence-based answers about external libraries or packages, prefer `jy-library-research`.
- If the user needs multi-angle codebase exploration across modules, prefer `jy-codebase-explore`.
- If the user's request is ambiguous and needs intent classification, prefer `jy-intent-gate`.
