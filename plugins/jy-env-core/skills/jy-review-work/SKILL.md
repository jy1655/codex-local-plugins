---
name: jy-review-work
description: Use when implementation is complete and needs multi-angle review before merging or handing off.
---

# JY Review Work

## Overview

구현 완료 후 5개 병렬 서브에이전트로 다각도 리뷰를 실행하는 워크플로우. 단일 리뷰어가 놓치는 맹점을 병렬 전문가가 커버한다. 5개 전부 통과해야 리뷰 통과.

이 skill은 실행 지향적이다. 실제 리뷰 실행, 테스트, QA는 보통 Default mode에서 수행해야 하며,
skill 자체가 Plan Mode를 전환할 수는 없다.

## When to Use

- 기능 구현이 끝나고 머지/핸드오프 직전
- "리뷰해줘", "검증해줘", "QA 돌려줘" 요청 시
- 대규모 변경(3+ 파일) 완료 후

사용하지 않을 때: 1-2줄 수정, 설정 변경, 문서 수정

## Quick Reference

| 단계 | 행동 |
|------|------|
| 0. 모드 확인 | 현재가 Default인지 Plan인지 먼저 판단 |
| 1. 컨텍스트 수집 | diff, 변경 파일, 목표, 제약조건, 실행 명령 파악 |
| 2. 5개 에이전트 병렬 실행 | 전부 `run_in_background=true`, 한 턴에 실행 |
| 3. 결과 수집 | 5개 전부 완료 대기 |
| 4. 판정 | 1개라도 FAIL이면 전체 FAIL |

## 5개 에이전트 구성

| # | 역할 | 초점 | 모드 |
|---|------|------|------|
| 1 | Goal Verifier | 원래 요청과 제약 충족 여부 | 읽기 전용 분석 |
| 2 | QA Executor | 실제 실행/테스트 수행 | 도구 사용 가능 |
| 3 | Code Reviewer | 코드 품질, 패턴 일관성 | 읽기 전용 분석 |
| 4 | Security Auditor | OWASP top 10, 인젝션, 시크릿 노출 | 읽기 전용 분석 |
| 5 | Context Miner | git 히스토리, 관련 이슈, 누락된 맥락 | 도구 사용 가능 |

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- 컨텍스트를 수집하고 5개 에이전트를 병렬 실행한다.
- 실제 실행, 테스트, QA, 결과 집계를 여기서 수행한다.

### If current collaboration mode is Plan

- 실제 multi-agent review 실행은 시작하지 않는다.
- 이렇게 유도한다:
  - "이건 실행형 review workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 `/jy-review-work`를 다시 실행하세요."
- 사용자가 review 전략만 원한다면 compact checklist만 준다.
- Plan Mode 안에서 "지금 5개 에이전트를 돌리겠다"라고 가장하지 않는다.

## Phase 0: 컨텍스트 수집

리뷰 시작 전 반드시 수집:

```bash
# 변경 파일 목록
git diff --name-only HEAD~1

# 전체 diff
git diff HEAD~1

# 실행 방법 탐지
# package.json scripts, Makefile, docker-compose.yml 확인
```

대화 히스토리에서 추출: 원래 목표, 제약조건, 배경. 명확하지 않으면 한 가지만 질문.

Plan Mode라면 여기까지를 preview로만 수행하고, 실제 에이전트 실행은 하지 않는다.

## Phase 1: 병렬 실행

5개 에이전트를 **반드시 한 턴에** 전부 실행. 순차 실행 금지.

읽기 전용 에이전트(1, 3, 4)에게는 diff + 파일 전문을 프롬프트에 포함. 도구 사용 에이전트(2, 5)에게는 목표와 포인터만 전달.

각 에이전트 프롬프트에 포함할 것:
- 원래 목표와 제약조건
- 변경 파일 목록
- 해당 에이전트의 판정 기준 (PASS/FAIL 조건)

## Phase 2-3: 수집과 판정

모든 에이전트 완료 후 결과를 표로 정리:

```markdown
| # | 역할 | 판정 | 핵심 발견 |
|---|------|------|----------|
| 1 | Goal Verifier | PASS/FAIL | ... |
| 2 | QA Executor | PASS/FAIL | ... |
| 3 | Code Reviewer | PASS/FAIL | ... |
| 4 | Security Auditor | PASS/FAIL | ... |
| 5 | Context Miner | PASS/FAIL | ... |
```

**1개라도 FAIL이면 전체 FAIL.** FAIL 항목의 구체적 수정 사항을 목록으로 제시.

## Common Mistakes

- Plan Mode에서 실제 review execution이 가능한 것처럼 행동하는 것
- `Shift+Tab`으로 Default mode 복귀 안내 없이 실행형 workflow를 시작하는 것
- 5개를 순차로 실행해서 시간 낭비 — 반드시 병렬
- 읽기 전용 에이전트에 파일 전문을 안 넣어서 "파일을 읽을 수 없다"는 응답 — diff + 전문 포함
- 1-2줄 수정에 5개 에이전트를 돌리는 과잉 — When to Use 확인
- FAIL 결과를 무시하고 "대부분 통과했으니 OK" — 1개라도 FAIL이면 전체 FAIL
- 컨텍스트 수집 없이 바로 에이전트 실행 — Phase 0 필수
