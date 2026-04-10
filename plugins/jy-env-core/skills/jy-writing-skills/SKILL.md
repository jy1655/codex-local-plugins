---
name: jy-writing-skills
description: Use when creating a new skill, revising an existing skill, or verifying that a first-party skill is ready for deployment in this repo.
---

# JY Writing Skills

## 목차

- 개요
- Quick Reference
- 스킬을 언제 작성할 것인가
- 스킬 유형
- SKILL.md 구조
- 작성 언어 정책
- Claude Search Optimization
- 테스트 전략
- Common Mistakes
- 스킬 작성 체크리스트

## 개요

스킬 작성은 TDD(테스트 주도 개발)를 프로세스 문서화에 적용한 것이다. 테스트 케이스를 먼저 작성하고(압박 시나리오), 실패를 관찰한 후(기준선), 스킬 문서를 작성하고(구현), 다시 성공을 확인한다(검증). 마지막으로 허점을 막는다(리팩토링).

핵심 원칙: 스킬 없이 에이전트가 실패하는 모습을 직접 보지 못했다면, 그 스킬이 올바른 것을 가르치는지 알 수 없다.

필수 배경: `jy-test-driven`를 반드시 먼저 이해해야 한다. 그 스킬이 RED-GREEN-REFACTOR 사이클의 기초를 정의한다.

## Quick Reference

| 단계 | 반드시 확인할 것 | 실패 신호 |
|------|----------------|----------|
| RED | 스킬 없이 기준선 실패를 관찰했는가 | 압박 시나리오 없이 문서부터 씀 |
| GREEN | 기준선 실패를 직접 막는 최소 문서를 썼는가 | 체크리스트와 예시만 늘어남 |
| REFACTOR | 새 합리화 경로를 막았는가 | 한 번 통과했다고 끝냄 |
| 배포 | references, agents, 테스트를 같이 검증했는가 | SKILL.md만 수정하고 끝냄 |

## 스킬이란?

스킬은 검증된 기법, 패턴, 도구에 대한 참조 가이드다. 향후 Claude 인스턴스가 효과적인 접근 방식을 찾고 적용하도록 돕는다.

스킬은 재사용 가능한 기법이자 패턴이자 도구다. 한 번 문제를 해결한 과정의 내러티브가 아니다.

이 repo에서 최근 확장 중인 대표적인 first-party workflow 예시는 `jy-writing-plans`,
`jy-executing-plans`, `jy-worktrees`, `jy-receiving-review` 같은 Codex-native 운영 스킬이다.

## TDD를 스킬 작성에 적용

| TDD 개념 | 스킬 작성 |
|---------|--------|
| 테스트 케이스 | 서브에이전트를 포함한 압박 시나리오 |
| 프로덕션 코드 | 스킬 문서 (SKILL.md) |
| RED 실패 | 스킬 없이 에이전트가 규칙 위반 |
| GREEN 성공 | 스킬 있으면 에이전트가 준수 |
| REFACTOR | 준수 유지하며 허점 막기 |

전체 스킬 작성 프로세스가 RED-GREEN-REFACTOR를 따른다.

## 스킬을 언제 작성할 것인가

작성 대상:
- 기법이 직관적이지 않음
- 여러 프로젝트 간 반복 참조
- 패턴이 광범위하게 적용 (프로젝트별 아님)
- 다른 사람도 유익

작성 대상 아님:
- 일회성 해결책
- 다른 곳에 이미 잘 정리된 표준
- 프로젝트별 규칙 (CLAUDE.md에 기술)
- 정규식/자동화로 강제 가능한 제약

## 스킬 유형

기법: 따라할 단계가 있는 구체적 방법 (예: 조건 기반 대기, 근본 원인 추적)

패턴: 문제를 생각하는 방식 (예: 플래그로 평탄화, 불변식 테스트)

참조: API 문서, 구문 가이드, 도구 설명서

