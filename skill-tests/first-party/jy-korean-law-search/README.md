# jy-korean-law-search Verification Pack

Use this pack to verify that `jy-korean-law-search` routes Korean legal queries to the
current `korean-law` MCP tool families instead of stale tool names or memory-only answers.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- The agent classifies the request before choosing a tool path.
- The agent prefers the installed `korean-law` MCP server and uses current tool names.
- The answer cites concrete law or decision identifiers from retrieved results.
- Fallback behavior is conservative: `beopmang` is used only if available and only after the
  primary path is unavailable.
- The answer stays informational and does not present itself as legal advice.
