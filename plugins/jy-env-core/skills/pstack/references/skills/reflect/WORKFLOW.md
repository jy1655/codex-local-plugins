# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "$pstack reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Resolve this conversation using the Codex runtime adapter's history procedure.
Use a known transcript path and verify its session and workspace metadata before
reading content. If it is unavailable, supply a concise digest of this session
and label the evidence limit. Do not guess a layout or scan unrelated chats.

## 2. Spawn three reviewers in parallel

Launch three independent reviewers through the runtime adapter, each with read-only scope and any actually available read-only MCP tools.

Use the named role from the merged bundled defaults and optional pstack/models.json overrides. Resolve and validate models through the Codex runtime adapter; report unavailable models and diversity gaps. Every investigator and reviewer has read-only scope, including MCP calls. Use only tools actually available to that child.

| Lens | Role line | Default `model` | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | Runtime role registry | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | Runtime role registry | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | Runtime role registry | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `Task` response body.

## 3. Synthesize

One `Task` call, `subagent_type: generalPurpose`, `model` from the `reflect judgment, divergent, synthesizer` line (default from the runtime role registry), read-only scope. It spot-verifies citations using available tools. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Keep Backlog items in the report. File them externally only when the user has authorized that action.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the available `skill-creator` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
