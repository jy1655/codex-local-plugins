---
name: jy-codebase-explore
description: Use when multiple modules are involved in a search or the codebase structure is unfamiliar and needs multi-angle exploration.
---

# JY Codebase Explore

## Overview

Explore the current codebase from multiple angles to understand structure, patterns, and
dependencies. Use it when a single keyword search is not enough to build the full picture,
and distinguish current evidence from stale or unverified context without stopping read-only
exploration.

## When to Use

- "Where is X implemented?", "Find the code that does Y"
- Two or more modules or layers are likely involved
- The repository structure is unfamiliar
- The task requires tracing a path across layers such as API -> service -> DB

Do not use it when:

- The exact file or symbol is already known
- A single keyword search is enough
- The task is really external library research (`jy-library-research`)

## Quick Reference

| Step | Action |
|------|--------|
| 1. Intent analysis | Separate the literal request from the real search goal |
| 2. Search strategy | Build multi-angle keywords and patterns |
| 3. Parallel exploration | Run multiple searches at once |
| 4. Freshness | Label material evidence when its currency matters |
| 5. Structured result | Return file path, line, evidence status, and a useful summary |

## Exploration Protocol

### Step 1: Separate literal wording from search intent

Write down:

```
Literal request: what the user asked for
Actual search goal: what must be found
Search angles: which keywords or patterns to try
```

### Step 2: Search from multiple angles

Do not depend on one keyword only:

- function, class, and type names
- error messages or log strings
- file globs and naming patterns
- import or require paths
- comments or documentation keywords

### Step 3: Return actionable results

Structure findings so someone can immediately open the right place:

```markdown
### Findings

| File | Line | Status | Why it matters |
|------|------|--------|----------------|
| src/auth/handler.ts | 42 | CURRENT | Authentication entry point |
| docs/auth-plan.md | 15 | STALE | Search lead, not current implementation proof |

### Structure Summary

auth -> handler.ts -> users.ts -> session.ts
```

### Step 4: Treat freshness as context

- Prefer the current source tree, current diff, and fresh read-only queries over older plans or reports
- When currency affects the conclusion, label evidence `CURRENT`, `STALE`, `UNKNOWN`, or
  `NOT-VERIFIED` and include the relevant source, revision, or timestamp
- Use stale documents as search leads, not as current proof and not as a reason to stop exploration
- Escalate only when missing freshness would make a later consequential mutation unsafe; read-only
  tracing should continue with the best available evidence

### Step 5: Match the requested depth

- `quick`: one or two direct searches
- `medium`: multi-angle search plus import tracing
- `very thorough`: cross-layer analysis plus dependency mapping

If the user does not specify depth, start with `medium`.

## Common Mistakes

- Searching one keyword and stopping there
- Listing file paths without line numbers or explanations
- Exploring external library source when the task is repo exploration
- Trusting stale plans as current source evidence or stopping a read-only trace because some context is stale
- Guessing instead of showing evidence
- Jumping into grep before clarifying what must actually be found
