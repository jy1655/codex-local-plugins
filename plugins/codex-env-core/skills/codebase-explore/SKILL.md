---
name: codebase-explore
description: Use when multiple modules are involved in a search or the codebase structure is unfamiliar and needs multi-angle exploration.
---

# Codebase Explore

## Overview

현재 프로젝트 코드베이스를 다각도로 탐색하여 구조, 패턴, 의존 관계를 파악한다.
단일 키워드 검색으로 부족할 때, 여러 검색 각도를 병렬로 돌려 전체 그림을 잡는다.

## When to Use

- "X가 어디에 구현되어 있지?", "Y를 하는 코드 찾아줘"
- 2개 이상 모듈이 관련된 탐색
- 익숙하지 않은 모듈 구조를 파악해야 할 때
- 교차 레이어 패턴 발견 (API → 서비스 → DB)

사용하지 않을 때:
- 정확히 어떤 파일/심볼을 찾는지 알 때 (직접 grep/glob)
- 단일 키워드로 충분한 검색
- 외부 라이브러리 조사 (library-research 사용)

## Quick Reference

| 단계 | 행동 |
|------|------|
| 1. 의도 분석 | 문자적 요청과 실제 탐색 목표 분리 |
| 2. 검색 전략 | 다각도 검색 키워드와 패턴 수립 |
| 3. 병렬 탐색 | 여러 검색을 동시 실행 |
| 4. 결과 정리 | 파일 경로 + 라인 + 발견 요약 |

## Exploration Protocol

### Step 1: 의도 분석

탐색 시작 전, 문자적 요청과 실제 목표를 분리:

```
문자적 요청: [사용자가 말한 것]
실제 탐색 목표: [찾아야 하는 것]
검색 각도: [시도할 키워드/패턴 목록]
```

### Step 2: 다각도 검색

단일 키워드에 의존하지 않는다:
- 함수명, 클래스명, 타입명
- 에러 메시지, 로그 문자열
- 파일 패턴 (glob)
- import/require 경로
- 주석, 문서 내 키워드

### Step 3: 결과 구조화

모든 결과를 실행 가능한 형태로 정리:

```markdown
### 발견

| 파일 | 라인 | 설명 |
|------|------|------|
| src/auth/handler.ts | 42 | 인증 미들웨어 진입점 |
| src/db/users.ts | 15 | 사용자 조회 쿼리 |

### 구조 요약

auth → handler.ts → users.ts → session.ts
```

### Step 4: 탐색 깊이

요청 시 명시된 깊이를 따른다:
- **quick**: 기본 검색 1-2회
- **medium**: 다각도 검색 + import 추적
- **very thorough**: 교차 레이어 분석 + 의존 그래프

명시 없으면 medium으로 시작.

## Common Mistakes

- 단일 키워드만 검색하고 끝내는 것 — 다각도 검색 필수
- 파일 경로만 나열하고 라인 번호와 설명을 빼는 것 — 실행 가능한 결과
- 외부 라이브러리 소스를 탐색하는 것 — 그건 library-research 역할
- 탐색 결과 없이 "아마 여기 있을 것이다"로 추측하는 것 — 증거 기반
- 의도 분석 없이 바로 grep 하는 것 — 먼저 무엇을 찾는지 정리
