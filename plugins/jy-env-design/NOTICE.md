# Upstream and port boundaries

The original six skills and their supporting references are adapted from Matt Pocock's
MIT-licensed skills, version 1.2.3 at `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`.
`UPSTREAM.json` records the original paths and SHA-256 values, independently matched
against the upstream revision. `LICENSE` retains Matt Pocock's copyright and MIT terms.

The user selected architecture improvement and grilling after using them in Claude Code,
and explicitly requested functional preservation without simplification. This is an
adoption decision, not a measured Codex utility result. Other Matt Pocock workflows are
outside this pack unless separately selected, as with retro below.

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

## Retro addition (2026-10-23)

The user separately selected `retro` with functional preservation. Retro and its complete
`writing-for-agents` reference (including `SKILL-MECHANICS.md`) come from version 1.3.1 at
`5beb35b040e3de97e54fa9e386d7e42d15c295c2`. `UPSTREAM.json` records these under
`additional_imports` with original SHA-256 values and local paths. The MIT license is
unchanged. This addition does not upgrade the original six skills.

The retrospective steps, seven improvement categories, severity ordering, implementation
versus review distinction, and file guidance are retained. Port changes are limited to:

- Codex trigger wording, Korean UI metadata, and the original explicit-only invocation
  policy in `agents/openai.yaml` instead of Claude frontmatter.
- The `writing-for-agents` Skill-tool call becomes a link to the complete bundled
  reference. Its frontmatter is removed because it is reference material, not another
  independently discoverable skill; skill mechanics remains a conditional relative link.
- Skill-mechanics backlinks follow the reference filename, and invocation-setting
  examples use Codex's `policy.allow_implicit_invocation` equivalent.

Retro returns improvement candidates; adopting it does not authorize applying those
candidates. Actual model-run fidelity is distinct from source preservation and packaging
validation.
