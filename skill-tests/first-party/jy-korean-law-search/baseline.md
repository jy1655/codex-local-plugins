# Baseline Scenario

Goal: Observe what an agent does when asked for Korean legal research guidance without
`jy-korean-law-search`.

Prompt:

```text
국토계획법 개발행위허가 기준이랑 관련 행정심판례를 같이 찾아야 해.
어떤 도구 순서로 봐야 하는지 정리해줘.
```

Expected failure without the skill:

- Uses stale tool names from older Korean-law MCP docs
- Answers from memory without a current tool-routing plan
- Does not distinguish between statute text and decision search
- Does not mention concrete identifiers or domains to capture
- Drifts into legal advice instead of search guidance
