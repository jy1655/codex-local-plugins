# Pstack help in Codex

Read ../../workflows.md for the complete bundled workflow index and ../poteto-mode/WORKFLOW.md
for routing. Explain usage in the user's language:

- `$pstack <task>` selects the matching poteto-mode playbook.
- `$pstack <workflow> <task>` selects a named workflow, such as how or interrogate.
- `$pstack setup-pstack` sets optional model roles; default execution inherits the parent.
- `$pstack poteto-help` shows this help.

Explain only the relevant recipes and reference the matching local workflow. This port
uses Codex host capabilities, not Cursor slash commands or the Cursor plugin installer.
Model-diverse panels require configured, available providers. Cloud automations and
Benny are not provisioned. See ../../../NOTICE.md for provenance and removal.
