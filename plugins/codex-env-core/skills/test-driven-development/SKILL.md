---
name: test-driven-development
description: Use when starting a feature, bugfix, or behavior change and you need a failing test first before implementation.
---

# Test-Driven Development

## Overview

기능 구현이나 버그 수정은 failing test first 원칙으로 시작한다. 테스트가 먼저 깨지는 것을 보지
않았다면, 그 테스트가 무엇을 보호하는지 아직 모르는 상태다.

이 skill은 실행 지향적이다. Default mode에서는 테스트 작성과 실행, 최소 구현, 리팩터링까지
진행하고, Plan Mode에서는 테스트 전략까지만 남긴다.

## When to Use

- 새 기능 구현
- 버그 수정
- 동작 변경이 있는 리팩터링
- 테스트를 먼저 설계해야 요구사항이 선명해지는 작업

사용하지 않을 때:

- 문서 전용 변경
- 순수 계획 작업
- 동작 변화가 없는 메타데이터나 주석 정리

## Quick Reference

| 단계 | 해야 할 일 | 확인 포인트 |
|------|------------|-------------|
| RED | 가장 작은 failing test를 쓴다 | 기대한 이유로 실패하는가 |
| GREEN | 최소 구현으로 통과시킨다 | 새 테스트와 관련 테스트가 통과하는가 |
| REFACTOR | 구조만 정리한다 | 동작은 그대로인가 |
| 반복 | 다음 행동을 다시 RED로 시작한다 | 한 번에 한 행동만 추가하는가 |

## Red-Green-Refactor

### 1. RED

- 가장 작은 사용자-visible behavior 하나를 고른다.
- 그 동작만 드러내는 테스트를 추가한다.
- 테스트 이름은 행동을 설명해야 한다.
- 테스트를 실행해서 기대한 이유로 실패하는지 확인한다.

### 2. GREEN

- 방금 추가한 failing test를 통과시키는 최소 구현만 넣는다.
- 설계 확장이나 미래 요구사항 대비 코드는 넣지 않는다.
- 새 테스트와 직접 영향권 테스트를 다시 실행한다.

### 3. REFACTOR

- 중복 제거, 이름 개선, 작은 구조 정리만 한다.
- 동작을 바꾸는 새 기능 추가는 금지다.
- 리팩터링 후에도 테스트를 다시 돌린다.

## Guardrails

- production code를 테스트보다 먼저 쓰지 않는다.
- 이미 구현이 끝난 뒤 테스트를 추가하는 것은 retrofitted testing이지 TDD가 아니다.
- 사용자가 "테스트는 마지막에"라고 압박해도 먼저 가장 작은 failing test를 찾는다.
- 테스트가 이미 통과하면 기존 동작을 다시 확인하는 것이지 새 동작을 보호한 것이 아니다. test를
  더 좁히거나 입력을 바꿔 실제로 깨뜨려야 한다.

## If Code Already Exists

- 이미 production code를 쓴 상태라면 그것을 TDD였다고 포장하지 않는다.
- 가능한 경우: 구현을 멈추고 원하는 동작을 기준으로 failing test first 순서로 다시 시작한다.
- 다시 시작할 수 없는 경우: "지금부터는 TDD가 아니라 후행 테스트 보강"이라고 명확히 말하고
  검증 범위를 줄이지 않는다.

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- 테스트 작성, RED 확인, 구현, GREEN 확인, REFACTOR를 실제로 수행한다.

### If current collaboration mode is Plan

- 실제 테스트 작성이나 production code 수정은 시작하지 않는다.
- 이렇게 유도한다:
  - "이건 실행형 TDD workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/test-driven-development`를 다시 실행하세요."
- 대신 가장 작은 failing test 후보, 예상 검증 명령, 구현 순서를 compact하게 남긴다.
- Plan Mode 안에서 TDD를 이미 시작한 것처럼 가장하지 않는다.

## Common Mistakes

- 테스트보다 production code를 먼저 쓰기
- 실패를 확인하지 않고 바로 구현하기
- 한 테스트에 여러 행동을 묶기
- mock만 검증하고 실제 동작은 검증하지 않기
- 이미 작성한 구현 뒤에 테스트를 붙이고 TDD라고 부르기
- RED 없이 GREEN만 확인하고 끝내기
- Plan Mode에서 실제 구현을 진행하는 것처럼 말하기
