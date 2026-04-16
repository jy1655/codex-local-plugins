# jy-korean-law-search Verification Pack

Use this pack to verify that `jy-korean-law-search` routes Korean legal queries to the
current `korean-law` MCP tool families instead of stale tool names or memory-only answers.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- The agent classifies the request before choosing a tool path.
- The agent distinguishes a `pure legal lookup` from a `real-world situation`.
- For a pure legal lookup, the agent answers directly and does not force the
  `General legal answer` / `Practical answer` split.
- The agent prefers the installed `korean-law` MCP server and uses current tool names.
- The answer cites concrete law or decision identifiers from retrieved results.
- For a real-world situation, the answer separates `General legal answer` from
  `Practical answer`.
- The `Practical answer` stays tied to directly relevant precedent, interpretation, appeal,
  or tribunal material.
- If directly relevant support is missing, the agent says so and does not guess a practical
  outcome.
- Fallback behavior is conservative: `beopmang` is used only if available and only after the
  primary path is unavailable.
- The answer stays informational and does not present itself as legal advice.
