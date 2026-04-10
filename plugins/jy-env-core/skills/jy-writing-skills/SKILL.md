---
name: jy-writing-skills
description: Use when creating a new skill, revising an existing skill, or verifying that a first-party skill is ready for deployment in this repo.
---

# JY Writing Skills

## Table of Contents

- Overview
- Quick Reference
- What Counts as a Skill
- TDD Mapping for Skill Writing
- When to Write a Skill
- Skill Types
- Directory Layout
- `SKILL.md` Structure
- Authoring Language Policy
- Claude Search Optimization
- The Iron Law
- Testing Strategy
- Red Flags
- Common Mistakes
- RED-GREEN-REFACTOR Cycle
- Skill Writing Checklist
- When to Use Flowcharts
- Code Examples
- STOP Before Moving On
- Discovery Workflow
- Summary

## Overview

Skill authoring is TDD applied to process documentation. Write the test case first
(pressure scenarios), watch the baseline failure, write the skill, verify it, then close
the loopholes.

Core principle: if you did not watch an agent fail without the skill, you do not know
whether the skill teaches the right behavior.

Required background: understand `jy-test-driven` first. That skill defines the
RED-GREEN-REFACTOR cycle this guide builds on.

## Quick Reference

| Phase | Must Be True | Failure Signal |
|-------|--------------|----------------|
| RED | You observed the baseline failure without the skill | You wrote docs before pressure scenarios |
| GREEN | You wrote the smallest document that blocks that failure | You only added checklists and examples |
| REFACTOR | You blocked the new rationalization paths too | You stopped after one passing run |
| Ship | You verified references, agents, and tests together | You edited only `SKILL.md` |

## What Counts as a Skill

A skill is a reusable guide for a proven technique, pattern, or tool. It is not a narrative
about one past session.

In this repo, first-party workflow skills include items such as `jy-writing-plans`,
`jy-executing-plans`, `jy-worktrees`, and `jy-receiving-review`.

## TDD Mapping for Skill Writing

| TDD Concept | Skill Writing Equivalent |
|-------------|--------------------------|
| Test case | pressure scenario, often with sub-agents |
| Production code | `SKILL.md` and supporting references |
| RED failure | agent violates the rule without the skill |
| GREEN success | agent follows the rule with the skill |
| REFACTOR | keep compliance while closing loopholes |

## When to Write a Skill

Write a skill when:

- the technique is not obvious
- it is reused across projects
- the pattern is broad rather than project-specific
- other people will benefit from reusing it

Do not write a skill when:

- it is a one-off solution
- a good standard already exists elsewhere
- it is a project-specific rule that belongs in `CLAUDE.md` or repo instructions
- the constraint can be enforced mechanically with regex, lint, or automation

## Skill Types

- Technique: a concrete method with steps to follow
- Pattern: a way of thinking about a class of problems
- Reference: API docs, syntax guidance, or tool manuals

## Directory Layout

```text
skills/
  skill-name/
    SKILL.md
    supporting-file.*
```

Keep the namespace flat so every skill remains searchable.

Move content out of `SKILL.md` when it is:

- large reference material (100+ lines)
- reusable tooling such as scripts, templates, or utilities

Keep content inline when it is:

- core principles
- short code patterns
- anything small enough to be scanned quickly

## `SKILL.md` Structure

Frontmatter:

- required: `name`, `description`
- `name`: lowercase letters, numbers, hyphens only
- `description`: third-person, starts with `Use when...`, includes triggers only

Preferred body structure:

- Overview
- When to Use
- Core Pattern when relevant
- Quick Reference
- Implementation or supporting references
- Common Mistakes

## Authoring Language Policy

The default is simple:

- core `SKILL.md` content is `English-first`
- `agents/openai.yaml` fields such as `display_name`, `short_description`, and `default_prompt` follow the same rule
- supporting references should also be English-first when the model is likely to read them directly

Why:

- skills are model-facing documents first
- search, trigger matching, cross-skill reuse, and provider portability are more stable in English
- mixed language in core workflow docs increases maintenance drift

Allowed exceptions:

- user-facing README files, human-facing Korean operating notes, and result templates may be bilingual or `Korean`
- repo-specific notes written mainly for humans may remain Korean
- but the core workflow instruction should not default to Korean without a specific reason

`English-first` is an authoring rule, not an `output-language rule`.

- the final user-facing response should follow the user's language by default
- if the user asks for English or switches languages, follow that request
- if a skill has an `Output Template`, its labels and short status phrases should be rendered in the user's language at runtime
- keep literal tokens such as commands, paths, and code identifiers exact

## Claude Search Optimization

Claude Search Optimization (CSO) matters because the description controls whether the skill
gets loaded at all.

### Description field

The description has only two jobs:

1. state the trigger conditions clearly
2. avoid summarizing the workflow

If the description summarizes the workflow, the agent may follow the description instead of
reading the body.

Good:

- "Use when executing a written implementation plan in the current session"
- "Use when starting a feature or bug fix before implementation"

Bad:

- "Use for TDD: write tests first, fail, implement, refactor"
- "Use for async testing"

### Keyword coverage

