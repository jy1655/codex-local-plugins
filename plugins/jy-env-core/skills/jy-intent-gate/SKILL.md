---
name: jy-intent-gate
description: Use when a user request is ambiguous and needs intent classification before choosing an action strategy.
---

# JY Intent Gate

## Overview

사용자 요청의 진짜 의도를 분류한 뒤 적절한 전략으로 라우팅한다. 문자 그대로의 해석이 아닌 실제 의도를 파악하는 것이 핵심. 분류 없이 바로 행동하면 잘못된 방향으로 시간을 낭비한다.

이 skill은 Codex의 current collaboration mode도 같이 고려해야 한다. planning 경로가 맞아도
skill 자체가 Plan Mode를 켜지는 못하고, execution 경로가 맞아도 Plan Mode 안에서 실행을
가짜로 시작하면 안 된다.

## When to Use

- 요청이 여러 의도로 해석 가능할 때
- "이거 해줘"처럼 모호한 요청
- 리서치인지 구현인지 불분명할 때
- 복합 요청 (조사 + 수정 + 검증이 섞인 경우)

사용하지 않을 때: 의도가 명확한 단순 요청 ("이 함수 이름 바꿔줘", "테스트 돌려줘")

## Quick Reference

| 의도 유형 | 신호 | 전략 |
|----------|------|------|
| **Research** | "어떻게 동작해?", "뭐가 최선이야?" | 코드 읽기 → 분석 → 설명. 수정 금지 |
| **Implementation** | "만들어줘", "추가해줘", "구현해줘" | 계획 → 구현 → 검증 |
| **Investigation** | "왜 깨져?", "원인이 뭐야?" | 증상 수집 → 가설 → 증거 확인 |
| **Fix** | "고쳐줘", "에러 수정", 스택트레이스 첨부 | 재현 → 근본 원인 → 최소 수정 → 검증 |
| **Evaluation** | "이거 괜찮아?", "리뷰해줘", "비교해줘" | 기준 설정 → 다각도 분석 → 판정 |
| **Refactoring** | "정리해줘", "리팩토링", "구조 개선" | 동작 보존 확인 → 점진적 변경 → 검증 |

## Mode-Aware Behavior

### If current collaboration mode is Default

- 먼저 intent를 분류한다.
- 분류 결과가 planning 계열이면:
  - 적절한 planning skill을 고른다.
  - "이건 Plan Mode가 맞습니다. `Shift+Tab`으로 Plan Mode로 바꾼 뒤 `/{skill-name}`를 다시 실행하세요."라고 유도한다.
  - 동시에 가능한 최소 draft brief 또는 draft plan summary는 남긴다.
- 분류 결과가 execution 계열이면 Default mode에서 계속 진행한다.

### If current collaboration mode is Plan

- planning 계열 분류면 그대로 Plan Mode에서 이어간다.
- execution-heavy 분류면 mode mismatch를 명시한다.
  - 예: 구현, fix, 실제 review 실행
  - 이 경우 "이건 Plan Mode보다 Default mode가 맞습니다. `Shift+Tab`으로 빠져나간 뒤 다시 실행하세요."라고 유도한다.
- Plan Mode 안에서 실행을 가장해 파일 수정이나 테스트 실행을 약속하지 않는다.

## 분류 프로세스

### Step 1: 문자 vs 의도 분리

```
문자적 요청: 사용자가 말한 것 그대로
실제 의도: 사용자가 달성하려는 것
```

예시:
- 문자: "이 코드 설명해줘" → 의도: Research (이해하고 싶다)
- 문자: "이 코드 봐줘" → 의도: Evaluation (품질 판단 원함) 또는 Fix (문제 의심)
- 문자: "이거 해줘" + 스택트레이스 → 의도: Fix (에러 해결)

### Step 2: 복합 의도 분해

하나의 요청에 여러 의도가 섞이면 분해:

```
"이 API가 왜 느린지 알아보고 고쳐줘"
→ Investigation (원인 파악) → Fix (수정)
→ 순서: 조사 먼저, 원인 확인 후 수정
```

### Step 3: 전략 선택 후 실행

분류 결과를 명시하고 해당 전략을 따른다. 분류가 불확실하면 사용자에게 확인.

```
의도: [Investigation → Fix]
전략: 먼저 증상을 수집하고 가설을 세운 뒤, 원인이 확인되면 최소 수정을 적용합니다.
```

### Step 4: 모드와 전략의 정합성 확인

- planning 전략인데 Default mode면 Plan Mode 전환을 안내한다.
- execution 전략인데 Plan Mode면 Default mode 복귀를 안내한다.
- mode와 전략이 맞으면 그대로 진행한다.

## Common Mistakes

- skill이 collaboration mode까지 자동으로 바꿀 수 있다고 가정하는 것
- Plan Mode인데 implementation/fix/review 실행을 그대로 시작하는 것
- Default mode인데 planning 질문 흐름이 필요한 요청을 그냥 실행으로 밀어붙이는 것
- 분류 없이 바로 구현 시작 — "만들어줘"가 아닌 요청에 코드부터 작성
- 문자적 해석만 적용 — "봐줘"를 항상 코드 리뷰로 처리 (실제로는 디버깅 요청일 수 있음)
- Research 의도에 코드 수정 — 설명만 원하는데 리팩토링까지 수행
- 복합 의도를 한 가지로 축소 — "조사하고 고쳐줘"에서 조사를 건너뛰고 바로 수정
- 모든 요청에 분류 적용 — 명확한 단순 요청에 불필요한 분류 단계 추가
