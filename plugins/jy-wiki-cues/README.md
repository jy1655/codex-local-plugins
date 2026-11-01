# Wiki 교훈 전달 (실험)

TokenEconomizer의 작은 교훈 단위를 참고한 자체 구현입니다. upstream 코드나 유료 모델을 사용하지 않습니다. 공용 실행 소스는 이 폴더의 `hooks/wiki_cues.py` 한 곳입니다. Claude 번들은 `claude-local-plugins/scripts/package-wiki-cues.py`로 이 파일을 패키징합니다.

`UserPromptSubmit`에서 작업 소유 세션 정리·검증 자료 관리와 관련된 요청을 고르고 로컬 Wiki의 `pages/concepts/agent-action-cues.md`에서 짧은 안내를 읽습니다. 본문에 적힌 출처 절의 SHA-256(UTF-8, LF, 마지막 개행 하나)을 확인합니다. 출처 변경·삭제·superseded·파싱 오류는 `UNAVAILABLE`로 표시합니다. 현재 사용자 지시와 명시 예외가 우선하며, 안내는 새로운 권한이나 차단 장치가 아닙니다.

일반 세션 시작에는 교훈을 넣지 않습니다. 명시적인 짧은 후속 요청과 resume/compact에는 해당 세션에서 마지막으로 선택한 ID만 재검증합니다(12시간 유효). 폴더 이동은 범위를 지우지 않으며 새 주제의 요청은 범위를 교체합니다. 같은 이벤트 재시도도 재검증한 결과를 다시 출력해 실패한 전달을 감추지 않습니다. 한 세션 전체에 중복 억제를 적용하지 않습니다. 정상 종료 후 resume에도 쓰도록 유효한 상태는 유지하고, 종료 시 이미 만료된 현재 세션 상태만 지웁니다.

## 설치

Python 3.11+와 Codex가 필요합니다. Windows는 `py -3`, 다른 OS는 `python3`를 사용합니다. `-I` 격리 모드로 작업 폴더·PYTHONPATH의 동명 모듈을 가져오지 않습니다. 다른 OS의 실제 호스트 검증은 별도입니다.

1. 저장소 루트에서 `python -m codex_env_sync.cli apply --repo-root .`로 선택 설치 번들을 stage합니다.
2. `codex plugin add jy-wiki-cues@personal-codex`로 설치합니다.
3. `~/.config/jy-wiki-cues/config.json`을 아래처럼 설정합니다. 두 호스트가 공유하는 기기별 설정이며 저장소에 커밋하지 않습니다.
4. 새 Codex 세션의 `/hooks`에서 정확한 훅 정의를 검토·신뢰합니다. 설치만으로 신뢰가 생기지 않습니다.

```json
{"schema_version": 1, "wiki_root": "D:/Dev/Wiki"}
```

`JY_WIKI_CUES_HOME`은 테스트·대체 설정 디렉터리용 선택 환경 변수입니다. 기본 디렉터리에는 설정과 `state/<host>/<session-hash>.json`이 생깁니다. 상태는 ID·출처 revision·출력 여부만 저장하며 prompt·transcript는 읽어 저장하지 않습니다. 세션 파일은 남을 수 있으나 12시간 후 재사용하지 않습니다. 새 session_id로 재개하면 이전 범위를 이어받지 않으며 구체적인 새 요청부터 다시 선택합니다.

Wiki는 기존 동기화로 갱신합니다. 훅은 네트워크·MCP·모델·git pull을 호출하지 않으며 서버 최신성은 보장하지 않습니다. 안내에도 이 한계를 표시합니다. 코드가 바뀌면 plugin version을 올려 양쪽에 다시 패키징·설치하고 Codex 훅을 재검토합니다. 제거는 `codex plugin remove jy-wiki-cues@personal-codex`이며 공용 설정을 자동 삭제하지 않습니다.

## 검증과 한계

`python -X utf8 -m unittest tests.test_wiki_cues -v`는 관련/무관 요청, 사용자 예외 안내, 이벤트 재시도, 새 주제·세션·호스트 분리, resume/compact, 출처 변경·삭제, 실패·경로 경계를 확인합니다. 단어 기반 선택은 모든 표현이나 작업 도중 새로 발생한 상황을 잡지 못합니다. 전달 여부는 실제 호스트에서 따로 확인해야 하며, 모델이 교훈을 적용했는지와 사고 감소는 별도 행동 비교 대상입니다.

기존 PreCompact handoff, 전역 지침, 자동 차단·도구 재작성·학습 lifecycle은 이 플러그인의 범위가 아닙니다.
