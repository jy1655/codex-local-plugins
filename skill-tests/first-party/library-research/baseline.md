# Baseline Scenario

Goal: Observe what an agent does when asked about an unfamiliar library without `library-research`.

Prompt:

```text
I need to use the Zod library for runtime validation in this TypeScript project.
How does discriminated union parsing work in Zod v4?
Show me how it differs from v3.
```

Expected failure without the skill:

- Provides an answer based on training data without checking current documentation
- Does not link to official docs or source code
- Mixes up v3 and v4 APIs without clear distinction
- Does not provide GitHub permalinks to the actual source
- Gives a generic tutorial instead of connecting to the current project
