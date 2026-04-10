# Claude Code Skills - 공식 문서

**원본 URL:** https://code.claude.com/docs/en/skills

---

## 개요

Claude Code Skills는 Claude의 기능을 확장하는 마크다운 기반의 명령어 및 워크플로우 모음입니다. `SKILL.md` 파일을 작성하여 Claude가 이를 자동으로 발견하고 필요할 때 로드합니다.

---

## 핵심 개념

### Skill의 위치와 범위

| 위치 | 경로 | 적용 범위 |
|------|------|---------|
| Enterprise | Managed settings | 전체 조직 |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | 모든 프로젝트 |
| Project | `.claude/skills/<skill-name>/SKILL.md` | 해당 프로젝트만 |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Plugin 활성화 위치 |

우선순위: Enterprise > Personal > Project > Plugin

### Skill 구조

```
my-skill/
├── SKILL.md           # 필수: 주요 지시사항
├── template.md        # 선택: Claude가 채울 템플릿
├── examples/
│   └── sample.md      # 선택: 예상 출력 형식
└── scripts/
    └── validate.sh    # 선택: Claude가 실행할 스크립트
```

---

## Frontmatter 설정

SKILL.md 최상단에 `---` 사이에 YAML 설정:

```yaml
---
name: my-skill
description: Skill이 무엇을 하고 언제 사용하는지 설명 (250자 이내 권장)
argument-hint: [filename] [format]
disable-model-invocation: true  # Claude가 자동 실행하지 않도록
user-invocable: false  # 사용자가 직접 호출 불가
allowed-tools: Read Grep Bash  # 허용된 도구 제한
model: claude-opus-4-6
effort: high
context: fork  # Subagent에서 실행
agent: Explore  # Subagent 타입
paths: src/**/*.ts,tests/**/*.ts  # 경로 패턴으로 활성화 제한
shell: bash  # bash 또는 powershell
---
```

### 주요 Frontmatter 필드

| 필드 | 설명 |
|------|------|
| `name` | Skill 이름 (소문자, 숫자, 하이픈만 사용) |
| `description` | Claude가 활성화 여부 판단에 사용 |
| `disable-model-invocation` | true면 수동 호출만 가능 (/skill-name) |
| `user-invocable` | false면 사용자는 호출 불가, Claude만 가능 |
| `allowed-tools` | Skill 활성화 시 Claude가 권한 없이 사용 가능한 도구 |
| `context: fork` | Skill을 subagent에서 격리 실행 |
| `agent` | Subagent 타입 (Explore, Plan, general-purpose 등) |
| `paths` | 특정 경로 패턴에서만 활성화 |

---

## Skill 타입과 용도

### Reference Content
코드베이스에 적용할 지식, 컨벤션, 패턴, 스타일 가이드

```yaml
---
name: api-conventions
description: API 설계 패턴
---

API 엔드포인트 작성 시:
- RESTful 네이밍 컨벤션 사용
- 일관된 에러 형식 반환
- 요청 검증 포함
```

### Task Content
단계별 지시사항을 통한 구체적 작업 (보통 `/skill-name`으로 수동 호출)

```yaml
---
name: deploy
description: Production 배포
disable-model-invocation: true
---

배포 절차:
1. 테스트 스위트 실행
2. 애플리케이션 빌드
3. 배포 대상으로 푸시
4. 배포 성공 확인
```

---

## 동적 Context Injection

`` !`<command>` `` 문법으로 실시간 데이터 주입:

```yaml
---
name: pr-summary
description: PR 요약
context: fork
agent: Explore
---

## PR Context
- PR diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Task
위 PR을 요약하라...
```

명령어는 Skill 실행 전에 먼저 실행되고, 출력이 Placeholder를 대체합니다.

다중 라인 명령어:
````markdown
```!
node --version
npm --version
git status --short
```
````

---

## 인자 전달 (Arguments)

### 기본 사용
```yaml
---
name: fix-issue
description: GitHub issue 수정
---

GitHub issue $ARGUMENTS를 수정하라...
```

`/fix-issue 123` 실행 시 `$ARGUMENTS`는 `123`으로 대체됨

