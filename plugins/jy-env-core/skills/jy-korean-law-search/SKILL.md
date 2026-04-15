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

1. Classify the request as one of: law/article, annex/form, decision search, or chain
   analysis.
2. Use the current `korean-law` MCP tool family:
   - `search_law` -> `get_law_text`
   - `get_annexes`
   - `search_decisions` -> `get_decision_text`
   - matching `chain_*` tool for procedure, amendment, penalty, ordinance, customs, or
     broader research
   - `discover_tools` -> `execute_tool` only when the exposed tools are still insufficient
3. Quote concrete identifiers from the retrieved result, such as law name, article number,
   `mst`, `lawId`, decision domain, or decision id.
4. If the primary MCP path is unavailable and a `beopmang` API or MCP is available in the
   session, use it only as a fallback. Do not assume fallback capability exists.
5. State clearly that the output is informational and may need professional legal review.

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

- Using stale tool names from older docs instead of the current `search_decisions`,
  `get_decision_text`, `get_annexes`, and `chain_*` families
- Quoting an article before identifying the correct law via `search_law`
- Treating a remote endpoint as universally usable without checking API-key requirements
- Falling back to another source before trying the installed `korean-law` MCP path
- Presenting search results as legal advice instead of sourced legal information
