# Baseline Scenario

Goal: Observe what an agent does when asked for strategic advice without `jy-oracle-consult`.

Prompt:

```text
I've tried fixing this race condition twice and failed both times.
The websocket handler and the REST endpoint both write to the same cache.
What should I do?
```

Expected failure without the skill:

- Jumps straight to code modification instead of analyzing the problem
- Does not structure the analysis (problem, options, tradeoffs, recommendation)
- Gives a single suggestion without considering alternatives
- Does not ask for or reference the actual code involved
- Ends with vague advice like "you should use locks" without specifics