### 위치 기반 접근
```yaml
---
name: migrate-component
description: 컴포넌트 마이그레이션
---

$ARGUMENTS[0] 컴포넌트를 $ARGUMENTS[1]에서 $ARGUMENTS[2]로 마이그레이션.
```

또는 단축형: `$0`, `$1`, `$2`

---

## 문자열 치환 (Substitution)

| 변수 | 설명 |
|------|------|
| `$ARGUMENTS` | 전달된 모든 인자 |
| `$ARGUMENTS[N]` | N번째 인자 (0-based) |
| `$N` | 단축형 (예: `$0`, `$1`) |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID |
| `${CLAUDE_SKILL_DIR}` | Skill 디렉토리 경로 |

---

## Invocation Control

### Claude 자동 호출 제한

```yaml
---
name: deploy
disable-model-invocation: true
---
```
사용자만 `/deploy`로 호출 가능. Claude는 자동 호출 불가

### 사용자 호출 제한

```yaml
---
name: legacy-context
user-invocable: false
---
```
Claude만 배경 지식으로 사용. `/legacy-context` 메뉴에 미표시

| Frontmatter | 사용자 호출 | Claude 호출 | Context 로드 |
|-------------|----------|-----------|------------|
| (기본값) | Yes | Yes | Description 항상, Skill은 호출 시 |
| `disable-model-invocation: true` | Yes | No | Description 미포함 |
| `user-invocable: false` | No | Yes | Description 항상 |

---

## 도구 접근 제한

```yaml
---
name: safe-reader
description: 파일 읽기 전용
allowed-tools: Read Grep Glob
---
```

Skill 활성화 시 지정된 도구만 Claude가 권한 없이 사용 가능

---

## Bundled Skills

Claude Code와 함께 제공되는 기본 Skill:

| Skill | 용도 |
|-------|------|
| `/batch <instruction>` | 코드베이스 전체의 병렬 대규모 변경 |
| `/claude-api` | Claude API 참고자료 로드 |
| `/debug [description]` | 디버그 로깅 활성화 |
| `/loop [interval] <prompt>` | 프롬프트 반복 실행 |
| `/simplify [focus]` | 코드 리팩토링 및 최적화 |

---

## Subagent에서 Skill 실행

`context: fork` 추가:

```yaml
---
name: deep-research
description: 깊이 있는 조사
context: fork
agent: Explore
---

다음을 철저히 조사하라: $ARGUMENTS

1. Glob과 Grep으로 관련 파일 찾기
2. 코드 읽기 및 분석
3. 파일 참조와 함께 결과 요약
```

Skill 콘텐츠가 Subagent의 프롬프트가 됨. `agent` 필드로 실행 환경 결정 (Explore, Plan, general-purpose 등)

---

## 시각적 출력 생성

Skill과 함께 번들된 스크립트로 인터랙티브 HTML 생성:

- 데이터 탐색 도구
- 의존성 그래프
- 테스트 커버리지 리포트
- API 문서
- DB 스키마 시각화

Python/JavaScript로 독립 실행형 HTML 파일 생성 후 `webbrowser.open()` 또는 유사 방법으로 브라우저 열기

---

## Claude의 Skill 접근 제한

### 모든 Skill 비활성화
```
/permissions에 추가:
Skill
```

### 특정 Skill만 허용/거부
```
# 정확한 매칭
Skill(commit)

# 접두사 매칭
Skill(review-pr *)

# 거부
Skill(deploy *)
```

---

## 문제 해결

### Skill이 자동으로 트리거되지 않음
1. Description이 자연스러운 사용자 언어 포함 확인
2. `/skill-name`으로 직접 호출 테스트
3. Description을 더 구체적으로 작성

### Skill이 자주 실행됨
1. Description을 더 구체적으로 변경
2. `disable-model-invocation: true` 추가

### Description이 잘림
Skill 많을 시 Description 문자 예산 제한. 250자 이내로 핵심 사용 사례 최우선으로 배치.

---

## 지원 파일 추가

복잡한 Skill은 SKILL.md를 깔끔하게 유지하고 참고 자료는 별도 파일로:

```markdown
SKILL.md에서 참조:

## 추가 자료
- 완전한 API 상세는 [reference.md](reference.md) 참조
- 사용 예시는 [examples.md](examples.md) 참조
```

SKILL.md는 500줄 이내 유지 권장
