---
name: jy-library-research
description: Use when working with an unfamiliar library, package, or external dependency and need evidence-based answers with source links.
---

# JY Library Research

## Overview

Answer questions about external libraries, packages, and dependencies with evidence.
Prefer official docs, source code, and GitHub permalinks over guesswork.

## When to Use

- "How do I use this library?", "What is the best practice for this package?"
- You need to understand odd behavior from an external dependency
- You need to inspect the internal implementation of an open-source library
- You need usage guidance for an unfamiliar npm, pip, cargo, or similar package

Do not use it when:

- The question is about the current project codebase instead of an external dependency
- The library is already well understood and the answer is straightforward
- The task is really an architecture tradeoff (`jy-consult`)

## Quick Reference

| Request Type | Approach |
|--------------|----------|
| Concept | Official docs -> examples -> key pattern |
| Source analysis | GitHub source -> permalink -> behavior explanation |
| Implementation | Official example -> adapt to current project context |
| Debugging | Issue tracker -> source -> known limits or caveats |

## Research Protocol

### Step 1: Classify the request

Classify the task as concept, source analysis, implementation guidance, or debugging.
Then follow the matching research path.

### Step 2: Gather evidence

- Check official documentation first
- If source inspection is needed, capture a GitHub permalink
- Be date-aware when source material may be stale
- When current or version-specific library docs materially affect the answer, use the
  lazy Context7 CLI route below before broad web search

#### Lazy Context7 CLI route

Context7 is an optional read-only provider, not a required runtime. Do not install it
globally or block the task when it is unavailable.

1. If `ctx7` is already on `PATH`, resolve the library first with
   `CTX7_TELEMETRY_DISABLED=1 ctx7 library <library> --json`.
2. Query the resolved ID with
   `CTX7_TELEMETRY_DISABLED=1 ctx7 docs <resolved-id> "<specific question>" --json`.
3. Otherwise, when Node.js 18+ and `npx` are available, run the same two commands lazily
   through the pinned package `npx --yes ctx7@0.5.5`.
4. Treat a missing CLI, rate limit, sandbox or network denial, malformed output, or index
   mismatch as a soft failure. Fall back once to the library's official documentation,
   source repository, changelog, and issue tracker.

Keep queries limited to public library names and public technical questions. Never send
private source, credentials, tokens, customer data, or proprietary identifiers. Authentication
is optional; when the user has configured it locally, inherit `CONTEXT7_API_KEY` from the
environment instead of placing secrets in command arguments.

### Step 3: Answer with evidence

Attach sources to every important claim:

- official docs links
- GitHub permalinks with file and line references
- issue or PR references when relevant

If you infer something from the source, say so explicitly.

### Step 4: Connect it back to the project

Do not stop at a generic tutorial answer. Explain how the library guidance applies to the
current project context.

## Common Mistakes

- Saying "people usually do this" without evidence, links, or a permalink
- Presenting stale information as current without checking dates
- Giving a generic tutorial and ignoring the actual project context
- Modifying code instead of staying in research mode
- Exploring the current project codebase instead of the external dependency
- Retrying Context7 instead of falling back to authoritative public sources
- Installing or authenticating a third-party documentation CLI without a user request