Use the terms Claude is likely to search for:

- error messages such as `timeout exceeded` or `ENOTEMPTY`
- symptoms such as `flaky`, `hanging`, or `race condition`
- synonyms such as `cleanup`, `teardown`, or `pollution`
- real tool names, commands, and library names

### Token efficiency

Frequently loaded skills compete with the rest of the context window.

Rough goals:

- getting-started workflows: under 150 words
- frequently loaded skills: under 200 words
- most other skills: under 500 words

Techniques:

- move long details into references
- cross-reference another skill instead of repeating it
- keep examples short
- remove repetition

### Cross-skill references

Use a plain skill-name reference such as:

```markdown
Required background: `jy-test-driven`
```

Do not use `@` file links that force-load large files too early.

## The Iron Law

```text
Do not write or revise a skill without a failing test first.
```

That rule applies to both new skills and edits to existing skills.

No exceptions:

- not for a small addition
- not for a new section
- not for a doc-only update
- do not keep untested changes "as reference"
- do not "adapt while testing"

## Testing Strategy

For rule-enforcement skills:

- comprehension questions
- pressure scenarios
- compound pressure: time + sunk cost + fatigue

For technique skills:

- application scenarios
- edge-case variations

For pattern skills:

- recognition scenarios
- application scenarios
- negative examples where the pattern should not be used

For reference skills:

- search scenarios
- apply-what-you-found scenarios

Detailed guidance lives in `references/skill-testing-guide.md`.

For loophole-closing patterns such as pressure scenarios, anti-rationalization tables, STOP
gates, and repeated injection, see `references/bulletproofing-skills.md`.

For CSO examples and counterexamples, see `references/cso-detailed.md`.

## Red Flags

```markdown
- code written before the test
- "I already tested it manually"
- "writing the test after the code reaches the same goal"
- "I followed the spirit"
- "this is different because..."

All mean the same thing: delete the code and restart with TDD.
```

## Common Mistakes

- putting workflow summaries into frontmatter descriptions so the agent never reads the body
- omitting scan-friendly sections like `Quick Reference` and `Common Mistakes`
- copying stale or nonexistent skill names
- assuming the document is obviously correct without seeing the baseline failure
- failing to say when a supporting file should be read
- breaking the English-first rule for core workflow docs without a specific reason
- treating English-first authoring as permission to force English user-facing output

## RED-GREEN-REFACTOR Cycle

RED:

- run the pressure scenario without the skill
- capture what the agent does, what excuses it uses, and what pressure triggers the violation

GREEN:

- write the smallest skill that counters those exact excuses
- rerun the same scenario with the skill and confirm compliance

REFACTOR:

- look for new excuses
- add explicit counters
- retest until no useful loopholes remain

## Skill Writing Checklist

### RED

- write pressure scenarios
- use 3+ combined pressures for rule skills
- run the scenario without the skill
- record baseline behavior and rationalizations

### GREEN

- keep the name lowercase plus hyphens
- define `name` and `description`
- start the description with `Use when...`
- keep the core `SKILL.md` and agent prompt surface English-first
- keep user-facing output aligned with the user's language
- include search keywords
- state the core principle clearly
- address the specific RED failures
- define output-language behavior for any `Output Template`
- include either inline examples or a targeted file reference
- rerun the scenario with the skill

### REFACTOR

- capture new rationalizations from testing
- add explicit counters
- maintain a rationalization table if useful
- add a Red Flags list
- retest until the loopholes are closed

### Quality checks

- use a flowchart only when the decision is not obvious
- include a Quick Reference table
- include a Common Mistakes section
- avoid narrative storytelling
- keep supporting files for tools or large references only

### Ship

- commit the skill changes
- consider contributing broadly useful guidance upstream only after the first-party version is stable

## When to Use Flowcharts

Use a flowchart when:

- a decision point is not obvious
- a process has early stop conditions
- the skill needs a real A-vs-B decision

Do not use a flowchart for:

- pure reference material
- code examples
- linear instructions
- meaningless labels such as `step1` or `helper2`

See `references/graphviz-conventions.dot` for style rules.

## Code Examples

One strong example beats many average ones.

Choose the most relevant language:

- testing techniques -> TypeScript or JavaScript
- systems debugging -> Shell or Python
- data handling -> Python

A good example is:

- complete and runnable
- commented only where the WHY matters
- grounded in a real scenario
- clear about the pattern being taught

Avoid:

- 5+ language versions
- fill-in-the-blank templates
- contrived examples

## STOP Before Moving On

After writing a skill, stop and finish the deployment loop before starting the next one.

Do not:

- batch multiple untested skills
- move on before validating the current one
- skip tests because batching feels efficient

Shipping an untested skill is the same quality failure as shipping untested code.

## Discovery Workflow

How future Claude instances find a skill:

1. a problem appears
2. the skill description matches
3. the Overview confirms relevance
4. the Quick Reference gives the pattern
5. examples or references load only when needed

Optimize for that flow. Put searchable information early.

## Summary

Skill authoring is TDD for process documentation. Same Iron Law, same cycle, same quality
bar. If you would use TDD for code, use it for skills too.
