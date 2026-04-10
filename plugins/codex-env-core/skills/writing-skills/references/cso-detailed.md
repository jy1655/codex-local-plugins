# Claude Search Optimization (CSO) — 상세 가이드

## 목차

1. Rich Description Field
2. Keyword Coverage
3. Descriptive Naming
4. Token Efficiency
5. Cross-Referencing Skills

## 1. Rich Description Field

목적: Claude가 description을 읽고 지금 이 스킬을 읽어야 하는가를 결정한다. "이 스킬을 지금 로드할까?"에 답해야 한다.

포맷: "Use when..."으로 시작하여 트리거 조건에 집중

Critical: Description = When to Use, NOT What the Skill Does

Description에 스킬의 프로세스나 워크플로우를 요약하지 마라.

### 왜 이것이 중요한가?

테스트 결과: Description이 스킬의 워크플로우를 요약하면, Claude는 설명 대신 본문을 따를 가능성이 있다. "작업 간 코드 리뷰를 하며 구현 계획 실행" 같은 설명은 Claude가 리뷰 1회만 하게 만든다. 실제로는 플로우차트가 명확하게 2회(사양 준수, 코드 품질)를 보여줌에도.

Description이 단순히 "현재 세션의 독립적 작업으로 구현 계획 실행할 때"로 바뀌면? Claude는 본문을 읽고 2단계 리뷰를 올바르게 따른다.

트랩: 워크플로우를 요약한 설명은 Claude가 취할 지름길이 된다. 스킬 본문은 무시할 문서가 된다.

### 나쁜 예

```yaml
# ❌ 워크플로우 요약 — Claude가 description을 따르고 본문 무시 가능
description: 구현 계획 실행 — 작업마다 서브에이전트 디스패치, 작업 간 코드 리뷰

# ❌ 너무 많은 프로세스 상세
description: TDD 사용 — 테스트 먼저, 실패 보기, 최소 코드, 리팩토링

# ❌ 너무 추상적, 트리거 없음
description: 비동기 테스팅용

# ❌ 1인칭
description: 비동기 테스트가 flaky할 때 도와줄 수 있어
```

### 좋은 예

```yaml
# ✅ 트리거만, 워크플로우 요약 없음
description: 현재 세션의 독립적 작업으로 구현 계획 실행할 때 사용

# ✅ 트리거만
description: 기능이나 버그 수정을 구현하기 전에 사용

# ✅ 기술 특정, 명확한 트리거
description: React Router를 사용하며 인증 리다이렉트를 처리할 때 사용

# ✅ 구체적 증상, 기술 무관
description: 테스트에 경쟁 조건, 타이밍 의존성, 일관성 없는 pass/fail이 있을 때 사용
```

### 작성 가이드라인

- 구체적 트리거, 증상, 상황을 사용 (문제를 신호하는 것들)
- 문제를 설명한다 (경쟁 조건, 일관성 없음) — 기술별 증상 아님 (setTimeout, sleep)
- 스킬 자체가 기술 특정 아니면 기술 무관하게
- 스킬이 기술 특정이면 트리거에 명시
- 3인칭 (시스템 프롬프트에 주입됨)
- 스킬의 프로세스나 워크플로우 절대 요약 금지

## 2. Keyword Coverage

Claude가 검색할 말들을 사용한다:

- 에러 메시지: "Hook timed out", "ENOTEMPTY", "race condition"
- 증상: "flaky", "hanging", "zombie", "pollution"
- 동의어: "timeout/hang/freeze", "cleanup/teardown/afterEach"
- 도구: 실제 명령어, 라이브러리명, 파일 타입

## 3. Descriptive Naming

스킬 이름도 검색 최적화다.

능동태, 동사 우선:
- ✅ `writing-skills` not `skill-writing`
- ✅ `condition-based-waiting` not `async-test-helpers`

gerund (-ing) 패턴이 프로세스 이름에 잘 맞는다:
- `writing-skills`, `testing-skills`, `debugging-with-logs`
- 능동적, 진행 중인 동작을 설명

## 4. Token Efficiency (Critical)

문제: 자주 로드되는 스킬과 getting-started는 모든 대화에 포함된다. 토큰은 금귀다.

목표 단어 수:
- getting-started 워크플로우: < 150 단어 각각
- 자주 로드되는 스킬: < 200 단어 전체
- 기타 스킬: < 500 단어 (여전히 간결)

### 기법들

도구 도움말로 세부 이동:

```markdown
# ❌ SKILL.md에 모든 플래그 문서화
search-conversations는 --text, --both, --after DATE, --before DATE, --limit N 지원

# ✅ --help 참조
search-conversations는 여러 모드와 필터를 지원한다. 상세는 --help 참조.
```

교차 참조 사용:

```markdown
# ❌ 워크플로우 세부 반복
검색할 때, 템플릿과 함께 서브에이전트 디스패치...
[20줄 반복된 지침]

# ✅ 다른 스킬 참조
항상 서브에이전트 사용 (50-100배 맥락 절약). 필수: coding-convention:other-skill-name 참조.
```

예제 압축:

```markdown
# ❌ 상세한 예제 (42 단어)
인간 파트너: "React Router에서 이전에 인증 에러를 어떻게 처리했어?"
당신: 과거 대화에서 React Router 인증 패턴을 검색하겠다.
[서브에이전트 디스패치: 검색 쿼리]

# ✅ 최소 예제 (20 단어)
파트너: "React Router 인증 에러 처리 어떻게 했어?"
당신: 검색...
[서브에이전트 → 종합]
```

중복 제거:
- 교차 참조된 스킬 내용 반복 금지
- 명령어에서 자명한 것 설명 금지
- 같은 패턴의 예제 여러 개 금지

검증:

```bash
wc -w skills/path/SKILL.md
# getting-started: < 150 목표
# 자주 로드: < 200 전체
```

## 5. Cross-Referencing Other Skills

다른 스킬을 참조할 때:

스킬 이름만 사용, 명시적 필수 마커:
- ✅ Good: `필수 선행: coding-convention:test-driven-development를 반드시 이해해야 한다`
- ✅ Good: `필수 배경: coding-convention:systematic-debugging를 이해해야 한다`
- ❌ Bad: `skills/testing/test-driven-development 참조` (필수인지 불명확)
- ❌ Bad: `@skills/testing/test-driven-development/SKILL.md` (강제 로드, 맥락 낭비)

왜 @ 링크 사용 금지: `@` 구문은 파일을 즉시 로드하여 필요하기 전에 200k+ 맥락을 소비한다.
