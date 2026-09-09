# Claude Search Optimization (CSO) — Detailed Guide

## Table of Contents

1. Rich Description Field
2. Keyword Coverage
3. Descriptive Naming
4. Token Efficiency
5. Cross-Referencing Skills

## 1. Rich Description Field

Purpose: Claude reads the description to decide whether the skill should load at all.
The description must answer "Should I read this skill right now?"

Format: start with `Use when...` and focus on trigger conditions.

Critical rule: `Description = When to Use`, not `What the Skill Does`.

Do not summarize the skill's workflow in the description.

### Why this matters

When the description summarizes the workflow, Claude may follow the description instead of
reading the body. A description like "execute an implementation plan while doing code review
between tasks" invites a shortcut. Claude may do only one review pass even if the real
workflow requires two.

When the description instead says "Use when executing a written implementation plan in the
current session", Claude is much more likely to read the body and follow the full workflow.

The trap is simple: a workflow-summary description becomes the shortcut.

### Bad examples

```yaml
# Workflow summary - likely to bypass the body
description: execute an implementation plan, dispatch sub-agents per task, review between tasks

# Too much process detail
description: use TDD - write tests first, fail, add minimal code, refactor

# Too abstract
description: for async testing

# First-person framing
description: can help when async tests are flaky
```

### Good examples

```yaml
# Trigger only, no workflow summary
description: Use when executing a written implementation plan in the current session

# Trigger only
description: Use when implementing a feature or bug fix before writing production code

# Tech-specific and clear
description: Use when handling authentication redirects in React Router

# Concrete symptom, not tied to one stack
description: Use when tests show race conditions, timing dependence, or inconsistent pass/fail behavior
```

### Writing guidelines

- use concrete triggers, symptoms, and contexts
- describe the problem, not one stack-specific workaround
- stay tech-agnostic unless the skill is genuinely tech-specific
- if the skill is tech-specific, say so directly in the trigger
- write in third person because the description is injected into the system context
- never summarize the full workflow here

## 2. Keyword Coverage

Use the terms Claude is likely to search for:

- error messages: `Hook timed out`, `ENOTEMPTY`, `race condition`
- symptoms: `flaky`, `hanging`, `zombie`, `pollution`
- synonyms: `timeout`, `hang`, `freeze`, `cleanup`, `teardown`, `afterEach`
- tool names, commands, libraries, file types

## 3. Descriptive Naming

Skill names are also search optimization.

Prefer:

- active voice
- verb-led names
- process-shaped gerunds such as `debugging`, `testing`, or `reviewing` when they match the behavior

Avoid:

- generic nouns with no trigger value
- names that hide the real task

## 4. Token Efficiency

Frequently loaded skills and getting-started skills compete with everything else in the
context window. Tokens are scarce.

Suggested targets:

- getting-started workflows: < 150 words each
- frequently loaded skills: < 200 words total
- most other skills: < 500 words

Techniques:

- move command flag details to `--help` references
- cross-reference other skills instead of repeating the workflow
- compress examples
- delete repetition

Bad:

```text
search-conversations supports --text, --both, --after DATE, --before DATE, --limit N ...
```

Better:

```text
search-conversations supports several modes and filters. See --help for details.
```

## 5. Cross-Referencing Skills

When another skill is required, reference the skill name directly:

- `Required background: jy-test-driven`
- `Required background: jy-debugging`

Do not use `@path/to/file` links that force-load a large file immediately.

Why: `@` syntax burns context before the file is actually needed.
