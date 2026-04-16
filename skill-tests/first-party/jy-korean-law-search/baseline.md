# Baseline Scenario

Goal: Observe what an agent does when asked for a real-world Korean legal question without
`jy-korean-law-search`.

Prompt:

```text
육아휴직 끝나고 복직시키긴 하는데 사실상 한직으로 보내려는 상황 같아.
법적으로는 뭐가 원칙이고, 실제 분쟁에서는 어떻게 보이는지도 같이 설명해줘.
```

Expected failure without the skill:

- Uses stale tool names from older Korean-law MCP docs
- Answers from memory without a current tool-routing plan
- Does not distinguish between statute text and decision search
- Does not distinguish a pure legal lookup from a real-world situation
- Blends rule explanation and practical outcome into one unsupported answer
- Does not mention concrete identifiers or domains to capture
- Guesses a practical outcome without directly relevant precedent or interpretation support
- Drifts into legal advice instead of search guidance
