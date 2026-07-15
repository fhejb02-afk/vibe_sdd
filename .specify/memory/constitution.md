<!--
Sync Impact Report
- Version change: new → 1.0.0
- Modified principles: new constitution
- Added sections: 추가 제약, 개발 워크플로
- Removed sections: none
- Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md, .specify/templates/checklist-template.md
- Follow-up TODOs: none
-->

# vibe_sdd 프로젝트 헌법

## Core Principles

### I. 스펙 우선
모든 기능은 구현 전에 명시적인 스펙 문서로 정의한다. 스펙에 없는 기능은 구현하지 않는다.

판정 기준:
- 구현 전에 스펙 문서가 작성되어 있는가?
- 구현 범위가 스펙에 명시된 내용으로 한정되는가?
- 스펙에 없는 기능이 코드에 포함되지 않았는가?

### II. 테스트 필수
핵심 기능(추가/완료 토글, 삭제, 남은 개수, 필터)은 pytest 자동화 테스트로 검증한다. 구현 완료의 기준은 해당 테스트가 통과하는 것이다.

판정 기준:
- 핵심 기능에 대한 pytest 테스트가 작성되어 있는가?
- 관련 테스트가 현재 코드에서 통과하는가?
- 회귀가 발생하지 않았는가?

### III. 설정 분리
데이터베이스 경로 등 환경설정 값은 .env 파일로 관리하고 저장소에 커밋하지 않는다. 필요한 환경변수는 .env.example 파일에 문서화한다.

판정 기준:
- 환경설정 값이 코드에 하드코딩되지 않았는가?
- .env.example에 필요한 변수와 설명이 있는가?
- .env 파일이 저장소에 포함되지 않았는가?

### IV. 추적 가능한 커밋
모든 커밋 메시지 앞에 태스크 ID를 붙인다. 예: "T03: 할 일 생성 API 구현"

판정 기준:
- 커밋 메시지 형식이 "TXX: ..."를 따른다?
- 각 변경이 추적 가능한 태스크 ID와 연결되는가?

### V. 단순성
요구사항에 없는 기능이나 라이브러리를 임의로 추가하지 않는다. 또한 이 프로젝트에서 생성되는 모든 문서(constitution, spec, plan, tasks, checklist, 분석 리포트 등)는 반드시 한국어로 작성한다.

판정 기준:
- 기능 추가가 명시된 요구사항 범위 안에 있는가?
- 새 라이브러리 도입이 불가피한 이유를 설명할 수 있는가?
- 생성된 문서가 한국어로 작성되어 있는가?

## 추가 제약
이 프로젝트의 환경설정 값은 .env와 .env.example를 통해 관리한다. 민감한 정보와 로컬 전용 설정은 저장소에 포함하지 않는다.

## 개발 워크플로
모든 구현은 스펙 정의 → 테스트 작성 → 구현 → 검증의 순서로 진행한다. 변경 사항이 생기면 관련 문서와 테스트를 함께 업데이트한다.

## Governance
이 헌법은 프로젝트의 최우선 개발 규칙이다. 변경은 사유와 영향 범위를 명시한 뒤, 관련 문서(spec, plan, tasks, checklist)와 함께 업데이트해야 한다.

버전은 MAJOR, MINOR, PATCH 규칙으로 관리한다. 원칙을 삭제하거나 재정의하는 변경은 MAJOR로 올린다. 새 원칙을 추가하거나 기존 원칙을 크게 확장하는 변경은 MINOR로 올린다. 문구 정정, 명확화, 오탈자 수정은 PATCH로 올린다.

모든 구현과 리뷰는 이 헌법의 원칙을 기준으로 검증해야 한다. 준수 여부가 불명확한 경우에는 변경 전후의 근거를 명확히 제시한 뒤 합의한다.

**Version**: 1.0.0 | **Ratified**: 2026-07-15 | **Last Amended**: 2026-07-15
