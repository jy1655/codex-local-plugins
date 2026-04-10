---
name: jy-verification-before-completion
description: Use when about to claim work is complete, fixed, or passing and you need fresh verification evidence first.
---

# JY Verification Before Completion

## Overview

완료 주장, 수정 완료, 테스트 통과 같은 표현은 fresh verification evidence 없이 말하지 않는다.
증거가 없으면 성공이 아니라 미검증 상태다.

이 skill은 실행 지향적이다. Default mode에서는 실제 검증 명령을 돌리고 결과를 읽는다. Plan Mode에서는
검증 체크리스트와 필요한 명령만 남기고 완료 주장은 하지 않는다.

## When to Use

- "done", "fixed", "passes", "ready" 같은 완료 주장 직전
- 커밋, 푸시, 핸드오프, PR 설명 직전
- 서브에이전트나 다른 도구가 성공했다고 보고했을 때
- 테스트 일부만 돌렸는데 전체 상태를 말해야 할 때

## Quick Reference

| 주장 | 필요한 증거 | 불충분한 것 |
|------|-------------|-------------|
| 테스트 통과 | fresh test command output | 이전 실행 기억 |
| 버그 수정 | 원래 증상 재검증 | 코드가 바뀌었다는 사실 |
| 빌드 성공 | fresh build output | lint 통과 |
| 작업 완료 | 요구사항 체크 + 검증 결과 | "아마 된다"는 판단 |

## Verification Gate

1. Identify: 지금 하려는 완료 주장이 무엇인지 적는다.
2. Select: 그 주장을 입증하는 가장 직접적인 명령을 고른다.
3. Run: 명령을 fresh하게 다시 실행한다.
4. Read: exit code, 실패 수, 경고, 실제 출력 요약을 읽는다.
5. Report: 증거와 함께 상태를 말한다.

명령을 아직 돌리지 않았다면 성공 표현 대신 `not run` 또는 미검증 상태라고 명시한다.

## Reporting Rules

- 검증 성공이면: 어떤 명령을 돌렸고 무엇이 통과했는지 함께 말한다.
- 검증 실패면: 실패를 숨기지 않고 실제 상태를 그대로 말한다.
- 검증 미실행이면: 완료 주장 대신 아직 검증하지 않았다고 말한다.
- 다른 에이전트의 성공 보고는 증거가 아니라 입력일 뿐이다. 직접 다시 검증한다.

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- 필요한 검증 명령을 실제로 실행하고 결과를 읽은 뒤 상태를 보고한다.

### If current collaboration mode is Plan

- 실제 테스트, 빌드, 실행 검증을 돌리지 않는다.
- 이렇게 유도한다:
  - "이건 실행형 verification workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/jy-verification-before-completion`을 다시 실행하세요."
- 대신 어떤 완료 주장에 어떤 명령이 필요한지 verification checklist만 남긴다.
- Plan Mode 안에서 fresh verification evidence가 있는 것처럼 가장하지 않는다.

## Common Mistakes

- 이전 테스트 결과를 fresh evidence처럼 인용하기
- 일부 테스트만 돌리고 전체가 통과했다고 말하기
- 서브에이전트 보고를 그대로 믿고 완료 주장하기
- 빌드를 안 돌렸는데 lint 결과만으로 성공을 말하기
- 검증이 없는데도 "should", "probably", "looks good"로 완료를 암시하기
- 검증을 안 돌렸으면서 `not run`이라고 솔직히 말하지 않기