## 디렉토리 구조

```
skills/
  skill-name/
    SKILL.md              # 필수
    supporting-file.*     # 필요시만
```

평탄한 네임스페이스 - 모든 스킬이 검색 가능하다.

분리 대상:
- 대용량 참조 (100+ 줄) — API 문서, 포괄적 구문
- 재사용 가능 도구 — 스크립트, 유틸, 템플릿

인라인 유지:
- 원칙과 개념
- 코드 패턴 (< 50 줄)
- 기타 모두

## SKILL.md 구조

Frontmatter (YAML):
- 필수 필드: `name`, `description`
- `name`: 소문자, 숫자, 하이픈만 (특수문자 금지)
- `description`: 제3인칭, "Use when..."으로 시작, 트리거 조건만 (프로세스 설명 금지)

본문 구조:
- Overview — 이것이 무엇인가? 핵심 원칙 1-2문장
- When to Use — 증상과 사용 사례 (결정이 자명하지 않으면 간단한 플로우차트)
- Core Pattern (기법/패턴용) — Before/After 코드 비교
- Quick Reference — 표 또는 글머리 목록으로 훑기
- Implementation — 간단하면 인라인, 길면 파일 링크
- Common Mistakes — 실패와 해결책

## 작성 언어 정책

기본값은 간단하다.

- core `SKILL.md` 본문은 `English-first`로 작성한다
- `agents/openai.yaml`의 `display_name`, `short_description`, `default_prompt`도 같은 기준을 따른다
- supporting reference도 모델이 직접 읽을 가능성이 높으면 영어를 우선한다

이유:

- 스킬은 사람보다 모델이 먼저 읽는 문서다
- 검색, trigger matching, cross-skill reuse, tool/provider portability가 영어 쪽이 더 안정적이다
- 동일 repo 안에서 core workflow 문서 언어가 섞이면 유지보수 drift가 커진다

예외:

- 사용자용 README, 한국어 운영 문서, 결과 기록 템플릿은 bilingual 또는 Korean이어도 된다
- repo-specific human note가 목적이라면 한국어를 써도 된다
- 단, core workflow instruction 자체를 한국어로 쓰는 것은 명확한 이유가 있을 때만 한다

즉 "사람이 보기 편하다"만으로 core skill을 한국어로 쓰는 쪽을 기본값으로 삼지 않는다.

## Claude Search Optimization (CSO) — 핵심

미래 Claude가 스킬을 찾을 수 있도록 하는 것이 중요하다.

### Description 필드의 역할

Description은 두 가지만 해야 한다:
1. 트리거 조건을 구체적으로 명시
2. 프로세스/워크플로우 설명 금지

테스트 결과: Description이 워크플로우를 요약하면, Claude는 본문을 읽지 않고 Description을 따른다. "코드 리뷰 사이에 진행" 같은 설명은 Claude가 리뷰 1회만 하게 만든다. 실제로는 2회 필요함에도.

Description을 "독립적 작업으로 실행 계획 수행 시"로 바꾸면 Claude는 본문을 읽고 2회 리뷰를 올바르게 따른다.

좋은 예:
- "구현 계획을 현재 세션의 독립적 작업으로 실행할 때 사용"
- "기능이나 버그 수정을 구현하기 전에 사용"

나쁜 예:
- "TDD 사용 - 테스트 먼저, 실패 보기, 최소 코드, 리팩토링" (워크플로우 요약)
- "비동기 테스팅용" (너무 추상적)

### 키워드 커버리지

Claude가 검색할 말들을 사용한다:
- 에러 메시지: "timeout exceeded", "ENOTEMPTY"
- 증상: "flaky", "hanging", "race condition"
- 동의어: "cleanup/teardown", "pollution"
- 도구명: 실제 명령어, 라이브러리명

### 토큰 효율성

자주 로드되는 스킬은 모든 대화에 포함된다. 토큰은 금귀다.

