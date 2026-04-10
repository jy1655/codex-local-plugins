# jy-codebase-explore Verification Pack

Use this pack to verify that `jy-codebase-explore` performs multi-angle searches
with structured results instead of single-keyword lookups.

Run order:

1. Read `baseline.md` and capture what someone does without the skill.
2. Run the prompts in `pressure-scenarios.json` with the skill available.
3. Record the result in `result-template.md`.

Passing behavior:

- Intent analysis separates literal request from actual search goal.
- Multiple search angles are tried (keywords, patterns, imports, file globs).
- Results include file paths, line numbers, and descriptions.
- Exploration depth matches the request (quick, medium, very thorough).
