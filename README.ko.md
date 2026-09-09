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
명시 호출 전용 오케스트레이션 스킬, 선택형 iOS 도구 팩입니다.
`apply`는 활성 bundle 2개만 `~/plugins`에 배치한 뒤 `INSTALLED_BY_DEFAULT` 항목을
Codex CLI로 설치합니다.

| Pack | Policy | Skills |
|---|---|---|
| `jy-env-core` — core-lite | `INSTALLED_BY_DEFAULT` | `jy-change-guardrails`, `jy-orchestrate` (명시 호출 전용) |
| `jy-env-ios` | `AVAILABLE` | iOS 도구·기술 참고 스킬 9개 |

`$jy-orchestrate`를 호출하면 현재 세션이 Codex와 Claude의 계획·구현을 조율하고,
Codex DevBlue와 별도 Claude 세션이 결과를 독립 검증합니다. 로컬에서 Agent Bridge를
사용할 수 있으면 우선 사용하며, `allow_implicit_invocation: false`로 자동 선택을 끕니다.

나머지 23개 절차 스킬과 `jy-env-planning`, `jy-env-delivery`, `jy-env-audit`는
[archive/](archive/README.md)에 보존합니다. Manifest와 marketplace에서 제외되어
배치·설치·자동 호출되지 않습니다. 유지한 10개 스킬의 변경 전 원문도 함께 보관합니다.

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
`plugin-creator`의 cachebuster 흐름으로 갱신합니다. 기본 core는 `apply`가 갱신하고,
선택형 iOS는 배치 후 다시 add합니다. `apply` 자체는 Codex plugin을 설치 해제하지 않습니다.
변경 후에는 새 Codex session을 시작합니다. 별도의 `~/.agents/skills/<pack>`
discovery link는 만들지 않습니다.

## 고정된 XcodeBuildMCP

`jy-env-ios`는 이 머신에서 upstream `build-ios-apps` plugin을 대체합니다.
`npx`로 `xcodebuildmcp@2.7.0`을 실행하고 `simulator`, `ui-automation`,
`debugging` workflow만 활성화합니다. 포함된 debugger skill은 현재
session-default, runtime-log, `elementRef` UI contract를 사용합니다.

`build-ios-apps@openai-curated`와 `jy-env-ios@personal-codex`를 동시에 활성화하지
마십시오. 둘 다 `xcodebuildmcp` server name을 등록합니다.

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
core-lite를 설치합니다.

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
codex-env.toml                    # 활성 plugin source 2개와 installation policy
codex_env_sync/                   # inspect/apply/bootstrap engine
archive/                         # Inactive originals, checksums, and restoration notes
plugins/jy-env-core/              # 기본 core-lite bundle
plugins/jy-env-ios/               # 선택 pinned iOS/XcodeBuildMCP pack
instructions/AGENTS.md            # 선택 skill을 eager routing하지 않는 전역 규칙
.agents/plugins/marketplace.json  # local personal marketplace catalog
skill-tests/first-party/          # skill 실용성 pressure scenario
skill-tests/UTILITY-EVAL.md       # 3-arm skill 실용성·보고 계약
tests/                            # unit·integration test
```

활성 first-party skill source는 `plugins/jy-env-*/skills/`에 두고, 비활성 원문은
배포에서 제외된 `archive/`에 보관합니다. Upstream 또는 company-shared skill은
로컬에서만 사용하는 seed material이며, 이 repo는 customization이 끝난 first-party
결과만 저장하고 third-party runtime을 vendor하지 않습니다. 유지할 skill은 upstream
seed에 실시간으로 의존하지 않고 이 저장소의 first-party plugin asset으로 관리합니다.
사용자가 참고나 재활성화를 요청하지 않으면 `archive/`의 지침을 설치·발견·적용하지 않습니다.

## Tests

전체 suite:

```bash
python3 -m unittest discover -s tests -v
```

Pressure-scenario asset 검증:

```bash
python3 -m unittest tests.test_skill_scenarios -v
```

## Skill 실용성 gate

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
