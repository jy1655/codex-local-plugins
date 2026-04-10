---
name: jy-debugging
description: Use when debugging a bug, failing test, or unexpected behavior and you need verified root-cause analysis before patching.
---

# JY Debugging

## Overview

버그를 고칠 때는 추측 패치보다 재현과 원인 검증을 우선한다. 증상이 아니라 원인을 확인한 뒤에만
수정한다.

이 skill은 실행 지향적이다. Default mode에서는 재현, 로그 확인, 테스트 실행, 최소 수정까지
진행할 수 있고, Plan Mode에서는 디버깅 전략과 검증 순서만 남긴다.

## When to Use

- failing test가 생겼을 때
- 런타임 에러나 비정상 동작이 재현될 때
- 같은 증상에 대해 여러 번 추측 패치를 했는데 실패했을 때
- 사용자가 "일단 null check 더 넣어" 같은 shotgun 수정 압박을 줄 때
- flaky처럼 보이는 문제를 실제 flake인지 제품 버그인지 구분해야 할 때

## Quick Reference

| 단계 | 해야 할 일 | 금지 |
|------|------------|------|
| 재현 | 실패를 다시 만든다 | 재현 전 패치 |
| 범위 축소 | 언제/어디서 깨지는지 줄인다 | 전체 코드에 shotgun 수정 |
| 가설 | 가능한 원인을 1-3개 적는다 | 근거 없는 단정 |
| 검증 | 가설을 하나씩 prove/disprove 한다 | 여러 원인을 한 번에 고치기 |
| 최소 수정 | 입증된 원인만 고친다 | 증상 주변 대량 수정 |
| 검증 마감 | 재현 케이스와 회귀 체크를 다시 돌린다 | "아마 됐다" 선언 |

## Debug Loop

### 1. 재현

- 실패 테스트, 입력, 로그, 환경을 먼저 확보한다.
- 재현 명령이 없으면 가장 작은 재현 방법부터 만든다.
- 재현이 안 되면 "아직 재현되지 않았다"라고 명확히 말한다.

### 2. 범위 축소

- 언제부터 깨지는지, 특정 입력인지, 특정 모듈인지 줄인다.
- 필요한 경우 로그/출력/상태를 추가 관찰하되 한 번에 하나씩 본다.
- 증상 경로와 무관한 파일은 건드리지 않는다.

### 3. 가설 작성

- 관찰된 사실을 근거로 가설을 적는다.
- 가설은 "무엇이 잘못됐고 어떤 관찰이 이를 반증하는가"까지 포함한다.
- 가장 가능성 높은 순서로 정렬하되, 확정 표현은 금지한다.

### 4. 검증

- 가설마다 확인 명령, 로그 포인트, 또는 테스트를 정한다.
- 결과가 가설과 맞는지 기록하고 다음 가설로 넘어간다.
- 원인이 검증되기 전까지는 patch를 넣지 않는다.

### 5. 최소 수정

- 입증된 원인만 고친다.
- 수정은 가능한 가장 작은 단위로 한다.
- null check 추가, broad retry, sleep 삽입 같은 shotgun 처방은 마지막 수단이 아니라
  기본적으로 금지다.

### 6. 검증 마감

- 원래 재현 케이스를 다시 실행한다.
- 가능하면 회귀 테스트를 추가하거나 기존 테스트에 증상을 고정한다.
- 관련 테스트나 빌드를 다시 돌려 파손이 없는지 확인한다.

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- 재현, 로그 확인, 테스트 실행, 최소 수정, 재검증을 실제로 수행한다.

### If current collaboration mode is Plan

- 실제 디버깅 실행이나 파일 수정은 시작하지 않는다.
- 이렇게 유도한다:
  - "이건 실행형 debugging workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/jy-debugging`을 다시 실행하세요."
- 대신 재현 방법, 가설, 검증 순서를 compact하게 남긴다.
- Plan Mode 안에서 "지금 패치하겠다"라고 가장하지 않는다.

## Common Mistakes

- 재현 전에 코드를 고치기
- 증상 주변 전체에 null check나 retry를 뿌리는 shotgun patch
- 가설 없이 로그만 늘리기
- 여러 수정과 검증을 한 번에 섞어서 무엇이 효과였는지 모르게 만들기
- 원인 검증 없이 "flake 같다"로 넘기기
- 회귀 테스트 없이 수정만 하고 끝내기
- Plan Mode에서 실제 디버깅이 가능한 것처럼 행동하기
