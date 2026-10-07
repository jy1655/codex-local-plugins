# Upstream and port boundaries

These six skills and their supporting references are adapted from Matt Pocock's
MIT-licensed skills, version 1.2.3 at `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`.
`UPSTREAM.json` records the original paths and SHA-256 values, independently matched
against the upstream revision. `LICENSE` retains Matt Pocock's copyright and MIT terms.

The user selected architecture improvement and grilling after using them in Claude Code,
and explicitly requested functional preservation without simplification. This is an
adoption decision, not a measured Codex utility result. Other Matt Pocock workflows are
outside this pack.

Port changes are limited to:

- Codex descriptions and Korean interface metadata; the three entry points retain
  explicit-only invocation through `agents/openai.yaml` instead of Claude frontmatter.
- Skill-tool calls become relative links to the bundled skill instructions.
- Delegation and question presentation use available host capabilities and local policy.
- Architecture reports follow configured Wiki storage, with the original temporary
  directory fallback; report prose and HTML language follow the user's language.

The full interview rounds, confirmation before action, architecture exploration,
visual candidate report, candidate selection, parallel alternative designs, design
vocabulary, dependency categories, test guidance, inline CONTEXT.md updates, and ADR
criteria remain. The HTML scaffold and design/document formats are included in full.
This port retains the tested version's CONTEXT.md convention instead of upgrading to
the later GLOSSARY.md convention.
