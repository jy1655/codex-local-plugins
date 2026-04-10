---
name: jy-library-research
description: Use when working with an unfamiliar library, package, or external dependency and need evidence-based answers with source links.
---

# JY Library Research

## Overview

외부 라이브러리, 패키지, 의존성에 대한 질문에 증거 기반으로 답한다.
추측이 아니라 공식 문서, 소스 코드, GitHub permalink로 뒷받침한다.

## When to Use

- "[라이브러리] 어떻게 쓰지?", "이 패키지 best practice가 뭐야?"
- 외부 의존성의 이상한 동작을 이해해야 할 때
- 오픈소스 라이브러리 내부 구현을 확인해야 할 때
- 익숙하지 않은 npm/pip/cargo 패키지 사용법을 찾을 때

사용하지 않을 때:
- 현재 프로젝트 코드 내부 탐색 (jy-codebase-explore 사용)
- 이미 알고 있는 라이브러리의 단순 사용
- 아키텍처 결정 (jy-consult 사용)

## Quick Reference

| 요청 유형 | 접근 |
|----------|------|
| **개념** ("어떻게 쓰지?") | 공식 문서 → 사용 예제 → 핵심 패턴 |
| **소스 분석** ("내부 동작이 뭐지?") | GitHub 소스 → permalink → 동작 설명 |
| **구현** ("이걸로 X 만들기") | 공식 예제 → 프로젝트 맥락 적용 → 코드 제안 |
| **디버그** ("왜 이상하게 동작해?") | 이슈 트래커 → 소스 → 알려진 제한 사항 |

## Research Protocol

### Step 1: 요청 분류

요청을 개념/소스/구현/디버그 중 하나로 분류한 뒤 해당 접근을 따른다.

### Step 2: 증거 수집

- 공식 문서를 먼저 확인
- 소스 코드가 필요하면 GitHub에서 permalink 확보
- 날짜 인식: 현재 연도 기준으로 검색, 작년 결과는 충돌 시 무시

### Step 3: 증거 기반 답변

모든 주장에 출처를 첨부:
- 공식 문서 링크
- GitHub permalink (파일 + 라인)
- 이슈/PR 번호

추측은 명시적으로 표시: "문서에 명시되지 않았지만, 소스에서 추론하면..."

### Step 4: 프로젝트 맥락 연결

라이브러리 정보를 현재 프로젝트에 어떻게 적용할지까지 연결.
일반적인 튜토리얼이 아니라 현재 코드에 맞는 적용 방법.

## Common Mistakes

- 증거 없이 "보통 이렇게 한다"로 답하는 것 — 문서/소스 링크 필수
- 작년 정보를 현재인 것처럼 제시하는 것 — 날짜 확인
- 일반적인 튜토리얼만 제공하고 프로젝트 맥락을 무시하는 것
- 코드를 수정하는 것 — 리서치 결과를 제공할 뿐, 구현은 별도
- 현재 프로젝트 내부 코드를 조사하는 것 — 그건 jy-codebase-explore 역할
