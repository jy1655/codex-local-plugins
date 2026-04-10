---
name: jy-codebase-explore
description: Use when multiple modules are involved in a search or the codebase structure is unfamiliar and needs multi-angle exploration.
---

# JY Codebase Explore

## Overview

Explore the current codebase from multiple angles to understand structure, patterns, and
dependencies. Use it when a single keyword search is not enough to build the full picture.

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
| 4. Structured result | Return file path, line, and a useful summary |

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

| File | Line | Why it matters |
|------|------|----------------|
| src/auth/handler.ts | 42 | Authentication entry point |
| src/db/users.ts | 15 | User lookup query |

### Structure Summary

auth -> handler.ts -> users.ts -> session.ts
```

### Step 4: Match the requested depth

- `quick`: one or two direct searches
- `medium`: multi-angle search plus import tracing
- `very thorough`: cross-layer analysis plus dependency mapping

If the user does not specify depth, start with `medium`.

## Common Mistakes

- Searching one keyword and stopping there
- Listing file paths without line numbers or explanations
- Exploring external library source when the task is repo exploration
- Guessing instead of showing evidence
- Jumping into grep before clarifying what must actually be found
