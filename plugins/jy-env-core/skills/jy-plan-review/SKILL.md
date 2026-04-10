---
name: jy-plan-review
description: Use when a plan exists and needs to be made decision-complete across product, architecture, UX, and delivery concerns.
---

# JY Plan Review

## Overview

이미 존재하는 계획을 읽고, 구현자가 추가 결정을 하지 않아도 되도록 빈칸을 메우는 first-party
plan review skill. 제품 범위, 기술 구조, UX/DX 영향, 검증 기준을 한 번에 점검하고,
필요하면 다음 handoff를 `jy-writing-plans`로 연결한다.

이 skill은 Codex의 collaboration mode를 인식해야 한다. decision-complete plan을 완성하려면
대개 Plan Mode가 더 적합하지만, skill 자체가 모드를 바꾸지는 못한다.

## When to Use

- 구현 전에 계획을 잠그고 싶을 때
- "이 계획 검토해줘", "빠진 결정이 뭐지", "이대로 구현 가능해?" 같은 요청
- 여러 관점의 review를 하나의 Codex-native workflow로 통합하고 싶을 때

사용하지 않을 때:
- 아직 문제 정의 자체가 흔들리는 경우
- 코드 diff 리뷰가 필요한 경우

## Quick Reference

| 단계 | 행동 |
|------|------|
| 0. 모드 확인 | Default인지 Plan인지 먼저 판단 |
| 1. plan 읽기 | 계획 초안과 관련 repo 규칙 파악 |
| 2. 공백 찾기 | 구현자가 막힐 결정 누락 식별 |
| 3. finding 정리 | severity 순으로 정리 |
| 4. plan 보강 | missing decision을 메운 revised plan 작성 |
| 5. 검증 잠금 | acceptance criteria와 시작 조건 명시 |

## Expected Inputs

- plan 문서 또는 사용자 메시지의 계획 초안
- 관련 repo 규칙과 기존 구조
- 명시된 제약: 일정, 호환성, 비기능 요구사항

## Expected Output

- 우선순위 순의 findings
- 계획에 추가되어야 할 결정 목록
- 결정이 반영된 revised plan
- 구현 시작 전 acceptance criteria
- 다음 handoff (`jy-writing-plans` 또는 바로 구현)

## Review Dimensions

- scope and non-goals
- data flow and interfaces
- UX or operator touchpoints
- failure modes and rollback thinking
- test and verification coverage
- migration or compatibility impact

## Mode-Aware Behavior

### If current collaboration mode is Default

- 계획 검토가 한 번 답변으로 끝날 수 있는지 먼저 판단한다.
- 공백이 많아서 질문 왕복이 필요하면 이렇게 유도한다:
  - "이건 Plan Mode로 잠그는 게 맞습니다. `Shift+Tab`으로 Plan Mode로 바꾼 뒤 `/jy-plan-review`를 다시 실행하세요."
- 동시에 현재 보이는 핵심 finding 3-5개와 간단한 draft revised plan은 남긴다.
- plan은 승인 가능한데 implementer용 task breakdown이 없으면 `jy-writing-plans`를 다음 단계로 명시한다.
- Default mode에서는 `<proposed_plan>`이나 Plan 전용 질문 흐름을 전제로 하지 않는다.

### If current collaboration mode is Plan

- 빠진 결정을 질문으로 잠근다.
- 결과를 implementer가 그대로 집을 수 있는 수준까지 채운다.
- 최종 계획은 `<proposed_plan>` 블록으로 정리한다.
- taskized implementation plan이 아직 아니면 `jy-writing-plans` handoff를 명시한다.

## Workflow

1. 현재 collaboration mode가 Default인지 Plan인지 확인한다.
2. 계획과 현재 repo 문맥을 읽는다.
3. 구현자가 막힐 결정 공백을 찾는다.
4. finding을 severity 순으로 정리한다.
5. 누락된 결정을 메운 revised plan 형태로 다시 쓴다.
6. 구현 시작 조건과 검증 기준을 명시한다.
7. taskized plan이 아직 아니면 다음 단계로 `jy-writing-plans`를 남긴다.

## Boundaries

- 코드 작성 금지
- 외부 runtime, review 로그, hidden telemetry 전제 금지
- 결과는 다른 구현자가 바로 이어받을 수 있는 plan 형태여야 한다

## Common Mistakes

- skill이 Plan Mode를 자동으로 켤 수 있다고 가정하는 것
- Default mode인데 바로 긴 질문 세션으로 들어가는 것
- 좋은 아이디어인지 평가만 하고 구현 결정을 잠그지 않는 것
- architecture만 보고 UX, migration, 검증 기준을 빼먹는 것
- finding은 적었지만 revised plan으로 다시 써주지 않는 것
- reviewed plan은 만들었지만 implementer가 그대로 실행할 task breakdown이 필요하다는 점을 명시하지 않는 것
- implementer가 다시 질문해야 하는 상태로 끝내는 것
