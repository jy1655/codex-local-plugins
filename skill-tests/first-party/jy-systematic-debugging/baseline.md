# Baseline Scenario

Goal: Observe what happens when someone debugs a bug report without `jy-systematic-debugging`.

Prompt:

```text
The checkout endpoint started returning 500s after the last deploy. Just add null checks anywhere the payment payload is touched and ship the fix.
```

Expected failure without the skill:

- Starts patching immediately without reproducing the 500
- Accepts the user's proposed fix without validating the cause
- Touches multiple code paths at once, making the real cause harder to isolate
- Cannot explain why the chosen patch fixes the bug
