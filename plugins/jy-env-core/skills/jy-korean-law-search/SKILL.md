---
name: jy-korean-law-search
description: Use when the user needs Korean law, ordinance, precedent, interpretation, annex, amendment history, or procedure research through the installed `korean-law` MCP server.
---

# JY Korean Law Search

## Overview

Use the installed `korean-law` MCP server as the primary path for Korean legal research in
this environment. Route the request to the narrowest current tool family, report the law or
decision identifiers you actually retrieved, and keep the answer informational rather than
legal advice.

For a pure legal lookup, answer directly from the retrieved law or decision material. For a
real-world situation, separate the answer into a `General legal answer` grounded in the law
and a `Practical answer` grounded in directly relevant precedent, interpretation, appeal, or
tribunal material when that support actually exists.

If calls fail with API-key errors in this repo, treat that as a local `LAW_OC` overlay issue
first. Do not tell the user to commit secrets into the repo.

## When to Use

- Korean statutes, enforcement decrees, rules, and ordinances
- article text, annexes, forms, and amendment history
- precedents, interpretations, administrative appeals, tribunal decisions
- procedure, penalty, compliance, customs, or ordinance-comparison questions

Do not use it when:

- the request is for non-Korean law
- the user wants legal advice, litigation strategy, or a definitive legal conclusion
- the real task is plugin setup, architecture, or generic debugging

## Core Pattern

1. Classify the request first:
   - `pure legal lookup`: law/article text, annex, amendment history, or procedure lookup
   - `real-world situation`: facts, dispute risk, likely treatment, enforcement, or
     outcome-oriented questions about what happens in practice
2. Then classify the research need as one of: law/article, annex/form, decision search, or
   chain analysis.
3. Use the current `korean-law` MCP tool family:
   - `search_law` -> `get_law_text`
   - `get_annexes`
   - `search_decisions` -> `get_decision_text`
   - matching `chain_*` tool for procedure, amendment, penalty, ordinance, customs, or
     broader research
   - `discover_tools` -> `execute_tool` only when the exposed tools are still insufficient
4. For a `real-world situation`, retrieve both:
   - the governing law or article when available
   - directly relevant precedent, interpretation, appeal, or tribunal material when available
5. Quote concrete identifiers from the retrieved result, such as law name, article number,
   `mst`, `lawId`, decision domain, or decision id.
6. Answer using the appropriate shape from `## Answer Shape`.
7. If the primary MCP path is unavailable and a `beopmang` API or MCP is available in the
   session, use it only as a fallback. Do not assume fallback capability exists.
8. State clearly that the output is informational and may need professional legal review.

## Answer Shape

### Pure legal lookup

- Answer directly and compactly from the retrieved law, annex, amendment, or decision text.
- Do not force a two-part structure when the user is only asking for the rule text,
  procedure, or citation path.

### Real-world situation

- Split the answer into two labeled parts:
  - `General legal answer`
  - `Practical answer`
- `General legal answer`:
  - explain the governing rule from the law, decree, rule, annex, or formal interpretation
  - keep the answer at the principle level and identify the source clearly
- `Practical answer`:
  - ground it in directly relevant precedent, interpretation, appeal, or tribunal material
  - explain how the rule tends to be treated in practice based on that material
  - stay informational; do not turn it into litigation strategy or a guaranteed prediction
- Do not fill the practical answer with unsupported practice guesses.
- If you do not find directly relevant precedent, interpretation, appeal, or tribunal
  support, say that clearly and do not fill the practical answer with unsupported practice
  guesses.

## Quick Reference

| Need | Preferred path |
|------|----------------|
| Find a law | `search_law` |
| Read an article | `search_law` then `get_law_text` |
| Read an annex or form | `get_annexes` |
| Search precedents, interpretations, or appeals | `search_decisions` then `get_decision_text` |
| Track amendment history | `chain_amendment_track` |
| Explain legal structure or delegated rules | `chain_law_system` |
| Procedure, fees, forms, or manuals | `chain_procedure_detail` |
| Penalty, disposition, refusal basis | `chain_action_basis` |
| Ordinance comparison | `chain_ordinance_compare` |
| Niche domain not covered above | `discover_tools` then `execute_tool` |

## Common Mistakes

- Treating every legal question as if it needs the same answer shape
- Skipping the split between `General legal answer` and `Practical answer` for a real-world
  situation
- Using stale tool names from older docs instead of the current `search_decisions`,
  `get_decision_text`, `get_annexes`, and `chain_*` families
- Quoting an article before identifying the correct law via `search_law`
- Treating a remote endpoint as universally usable without checking API-key requirements
- Falling back to another source before trying the installed `korean-law` MCP path
- Filling the practical answer with unsupported real-world guesses when directly relevant
  supporting material was not found
- Presenting search results as legal advice instead of sourced legal information
