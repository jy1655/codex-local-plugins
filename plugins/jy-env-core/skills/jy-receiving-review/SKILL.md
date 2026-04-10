---
name: jy-receiving-review
description: Use when review feedback, PR comments, or requested fixes need verification against the codebase before code changes are made.
---

# JY Receiving Review

## Overview

리뷰 코멘트는 그대로 복종하는 지시가 아니라, 실제 코드베이스와 대조해 검증해야 하는 입력이다.
핵심 원칙은 social performance가 아니라 technical evaluation이다.

특히 `performative agreement`를 금지한다. 맞는 피드백은 검증 후 반영하고, 틀린 피드백은
`기술적 반박`으로 정리한다.

## When to Use

- "리뷰 반영해", "PR 코멘트 처리해", "이 피드백 맞는지 보고 수정해"
- reviewer가 여러 개의 수정 요청을 남겼을 때
- 외부 리뷰어의 제안이 현재 구현과 충돌할 수 있을 때

사용하지 않을 때:

- 리뷰가 아니라 신규 구현 요청인 경우
- 이미 검증된 수정 항목을 단순 적용만 하면 되는 경우

## Quick Reference

| 단계 | 행동 |
|------|------|
| 0. 모드 확인 | Default인지 Plan인지 먼저 판단 |
| 1. triage | 피드백을 clear / unclear / disputed로 분류 |
| 2. 검증 | 각 항목을 실제 코드베이스와 대조 |
| 3. 질문 또는 반박 | 명확하지 않은 항목은 질문, 틀린 항목은 기술적으로 반박 |
| 4. 구현 | 맞는 항목만 순서대로 반영 |
| 5. 검증 | 반영 결과를 fresh evidence로 확인 |

## Feedback Triage

- clear: 의도와 수정 위치가 명확하다
- unclear: 요구사항이 `명확하지` 않거나 항목 간 의존성이 있다
- disputed: 현재 코드베이스, 요구사항, 호환성 기준과 충돌한다

clear가 아닌 항목은 바로 구현하지 않는다.

## Verification Rules

- 각 항목을 실제 코드베이스와 대조한다
- reviewer 설명이 맞는지, 이미 해결됐는지, 다른 제약과 충돌하는지 확인한다
- multi-item feedback에서 일부가 `명확하지` 않으면 그 항목을 분리해서 질문한다
- external reviewer의 제안은 자동으로 맞다고 가정하지 않는다

## Response Rules

금지:

- `performative agreement`
- "맞습니다, 바로 고치겠습니다" 같은 무검증 수용
- unclear item이 남아 있는데 일부만 먼저 구현하는 것

허용:

- 검증 후 바로 수정
- 필요한 clarification 요청
- 테스트와 코드 근거를 바탕으로 한 `기술적 반박`

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- triage, 코드베이스 검증, clarification, 수정, 최종 verification까지 실제로 수행한다.

### If current collaboration mode is Plan

- 실제 수정은 하지 않는다.
- 이렇게 유도한다:
  - "이건 리뷰 반영 실행 workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/jy-receiving-review`를 다시 실행하세요."
- 대신 triage와 missing clarification 목록은 남긴다.

## Workflow

1. 현재 collaboration mode가 Default인지 Plan인지 확인한다.
2. 리뷰 피드백을 clear / unclear / disputed로 분류한다.
3. 각 항목을 코드베이스와 대조한다.
4. unclear item은 질문으로, disputed item은 근거 있는 `기술적 반박`으로 정리한다.
5. 맞는 항목만 구현한다.
6. 마지막에는 변경 결과를 fresh verification으로 닫는다.

## Common Mistakes

- `performative agreement`로 검증 없이 수용하는 것
- 실제 코드베이스를 보지 않고 reviewer 설명만 믿는 것
- `명확하지` 않은 항목을 남긴 채 일부만 먼저 구현하는 것
- reviewer가 틀렸는데도 반박 근거 없이 따라가는 것
- 반영 후 검증 없이 "리뷰 반영 완료"라고 말하는 것
- Plan Mode에서 실제 수정이 진행된 것처럼 말하는 것
