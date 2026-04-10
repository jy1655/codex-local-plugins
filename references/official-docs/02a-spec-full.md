# Agent Skills 공식 명세 및 전체 페이지 통합

## 개요

Agent Skills는 Anthropic이 개발한 경량 오픈 포맷으로, AI 에이전트가 전문적 지식과 워크플로우를 동적으로 로드할 수 있게 한다. 스킬은 폴더에 담긴 지침, 스크립트, 리소스의 조합이다.

## SKILL.md 파일 구조

모든 스킬은 최소한 `SKILL.md` 파일을 포함해야 하며, 다음과 같은 구조를 가진다:

```
skill-name/
├── SKILL.md          # 필수: 메타데이터 + 지침
├── scripts/          # 선택: 실행 가능한 코드
├── references/       # 선택: 상세 문서
├── assets/           # 선택: 템플릿, 리소스
└── ...               # 추가 파일/디렉토리
```

## 프론트매터 필드

| 필드 | 필수 여부 | 제약사항 |
|------|---------|--------|
| `name` | 필수 | 최대 64자, 소문자/숫자/하이픰만 가능, 하이픰으로 시작/종료 불가, 스킬 디렉토리명과 일치 |
| `description` | 필수 | 최대 1024자, 스킬 사용 시기 설명, 에이전트의 활성화 여부 판단에 사용 |
| `license` | 선택 | 라이선스명 또는 번들된 라이선스 파일 참조 |
| `compatibility` | 선택 | 최대 500자, 환경 요구사항 표시 |
| `metadata` | 선택 | 임의의 키-값 매핑, 추가 메타데이터 저장 |
| `allowed-tools` | 선택 | 사전 승인된 도구 목록 (실험적) |

### name 필드 규칙

- 1-64자
- 소문자 알파벳, 숫자, 하이픰(-) 만 사용
- 하이픰으로 시작/종료 불가
- 연속 하이픰(--)  불가
- 부모 디렉토리명과 일치해야 함

유효한 예: `pdf-processing`, `data-analysis`, `code-review`
무효한 예: `PDF-Processing` (대문자), `-pdf` (하이픰으로 시작), `pdf--processing` (연속 하이픰)

### description 필드 가이드

좋은 설명:
- "PDFs 추출, 양식 작성, 병합 수행. PDF 문서 작업 시 사용."
- 사용 시기와 무엇을 하는지 명확히

나쁜 설명:
- "PDF 처리에 도움" (너무 모호)
- 일반적인 조언만 포함

## 스킬 본문 콘텐츠

프론트매터 이후 마크다운 본문에 실제 지침 작성. 추천 섹션:

- 단계별 지침
- 입출력 예제
- 엣지 케이스 처리

권장: 500줄 이내, 5000토큰 미만으로 유지

## 선택적 디렉토리

### scripts/

실행 가능 코드:
- 독립적이거나 의존성 명확히 문서화
- 도움이 되는 에러 메시지
- 엣지 케이스 처리

### references/

상세 문서:
- `REFERENCE.md` - 기술 레퍼런스
- `FORMS.md` - 폼 템플릿
- 도메인별 파일

파일은 필요시에만 로드되므로 집중된 내용 유지

### assets/

정적 리소스:
- 템플릿
- 이미지
- 데이터 파일

## Progressive Disclosure 원칙

스킬의 효율적 컨텍스트 사용:

1. **메타데이터** (~100 토큰): 모든 스킬의 name, description 로드 (시작)
2. **지침** (<5000 토큰): 스킬 활성화 시 전체 SKILL.md 로드
3. **리소스** (필요시): scripts/, references/ 파일 필요할 때만 로드

## 파일 참조

스킬 내 다른 파일 참조 시 상대경로 사용:

```markdown
상세사항은 [레퍼런스](references/REFERENCE.md)를 보세요.

추출 스크립트 실행:
scripts/extract.py
```

깊게 중첩된 참조 체인 피하기

## 검증

skills-ref 라이브러리로 스킬 검증:

```bash
skills-ref validate ./my-skill
```

프론트매터 유효성과 네이밍 컨벤션 확인

## 클라이언트 지원

Agent Skills는 40+개의 주요 에이전트 제품이 지원:

Junie, Gemini CLI, Autohand, OpenCode, OpenHands, Mux, Cursor, Amp, Letta, Firebender, Goose, GitHub Copilot, VS Code, Claude Code, Claude, Codex, Piebald, Factory, Databricks Genie, OpenAI 등

## 스킬 생성 가이드

### 빠른 시작

`.agents/skills/skill-name/SKILL.md` 파일 생성:

```yaml
---
name: roll-dice
description: 주사위 굴리기. 사용자가 주사위 굴리기 요청 시 사용.
---

주사위 굴리기 명령:
```bash
echo $((RANDOM % <sides> + 1))
```
```

### 모범 사례

1. **실제 전문성에서 시작**
   - 실제 작업에서 추출한 패턴 재사용
   - 프로젝트 특정 맥락 포함
   - 일반적 가이드보다는 구체적 지식 활용

2. **실행으로 검증**
   - 실제 작업에 대해 테스트
   - 피드백 루프로 반복 개선
   - 실행 추적 분석

