---
name: jy-writing-skills
description: Use when creating a new skill, revising an existing skill, or verifying that a first-party skill is ready for deployment in this repo.
---

# JY Writing Skills

## Overview

Author small, discoverable first-party skills whose instructions are proportional to their
risk. Use static checks for structure, manual pressure scenarios for behavior, and fresh
deployment checks for the installed surface. Do not manufacture a behavioral test cycle for
a wording-only edit.

## Authoring Language

- Use English-first wording for the core `SKILL.md` and `agents/openai.yaml` because these
  are model-facing instructions.
- Korean and other languages are valid for user-facing examples or an explicitly justified
  locale-specific skill.
- Respond in the user's language. English-first authoring is not an output-language rule.

## Skill Shape

Every skill needs:

- YAML frontmatter with a directory-matching `name`;
- a third-person `description` beginning with `Use when` and describing triggers;
- only the workflow, boundaries, and examples needed to change agent behavior;
- `agents/openai.yaml` when the plugin surface expects it.

Sections such as Quick Reference, Common Mistakes, or a flowchart are optional. Add them
only when they materially improve a non-trivial workflow.

## Risk Tiers

### Tier 1: metadata or wording

Examples: typo, clearer sentence, display metadata, non-behavioral link fix.

- inspect the local context;
- edit narrowly;
- run targeted schema, link, or compliance checks;
- do not require a manual pressure run unless the trigger or behavior changed.

### Tier 2: trigger or workflow behavior

Examples: description trigger, routing decision, mode behavior, output contract.

- define the failure the change should prevent;
- update the matching `pressure-scenarios.json` input;
- run relevant static tests;
- manually run the scenario when behavioral confidence is required, and record the actual
  model/configuration externally.

### Tier 3: safety or irreversible action

Examples: git publication, destructive operations, external messages, secret handling.

- use adversarial pressure cases and explicit stop conditions;
- test likely rationalizations and permission boundaries;
- require fresh, task-specific verification before deployment.

The files in `skill-tests/first-party/` are manual inputs. Their presence proves schema
coverage only, not that an evaluation passed.

## Workflow

1. Confirm the requested skill or change is necessary and belongs in this plugin.
2. Inspect the nearest existing skill, plugin conventions, and current tests.
3. Classify the change as Tier 1, 2, or 3.
4. Write the smallest instruction that closes the evidenced gap.
5. Update `agents/openai.yaml`, routing docs, or pressure scenarios only when their contract
   changed.
6. Run proportional static checks.
7. For Tier 2 or 3, run manual pressure evaluation when the user or release risk requires
   behavioral evidence; never imply it ran when it did not.
8. Apply the repo and start a fresh Codex session when deployment visibility matters.

## Pressure Scenario Guidance

Each manual scenario should name one realistic pressure, a likely failure without the
skill, and observable expected behavior with it. Avoid vague success language.

See [skill-testing-guide.md](references/skill-testing-guide.md) for scenario design. For
high-pressure rule skills, use [bulletproofing-skills.md](references/bulletproofing-skills.md)
and [cso-detailed.md](references/cso-detailed.md) selectively. These references do not turn
every edit into a mandatory baseline experiment.

## Visual Workflows

Use a diagram only when branching or state transitions are hard to understand in prose.
Follow [graphviz-conventions.dot](references/graphviz-conventions.dot) for repo-native DOT
style; do not add a renderer runtime merely to document a simple sequence.

## Deployment Check

- run the relevant unit tests and `git diff --check`;
- run `python3 -m codex_env_sync.cli inspect --repo-root .`;
- for this local development repo, run normal `apply` so the live symlink surface updates;
- for a detached install, use `apply --snapshot` or bootstrap;
- start a fresh Codex session if discovery metadata changed.

## Common Mistakes

- Encoding usage instructions in the description instead of trigger conditions
- Adding boilerplate sections that do not affect decisions
- Treating scenario JSON as evidence of an executed evaluation
- Requiring a no-skill baseline for a typo or metadata-only change
- Copying stale namespaces or third-party runtime assumptions
- Editing generated plugin cache instead of the first-party source