목표 단어 수:
- getting-started 워크플로우: < 150 단어
- 자주 로드되는 스킬: < 200 단어
- 기타: < 500 단어

기법: 세부 내용을 도구 도움말로 이동, 다른 스킬 참조, 예제 압축, 중복 제거.

### 다른 스킬 참조

```markdown
필수 선행: `jy-test-driven`를 반드시 이해해야 한다
```

`@` 링크는 사용 금지 — 파일을 즉시 로드하여 맥락을 낭비한다.

## The Iron Law (TDD와 동일)

```
실패하는 테스트 없이 스킬 작성 금지
```

새 스킬과 기존 스킬 수정 모두 적용된다.

스킬을 먼저 쓴 후 테스트? 삭제. 다시 시작.
스킬을 수정했는데 테스트 안 함? 같은 위반.

예외 없음:
- 간단한 추가도 아님
- 섹션 추가도 아님
- 문서 업데이트도 아님
- 미테스트 변경을 참조로 유지하지 말 것
- 테스트 실행 중 "적응"하지 말 것

## 테스트 전략

스킬 유형별 테스트 방식:

규칙 적용 스킬 (TDD, 검증-후-완료):
- 학술적 질문: 규칙을 이해하는가?
- 압박 시나리오: 압박 속에서 준수하는가?
- 복합 압박: 시간 + 투자 비용 + 피로

기법 스킬 (조건 기반 대기, 근본 원인 추적):
- 응용 시나리오: 기법을 올바르게 적용하는가?
- 변형 시나리오: 엣지 케이스를 처리하는가?

패턴 스킬 (정신 모델):
- 인식 시나리오: 패턴을 인식하는가?
- 응용 시나리오: 정신 모델을 사용하는가?
- 반대 사례: 사용하지 말아야 할 때를 아는가?

참조 스킬 (문서, API):
- 검색 시나리오: 올바른 정보를 찾는가?
- 응용 시나리오: 찾은 정보를 올바르게 사용하는가?

상세한 테스트 방법은 references/skill-testing-guide.md 참조.

합리화 회피 경로를 막는 강화 패턴 (Bulletproofing) — 압박 시나리오·반례 모음·"이건 다르다" 변명 차단·STOP 게이트·반복 주입 등은 references/bulletproofing-skills.md 참조.

CSO(조건-스킬-출력) 형식의 정확한 예시·반례·작성 절차는 references/cso-detailed.md 참조.

## Red Flags — 멈추고 다시 시작할 징후

```markdown
- 테스트 먼저 작성 없이 코드 작성
- "수동으로 이미 테스트했다"
- "테스트 후 작성이 같은 목표 달성"
- "정신은 지켰다"
- "이건 다르다, 왜냐하면..."

모두 의미: 코드 삭제. TDD로 다시 시작.
```

## Common Mistakes

- frontmatter 설명에 워크플로우를 요약해서, 에이전트가 본문을 안 읽게 만드는 것
- 본문에 `Quick Reference`와 `Common Mistakes` 같은 스캔용 섹션을 빼는 것
- 존재하지 않는 스킬 네임스페이스나 오래된 참조명을 그대로 복사하는 것
- 기준선 실패를 보지 않고 "문서만 보면 분명하다"라고 가정하는 것
- supporting file이 있는데 본문에서 언제 읽어야 하는지 연결하지 않는 것
- core workflow instruction을 특별한 이유 없이 한국어로 작성해서 English-first 규칙을 깨는 것

## RED-GREEN-REFACTOR 사이클

RED: 압박 시나리오를 스킬 없이 실행. 정확히 무엇을 하는가? 어떤 변명을 하는가? 어떤 압박이 위반을 유발하는가?

GREEN: 그 변명들을 다루는 최소한의 스킬을 작성. 같은 시나리오를 스킬 있이 실행. 에이전트는 이제 준수해야 한다.

