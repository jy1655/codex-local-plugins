# Setup pstack for Codex

Configure optional role choices in `${CODEX_HOME:-$HOME/.codex}/pstack/models.json`.
This file affects only pstack invocations. Do not change global AGENTS.md, LOCAL.md,
Codex config.toml, plugin manifests, or Cursor rules. Defaults work without a file. Keep `speed: "standard"` unless the user explicitly
requests another speed; changing model or reasoning budget does not change speed.

1. Read the Codex runtime adapter and any existing models.json. Resolve available
   native models or locally authorized CLI providers from actual host metadata.
   Do not treat provider-looking strings as proof of availability.
2. Show the current roles and choices. If the user already supplied a valid mapping,
   apply it. Otherwise ask for provider/model and effort preferences using available
   question tools. The bundled defaults split code and judgment roles across Sol and Astra, with
   large/xhigh starting effort. Offer small/medium, medium/high, large/xhigh,
   or unlimited/max budgets using the exact mapping in the runtime adapter.
3. Keep the upstream role names below. Each role is one seat object, or a list for
   panels. Validate explicit models and effort against the chosen backend. `auto`
   and `inherit-parent` mean host inheritance, not a model identifier to send to a CLI.
4. Write only requested overrides in UTF-8 JSON. Preserve unmodified roles. On invalid
   existing JSON report the problem before replacing it; do not silently discard choices.
5. Report the saved path and actual choices. Changes apply to the next pstack invocation.
   Removing models.json restores bundled role defaults. Do not create an always-applied rule.

Example shape (the user may choose a supported CLI provider instead of native):

```json
{
  "speed": "standard",
  "roles": {
    "feature, refactoring": {"provider": "native", "model": "inherit-parent"},
    "interrogate reviewers": [
      {"provider": "native", "model": "inherit-parent"},
      {"provider": "native", "model": "inherit-parent"}
    ]
  }
}
```

Roles: `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`,
`judgment and prose`, `hardest tasks`, `how explorer`, `how explainer`,
`why investigators`, `why synthesizer`, `reflect tooling`,
`reflect judgment, divergent, synthesizer`, `arena runners`,
`arena cross-judge pool`, `swarm workers`, `architect runners`,
`interrogate reviewers`.

If the user also wants a project verification harness, route that separate request
through create-verification-skill. Setting model preferences alone does not create it.
