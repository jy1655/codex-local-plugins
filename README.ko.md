# Portable Codex Environment Sync

[![언어: English](https://img.shields.io/badge/Language-English-111827?style=for-the-badge)](./README.md)
[![언어: Korean](https://img.shields.io/badge/Language-Korean-0A66C2?style=for-the-badge)](./README.ko.md)

이 저장소는 이식 가능한 first-party Codex 환경을 정의합니다. 로컬 plugin bundle을
stage하고 personal marketplace와 간결한 전역 instruction을 관리하되, Codex runtime
cache를 직접 수정하지 않습니다.

사용자에게 보이는 plugin·skill 표시명, 설명, 기본 요청 문구는 한국어로 작성합니다.
모델이 읽는 스킬 본문·호출 조건 설명·기술 자료는 영어로 유지합니다. 언어·권한·개인정보·
기존 작업 보존 같은 공통 지침은 절차 스킬 설치 여부와 관계없이 전역 `AGENTS.md`에서 적용합니다.
각 컴퓨터에만 해당하는 지침은 사용자가 별도로 관리하는 `LOCAL.md`에 둡니다.

## Pack model

GPT-6 Astra 기준 구성은 `max` 추론과 기본 core-lite 가드레일 1개,
명시 호출 전용 오케스트레이션 스킬, 사용자가 선택한 아키텍처·인터뷰 팩,
선택형 iOS 메모리 분석 팩입니다. `apply`는 활성 bundle 3개를 `~/plugins`에 배치한 뒤 `INSTALLED_BY_DEFAULT` 항목을
Codex CLI로 설치합니다.

| Pack | Policy | Skills |
|---|---|---|
| `jy-env-core` — core-lite | `INSTALLED_BY_DEFAULT` | `jy-change-guardrails`, `jy-orchestrate` (명시 호출 전용) |
| `jy-env-design` | `INSTALLED_BY_DEFAULT` | `improve-codebase-architecture`, `grill-me`, `grill-with-docs` (명시 호출 전용); `grilling`, `codebase-design`, `domain-modeling` |
| `jy-env-ios` | `AVAILABLE` | `ios-memgraph-leaks` — 실기기 메모리 그래프 분석 |

`$jy-orchestrate`를 호출하면 현재 세션이 Codex·Claude의 계획·구현과 같은 결과물에 대한
Codex DevBlue·별도 Claude 세션의 독립 검증을 직접 조율합니다. 작업자에게 범위와 완료
조건을 전달하고 간결한 결과를 받으며, 근거 있는 지적은 작업자에게 돌려 수정과 영향 범위
재검토를 진행합니다. 별도 관리 세션이나 지휘자 교체 개수 제한은 없습니다. 독립적인 작업은
실행 환경이 지원하는 범위에서 병렬로 진행하고, 겹치는 편집은 격리하거나 순서대로 처리합니다.
로컬에서 Agent Bridge를 사용할 수 있으면 우선 사용하며, `allow_implicit_invocation: false`로
자동 선택을 끕니다. 컨텍스트는 기본 압축 기능을 우선 사용하고 실제 인계·복구에만 작은
기록을 둡니다. 현재 세션은 전역·로컬 정책에 따른 Wiki 기록과 저장 확인, 결과 회수와 후속
작업을 마친 세션의 종료까지 책임집니다. 기기별 Wiki 경로는 스킬에 넣지 않습니다.

나머지 23개 절차 스킬과 `jy-env-planning`, `jy-env-delivery`, `jy-env-audit`는
[archive/](archive/README.md)에 보존합니다. Manifest와 marketplace에서 제외되어
배치·설치·자동 호출되지 않습니다. 2026-09-08 전환 당시 유지한 10개 스킬의 변경 전
원문도 함께 보관합니다. 2026-10-06에는 실기기 개발 방식에 맞춰 활성 iOS 팩에
메모리 누수 분석만 남기고 나머지 8개 스킬을 삭제했습니다. 기존 archive와 과거 평가
입력은 이력 자료로 남습니다.

`AVAILABLE`로 바꾸는 것만으로 기존 설치가 해제되지는 않습니다. 기존 설치를 전환할 때는
축소된 marketplace를 적용하기 전에 설치된 절차 팩을 해제합니다.

```bash
codex plugin remove jy-env-planning@personal-codex
codex plugin remove jy-env-delivery@personal-codex
codex plugin remove jy-env-audit@personal-codex
python3 -m codex_env_sync.cli apply --repo-root .
codex plugin add jy-env-ios@personal-codex
```

설치된 항목에 대해서만 remove를 실행합니다. 변경한 활성 plugin은 `apply` 전에
`plugin-creator`의 cachebuster 흐름으로 갱신합니다. 기본 core와 design은 `apply`가 갱신하고,
선택형 iOS는 배치 후 다시 add합니다. `apply` 자체는 Codex plugin을 설치 해제하지 않습니다.
변경 후에는 새 Codex session을 시작합니다. 별도의 `~/.agents/skills/<pack>`
discovery link는 만들지 않습니다.

## 아키텍처 개선과 grill 인터뷰

2026-10-07 사용자는 Claude Code에서 Matt Pocock 원본을 직접 사용한 뒤 이 기능들의
도입을 결정했고, 간략화 없이 원본 기능을 최대한 보존하도록 요청했습니다. 이 팩의 채택은
기존 core-lite 축소 원칙보다 우선합니다. 나머지 upstream 스킬은 사용자가 원본을
사용해본 뒤 별도로 결정합니다.

별도 `jy-env-design` 팩은 1.2.3의 `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`을 기준으로 합니다.

- `$improve-codebase-architecture`: 탐색, HTML 후보 보고서, 사용자 선택 후 grilling과
  도메인 기록. HTML 템플릿과 병렬 대안 설계 참조도 모두 포함합니다.
- `$grill-me`: 결정 트리 전체를 따라 추천안을 붙인 질문 라운드, 사실 조사 위임,
  행동 전 사용자 확인을 원본대로 수행합니다.
- `$grill-with-docs`: 같은 인터뷰와 함께 `CONTEXT.md`를 갱신하고 필요한 ADR을 기록합니다.

직접 호출 스킬 3개는 명시 호출 전용입니다. 공통 기능인 `grilling`, `codebase-design`,
`domain-modeling`은 원본처럼 자동 선택이 가능하며 번들 내부 상대 링크로도 읽습니다.
Codex 호출 방식, 한국어 표시 정보, 로컬 위임 방식, Wiki·보고서 저장 위치만 이식하고
원본 절차는 줄이지 않았습니다. [이식 범위와 원저작자 표시](plugins/jy-env-design/NOTICE.md)를
참고하세요.

## 실기기 iOS 메모리 분석

`jy-env-ios`에는 `ios-memgraph-leaks`와 메모리 그래프 요약 스크립트만 있습니다.
연결한 iPhone·iPad에서 Xcode의 Debug Memory Graph와 File > Export Memory Graph로
`.memgraph`를 내보낸 뒤, Mac의 `leaks`와 포함된 스크립트로 분석합니다.
이미 확보한 메모리 그래프가 있으면 바로 분석할 수 있습니다.

스킬은 객체 수명·보유 경로·동일 조건의 수정 전후 증거에 집중합니다. 시뮬레이터 도구를
설치하거나 MCP 서버를 등록하지 않습니다. 일반 빌드·디버깅·UI 작업은 앱 저장소의 기존
도구와 지침을 사용합니다. 상세 절차는
[스킬 본문](plugins/jy-env-ios/skills/ios-memgraph-leaks/SKILL.md)을 참고합니다.

## 보관된 조사 지침

`jy-library-research`의 Context7 경로는 다른 절차 스킬과 함께 보관하며 활성 호출
규칙으로 사용하지 않습니다. 공개 질문만 전송하는 경계와 `CONTEXT7_API_KEY` 취급 지침은
명시적으로 재활성화할 때 참고할 수 있도록 원문에 보존합니다.

## Install surface

- plugin source: `~/plugins`
- personal marketplace: `~/.agents/plugins/marketplace.json`
- global instruction: `~/.codex/AGENTS.md`
- machine-local instruction (사용자 관리, 동기화 제외): `~/.codex/LOCAL.md`
- managed state: `~/.codex-env-sync/state.json`
- `codex plugin`으로만 변경하는 Codex 소유 cache: `~/.codex/plugins/cache`

로컬 `apply`는 macOS와 Linux에서 plugin source와 instruction을 symlink하고,
Windows에서는 copy mode를 사용합니다. Bootstrap과 `--snapshot`은 항상 안정적인
copy snapshot을 설치합니다. Stage 후에는 `codex plugin add`로 기본 plugin을
설치하거나 갱신하며, 선택 pack은 명시적으로 설치해야 합니다. Dirty checkout은
별도의 live skill discovery surface로 노출하지 않습니다.

### 컴퓨터별 로컬 지침

각 컴퓨터의 경로·로컬 도구·작업 공간 규칙은 설치된 전역 `AGENTS.md` 옆의 `LOCAL.md`에
작성합니다. 기본 위치는 macOS/Linux에서 `~/.codex/LOCAL.md`, Windows에서
`%USERPROFILE%\.codex\LOCAL.md`입니다. Codex가 별도의 `CODEX_HOME`을 사용한다면
그 디렉터리에 둡니다. `AGENTS.md`가 symlink여도 저장소의 `instructions/`가 아닌
설치된 전역 파일의 디렉터리를 사용합니다.

공통 `AGENTS.md`가 작업 전에 이 파일을 읽도록 지시합니다. `LOCAL.md`는 Codex의 기본
자동 탐색 파일명이 아니며, 파일이 없으면 공통 지침만으로 진행합니다. `apply`, bootstrap,
snapshot 설치는 이 파일을 관리하지 않으므로 생성·복사·덮어쓰기·삭제하지 않습니다.
저장소와 `codex-env.toml`에는 포함하지 않습니다. 지침을 변경한 뒤에는 새 Codex session을
시작합니다.

## First run

macOS / Linux:

```bash
./scripts/bootstrap.sh <git-url>
```

Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1 -GitUrl <git-url>
```

두 명령 모두 `codex` CLI가 필요하며, repo를 한 번 clone하고 안정적인 snapshot과
core-lite와 design 팩을 설치합니다.

## 기존 기기 업데이트

해당 기기의 이 저장소 clone에서 게시된 변경을 받고 설치본에 적용합니다.

```bash
git pull --ff-only
python3 -m codex_env_sync.cli apply --repo-root .
codex plugin list --marketplace personal-codex --json
```

해당 기기에 설정된 Python 3.11 이상을 사용합니다. Windows에서는 필요에 따라
`python3` 대신 `python`을 씁니다. `apply`가 기본 core와 design을 갱신하므로
각 설치 버전이 `plugins/<pack>/.codex-plugin/plugin.json`과 일치하는지
확인한 뒤 새 Codex 세션을 시작합니다. 기기별 `LOCAL.md`는 계속 별도로 관리합니다.

## Local development

해석된 source, install mode, marketplace policy를 점검합니다.

```bash
python3 -m codex_env_sync.cli inspect --repo-root .
```

현재 checkout을 적용합니다.

```bash
python3 -m codex_env_sync.cli apply --repo-root .
```

분리된 snapshot을 설치합니다.

```bash
python3 -m codex_env_sync.cli apply --repo-root . --snapshot
```

이미 설치된 plugin을 바꾼 뒤에는 `plugin-creator`의 cachebuster/reinstall 흐름을
사용하고 새 thread를 시작합니다. `~/.codex/plugins/cache`를 직접 수정하지 않습니다.

## Layout

```text
codex-env.toml                    # 활성 plugin source 3개와 installation policy
codex_env_sync/                   # inspect/apply/bootstrap engine
archive/                         # Inactive originals, checksums, and restoration notes
plugins/jy-env-core/              # 기본 core-lite bundle
plugins/jy-env-design/            # 원본을 보존한 아키텍처·인터뷰 팩
plugins/jy-env-ios/               # 선택형 실기기 메모리 분석 팩
instructions/AGENTS.md            # 선택 skill을 eager routing하지 않는 전역 규칙
.agents/plugins/marketplace.json  # local personal marketplace catalog
skill-tests/first-party/          # skill 실용성 pressure scenario
skill-tests/UTILITY-EVAL.md       # 3-arm skill 실용성·보고 계약
tests/                            # unit·integration test
```

활성 first-party skill source는 `plugins/jy-env-*/skills/`에 두고, 비활성 원문은
배포에서 제외된 `archive/`에 보관합니다. Upstream 또는 company-shared skill은
로컬에서만 사용하는 seed material이며, 이 repo는 customization이 끝난 first-party
결과만 저장하고 third-party runtime을 vendor하지 않습니다. 사용자가 선택한 `jy-env-design`은
seed-only 재작성 원칙의 명시적 예외로, 선택한 원본 스킬과 참조를 고정 revision·출처 해시·
MIT 라이선스와 함께 보존합니다. 유지할 skill은 upstream
seed에 실시간으로 의존하지 않고 이 저장소의 first-party plugin asset으로 관리합니다.
사용자가 참고나 재활성화를 요청하지 않으면 `archive/`의 지침을 설치·발견·적용하지 않습니다.

## Tests

CI와 같은 Python 3.11로 push 전에 전체 suite를 실행합니다.

```bash
python3 -X warn_default_encoding -W error::EncodingWarning -m unittest discover -s tests -q
git diff --check
```

이 명령은 모든 OS에서 텍스트 인코딩 누락을 오류로 처리해 Windows에서만 드러나던
기본 인코딩 의존을 로컬에서도 잡습니다. 파일 입출력의 명시적 UTF-8 지정과
`.gitattributes`의 archive 원본 바이트 보존·plugin LF 규칙을 유지합니다.

Pressure-scenario asset 검증:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```

## Skill 실용성 gate

Design 팩은 사용자의 직접 사용 경험과 채택 결정으로 유지합니다. 명시 호출 전용
워크플로에 implicit 활성률이나 추가 채택 벤치마크를 도입 조건으로 요구하지 않습니다.
평가 시나리오는 동작 회귀 확인용이며 Codex에서의 비교 성능을 입증한 결과는 아닙니다.

지침이 그럴듯하다는 이유만으로 skill을 유지하지 않습니다. 실용성 evaluator는 같은
task를 같은 model·effort에서 `baseline`(skill 없음), `implicit`(발견 가능),
`explicit`(강제 호출)로 비교하되 같은 plugin의 나머지 skill은 고정합니다. 이후
응답을 blind scoring하고 품질, token,
latency, implicit 활성 gate를 적용하며 tool call과 실제 skill read 여부를 기록합니다.

먼저 model call 범위를 확인합니다.

```bash
python3 -m codex_env_sync.skill_eval plan \
  --repo-root . --skill jy-change-guardrails
```

한 skill을 실행하고 freshness 또는 최신 보고서를 확인합니다.

```bash
python3 -m codex_env_sync.skill_eval run \
  --repo-root . --skill jy-change-guardrails

python3 -m codex_env_sync.skill_eval status --repo-root .
python3 -m codex_env_sync.skill_eval report --repo-root .
```

실효성 비교는 실제 부족함이 관측된 대상부터 선택적으로 실행합니다. Evaluator는
`plugins/`의 활성 source만 발견하며 보관 스킬과 과거 보고서는 참고 자료로 남깁니다.
현재 평가 정책은 `gpt-6-astra`·`max`·기본 service tier이며 별도 judge 모델의 역할은
유지합니다. 5.6 결과를 Astra의 실효성 근거로 사용하지 않으며 이번 전환에서 전체 모델
평가를 실행하지 않습니다. 증거 경계는 [skill-tests/UTILITY-EVAL.md](skill-tests/UTILITY-EVAL.md),
개별 복원 방법은 [archive/README.md](archive/README.md)를 참고합니다.