REFACTOR: 새로운 변명을 찾으면 명시적 대응 추가. 허점이 없을 때까지 재테스트.

## 스킬 작성 체크리스트 (TDD 적응)

RED Phase — 실패하는 테스트 작성:
- 압박 시나리오 작성 (규칙 스킬은 3+ 복합 압박)
- 스킬 없이 시나리오 실행 — 기준선 행동 기록
- 변명/실패 패턴 파악

GREEN Phase — 최소한 스킬 작성:
- 이름: 소문자, 숫자, 하이픈만
- Frontmatter: `name`, `description` (max 1024 chars)
- Description: "Use when..."으로 시작, 제3인칭, 트리거만
- core `SKILL.md`와 agent prompt surface는 English-first 유지
- 검색 키워드 포함 (에러, 증상, 도구)
- 명확한 개요와 핵심 원칙
- RED에서 식별한 구체적 실패 해결
- 코드 인라인 또는 파일 링크
- 뛰어난 예제 1개 (다중 언어 아님)
- 스킬 있이 시나리오 실행 — 준수 확인

REFACTOR Phase — 허점 막기:
- 테스트에서 새로운 변명 파악
- 명시적 대응 추가 (규칙 스킬)
- 모든 테스트 반복에서 변명 표 작성
- Red Flags 목록 생성
- 허점 없을 때까지 재테스트

품질 검사:
- 플로우차트는 결정이 자명하지 않을 때만
- Quick Reference 표
- Common Mistakes 섹션
- 내러티브 스토리텔링 없음
- 도구/대용량 참조용 보조 파일만

배포:
- git에 커밋
- 광범위하게 유용하면 PR 기여 고려

## 흐름도 사용

언제 사용할 것인가:
- 자명하지 않은 결정점
- 일찍 멈출 수 있는 프로세스 루프
- "A vs B" 결정

언제 사용하지 말 것인가:
- 참조 자료 → 표, 목록
- 코드 예제 → Markdown 블록
- 선형 지침 → 번호 목록
- 의미 없는 라벨 (step1, helper2)

graphviz 스타일 규칙은 references/graphviz-conventions.dot 참조.

## 코드 예제

뛰어난 예제 1개가 평범한 예제 여러 개를 이긴다.

가장 관련성 높은 언어 선택:
- 테스트 기법 → TypeScript/JavaScript
- 시스템 디버깅 → Shell/Python
- 데이터 처리 → Python

좋은 예제:
- 완전하고 실행 가능
- 잘 주석 처리되어 WHY를 설명
- 실제 시나리오에서
- 패턴을 명확히 보여줌
- 적응 준비됨 (제너릭 템플릿 아님)

하지 말 것:
- 5+ 언어로 구현
- 채워 넣을 템플릿
- 억지 예제

## STOP: 다음 스킬로 이동 전

어떤 스킬을 작성한 후에는 반드시 멈추고 배포 프로세스를 완료해야 한다.

하지 말 것:
- 각각을 테스트하지 않고 여러 스킬을 일괄 작성
- 현재 스킬 검증 전에 다음으로 이동
- 배치가 효율적이라며 테스트 건너뛰기

미테스트 스킬 배포 = 미테스트 코드 배포. 품질 기준 위반.

## 발견 워크플로우

미래 Claude가 스킬을 찾는 방식:

1. 문제 발생 ("테스트가 flaky다")
2. SKILL 찾기 (Description이 매칭)
3. Overview 훑기 (관련 있나?)
4. 패턴 읽기 (Quick Reference 표)
5. 예제 로드 (구현할 때만)

이 흐름에 맞춰 최적화한다. 검색 가능한 항목을 앞쪽에 자주 배치한다.

## 요약

스킬 작성은 프로세스 문서화에 TDD를 적용한다. 같은 Iron Law, 같은 사이클, 같은 이점. 코드에 TDD를 따르면 스킬에도 따른다. 문서화에 적용된 같은 원칙이다.
