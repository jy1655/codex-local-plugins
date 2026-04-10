---
name: jy-slop-remover
description: Use when reviewing a file for AI-generated code smells like obvious comments, over-defensive code, or deep nesting.
---

# JY Slop Remover

## Overview

AI가 생성한 코드 악취를 파일 단위로 탐지하고 제거한다. 기능은 반드시 보존. 의심스러우면 건드리지 않는다.

입력: 정확히 1개 파일. 여러 파일이면 파일당 병렬 호출.

이 skill은 실행 지향적이다. 실제 파일을 수정하므로 Default mode에서만 정상 동작한다.

## When to Use

- AI가 생성한 코드를 정리할 때
- 코드 리뷰에서 "AI스러운" 패턴이 보일 때
- "슬롭 제거", "코드 정리", "AI 냄새 제거" 요청 시

## Quick Reference

| 탐지 대상 | 제거 | 유지 |
|----------|------|------|
| 자명한 주석 | `x += 1 # increment x` | WHY를 설명하는 주석, 이슈 링크 |
| 과도한 방어 코드 | None 불가능한 값의 null 체크 | 시스템 경계 검증 (사용자 입력, 외부 API) |
| 스파게티 네스팅 | 3단 이상 중첩 if-else | 도메인 상 불가피한 분기 |
| 죽은 코드 | 주석 처리된 코드, `# removed` | 의도적 비활성화 (피처 플래그) |
| 과잉 추상화 | 한 번만 쓰이는 헬퍼 함수 | 재사용 증거가 있는 추상화 |
| 역호환 잔재 | `_old_name = new_name` | 실제 외부 의존이 있는 경우 |

## 탐지 기준 상세

### 1. 자명한 주석

제거:
- 코드를 그대로 반복하는 주석
- 간단한 메서드의 자명한 독스트링
- 섹션 구분선 (`# ===== HELPERS =====`)
- 구체적 계획 없는 `# TODO: future enhancement`

유지:
- 비즈니스 로직 설명 (WHY)
- 정규식 설명
- 기존 코드 스타일과 일치하는 주석

### 2. 과도한 방어 코드

제거:
- None이 될 수 없는 값의 null 체크
- 발생 불가능한 예외의 try-except
- 정적 타입 파라미터의 `isinstance()` 체크
- 빈 문자열이 무효한 필수 파라미터의 기본값

유지:
- I/O 에러 핸들링
- nullable DB 필드 체크
- 테스트 코드의 assertion

### 3. 스파게티 네스팅

리팩토링: 중첩 if-else를 early return/guard clause로 변환.

## 프로세스

1. **읽기**: 파일 전체를 읽고 슬롭 인스턴스를 라인 번호와 함께 식별
2. **판단**: 각 항목에 대해 — 기능이 변하는가? 테스트가 깨지는가? 맥락상 필요한가? 가독성이 떨어지는가? 하나라도 YES면 **건너뛰기**
3. **수정**: 한 번에 하나의 논리적 변경. Edit 도구 사용
4. **보고**: 제거한 항목, 건너뛴 항목과 이유, 전후 비교

## Mode-Aware Behavior

### If current collaboration mode is Default

- 이 skill의 정상 실행 모드다.
- 파일을 읽고, 슬롭을 식별하고, Edit 도구로 수정한다.

### If current collaboration mode is Plan

- 실제 파일 수정은 하지 않는다.
- 이렇게 유도한다:
  - "이건 파일 수정 workflow라 Default mode가 맞습니다. `Shift+Tab`으로 Plan Mode에서 나온 뒤 다시 실행하세요."
- 대신 탐지된 슬롭 목록과 제거 계획은 compact preview로 남긴다.
- Plan Mode 안에서 "지금 파일을 수정하겠다"라고 가장하지 않는다.

## Iron Rule

**의심스러우면 변경하지 않는다.** False negative가 코드 파손보다 낫다.

## Common Mistakes

- 여러 파일을 한 호출에 처리 — 파일당 1회, 여러 파일은 병렬
- WHY를 설명하는 주석을 "자명하다"고 삭제 — 비즈니스 로직 주석은 유지
- 시스템 경계의 방어 코드를 "과도하다"고 삭제 — 사용자 입력/외부 API 검증은 유지
- 기존 코드 스타일과 다른 기준 적용 — 프로젝트 컨벤션 우선
- 한 번에 대량 수정 후 검증 — 논리적 단위로 나눠서 수정