3. **컨텍스트 현명하게 사용**
   - 에이전트가 이미 아는 것 제외
   - 응집력 있는 단위로 설계
   - 대규모 스킬은 progressive disclosure 활용

4. **제어 보정**
   - 유연한 작업: 자유도 제공, 이유 설명
   - 취약한 작업: 구체적 지시
   - 기본값 제공, 메뉴 제시 아님

### 효과적 지침 패턴

- **Gotchas 섹션**: 에이전트가 놓칠 구체적 사항
- **출력 포맷 템플릿**: 구체적 형식 예제 제공
- **다단계 워크플로우 체크리스트**: 진행 상황 추적
- **검증 루프**: 에이전트 스스로 검증
- **Plan-Validate-Execute**: 큰 작업의 안전성

## 스킬 설명 최적화

description은 스킬 활성화의 유일한 메커니즘. 효과적 설명:

- 명령형 표현: "다음 경우 사용..."
- 사용자 의도 중심
- 명시적 문맥 나열 (사용자가 명시하지 않아도)
- 간결함 (1024자 제한)

eval 쿼리로 테스트:
- 20개 쿼리 (should-trigger 10개, should-not-trigger 10개)
- 다양한 문체, 명확성, 디테일
- near-miss 포함 (비슷하지만 다른 작업)
- 3회 이상 실행해 trigger rate 계산

Train/validation split으로 과적합 방지:
- Train (60%): 개선 가이드
- Validation (40%): 일반화 확인

## 스킬 평가

`evals/evals.json` 에 테스트 케이스 정의:

```json
{
  "skill_name": "csv-analyzer",
  "evals": [
    {
      "id": 1,
      "prompt": "...",
      "expected_output": "...",
      "files": [...],
      "assertions": [...]
    }
  ]
}
```

평가 워크스페이스 구조:
```
skill-workspace/
└── iteration-N/
    ├── eval-test-1/
    │   ├── with_skill/
    │   └── without_skill/
    ├── eval-test-2/
    └── benchmark.json
```

Assertion으로 검증:
- 구체적인 pass/fail 조건
- 증거 기록 (파일 크기, 콘텐츠 인용)
- 패턴 분석 (실패 원인, 개선 방향)

Iteration 루프:
1. 현재 상태 평가
2. 실패 분석
3. 개선
4. 새 iteration에서 재실행
5. 결과 분석

## 스크립트 사용

### 일회성 명령

기존 도구 직접 참조 (의존성 자동 해결):

```bash
# Python
uvx ruff@0.8.0 check .
pipx run 'black==24.10.0' .

# JavaScript
npx eslint@9 --fix .

# Go
go run golang.org/x/tools/cmd/goimports@v0.28.0 .
```

### 자체 포함 스크립트

PEP 723 (Python):
```python
# /// script
# dependencies = ["beautifulsoup4"]
# ///
```

Deno:
```typescript
import * as cheerio from "npm:cheerio@1.0.0";
```

Bun:
```typescript
import * as cheerio from "cheerio@1.0.0";
```

### 에이전트 친화적 스크립트

- 인터랙티브 프롬프트 금지
- `--help` 문서화
- 구체적 에러 메시지
- 구조화된 출력 (JSON/CSV)
- stdout=데이터, stderr=진단
- 멱등성
- Dry-run 지원
- 의미 있는 exit code

## 클라이언트 구현 가이드

### Discovery (1단계)

검색 경로:
- 프로젝트 레벨: `<project>/.agents/skills/`, `<project>/.<client>/skills/`
- 사용자 레벨: `~/.agents/skills/`, `~/.<client>/skills/`

검색 규칙:
- SKILL.md를 포함한 디렉토리만 발견
- .git/, node_modules/ 제외
- 깊이 제한 (최대 4-6 레벨)

name 충돌: 프로젝트 레벨 > 사용자 레벨 (결정적 우선순위)

### Parsing (2단계)

frontmatter 추출:
1. `---` 찾기 (시작과 끝)
2. YAML 파싱
3. 본문은 마지막 `---` 이후

저장 항목: name, description, location

### Disclosure (3단계)

스킬 카탈로그 생성:

```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>...</description>
    <location>/path/to/SKILL.md</location>
  </skill>
</available_skills>
```

시스템 프롬프트 또는 도구 설명에 포함
각 스킬 ~50-100 토큰

### Activation (4단계)

두 가지 활성화 방식:

1. **파일 읽기**: 모델이 SKILL.md 경로로 표준 파일 읽기 도구 호출
2. **전용 도구**: `activate_skill` 도구 구현

전달 내용:
- 전체 파일 (frontmatter 포함) 또는
- 본문만 (frontmatter 제거)

구조적 래핑 (선택):
```xml
<skill_content name="pdf-processing">
...
<skill_resources>
  <file>scripts/extract.py</file>
</skill_resources>
</skill_content>
```

권한 allowlist: 스킬 디렉토리에서 무제한 파일 읽기 허용

### Context Management (5단계)

- 스킬 콘텐츠 pruning에서 보호
- 활성화 중복 제거
- 서브에이전트 위임 (선택)

---

**작성 기준 날짜**: 2026년 4월
**소스**: https://agentskills.io 공식 문서 전체
