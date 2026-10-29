# 압축 전 Wiki handoff

`PreCompact`의 동기 command 훅입니다. 수동·자동 압축 전에 공개 대화 기록을
별도 Codex 모델 호출로 요약하고 Wiki MCP에 저장·재조회한 뒤 압축을 계속합니다.
`clear`를 호출하지 않습니다. 현재 세션 모델 이름을 재사용하며 압축마다 추가
모델 사용량과 대기 시간이 발생합니다.

## 처리와 저장 위치

1. 훅의 세션 ID와 대화 파일 ID를 비교합니다. 사용자·assistant 공개 메시지,
   최근 계획과 제한된 도구 결과 발췌를 읽습니다. 숨겨진 reasoning은 제외합니다.
2. 읽기 전용·ephemeral Codex 호출로 목표·제약·유효한 결정·완료/미완료·근거·다음
   행동을 구조화합니다. 해당 호출은 사용자 config를 읽지 않고 shell, MCP, apps,
   plugins, subagents, memories, web search를 사용하지 않도록 설정합니다.
   프로젝트 수정·Wiki 쓰기는 요약 모델에 맡기지 않습니다.
3. `gitleaks stdin --redact`로 결과를 검사합니다. 별도 app-server의 ephemeral
   연결에서 이미 로그인된 `wiki` MCP의 `wiki_add_raw`, `wiki_write_page`,
   `wiki_read`만 호출합니다. 자격증명을 읽거나 복사하지 않습니다.
4. `raw/YYYY-MM-DD_codex-handoff-<key>.md`를 남기고 세션별
   `pages/concepts/codex-handoff-<session-id>.md`를 최신 기록으로 갱신합니다.
   두 파일의 내용과 SHA-256을 다시 읽어 확인합니다. 같은 입력의 저장 재시도는
   기존 요약을 재사용하고, raw만 저장된 경우 page 연결부터 복구합니다.

원문 대화 전체는 Wiki로 전송하지 않습니다. 요약은 과거 맥락이며 현재 권한을
부여하지 않습니다. 모델 요약의 누락·오해 가능성은 남으므로 근거와 미검증 항목을
함께 기록합니다. 비밀정보·고객/타인 개인정보·법인 공식 문서 원문을 제외하도록
요약기에 지시하며 로컬 및 서버의 내용 검사를 적용합니다. 이는 모든 민감정보를
완벽히 탐지한다는 보장이 아닙니다.

## 기기별 적용

필수: Codex CLI 0.165.0에서 사용한 app-server API, Python 3.9 이상,
`gitleaks`, 로그인된 Codex, 이름이 `wiki`인 MCP 연결과 Wiki 쓰기 권한.
환경 sync 자체에는 Python 3.11 이상이 필요합니다.

```sh
git pull
python3.11 -m codex_env_sync.cli apply --repo-root .
```

Windows는 설치된 Python 3.11 이상으로 `py -3 -m codex_env_sync.cli apply --repo-root .`를
실행합니다. 훅의 Windows launcher도 Python Launcher(`py`)를 사용합니다.
Windows에서의 실제 실행은 별도 검증 대상입니다.

새 Codex 세션의 `/hooks`에서 이 정의를 읽고 신뢰해야 활성화됩니다. 소스 또는
설치만으로 신뢰를 부여하지 않으며 신뢰 상태와 인증정보를 Git으로 복제하지 않습니다.
`wiki` 연결이 없다면 해당 기기의 기존 설치 절차로 연결하고 `codex mcp login wiki`로
로그인합니다. 이미 유효한 로그인이 있으면 반복할 필요가 없습니다.

## 실패와 제한

처리 가능한 읽기·요약·검사·저장·재조회 실패는 `continue: false`로 압축을 중단합니다.
요약 제한 시간은 240초, MCP 연결을 포함한 내부 제한은 350초, 호스트 훅 제한은
420초입니다. 훅 자체의 강제 종료·호스트 시간초과·미신뢰/비활성 상태까지
차단된다고 보장하지 않습니다. 호스트의 실패 동작은 별도입니다.

입력이 200,000자 또는 대화 파일이 128 MiB를 넘으면 조용히 잘라 저장하지 않고
중단합니다. 공개된 이전 compaction 요약이 있으면 그 이후 기록을 사용합니다.
대화 파일 포맷과 app-server API는 변할 수 있으며, 지원하지 않는 형태는 중단합니다.
OpenAI 로그인으로 사용 가능한 모델을 전제로 하고 다른 provider는 검증하지 않았습니다.

실제 `PreCompact` 자동 호출과 직접 프로그램 호출은 다른 검증입니다.
`_verification: true`인 테스트 입력은 Wiki에 수동 검증임을 표시하며 compact를 실행하지 않습니다.
해제는 `/hooks`에서 이 훅만 비활성화하면 됩니다.

공식 동작: <https://learn.chatgpt.com/docs/hooks>
