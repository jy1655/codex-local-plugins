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
