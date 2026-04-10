# jy-library-research Verification Pack

Use this pack to verify that `jy-library-research` provides evidence-based answers
with source links instead of unsourced guesses.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- All claims are backed by documentation links, GitHub permalinks, or issue references.
- Requests are classified by type (concept, source, implementation, debug) before research.
- Answers are connected to the current project context, not generic tutorials.
- The agent does not modify code during research.
