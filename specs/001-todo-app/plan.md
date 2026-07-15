# Implementation Plan: 오늘의 할 일 웹 앱

**Branch**: `001-todo-app` | **Date**: 2026-07-15 | **Spec**: [specs/001-todo-app/spec.md](spec.md)

**Input**: Feature specification from /specs/001-todo-app/spec.md

## Summary

이 기능은 FastAPI 기반의 단일 페이지 할 일 관리 웹 앱을 구현한다. 사용자는 할 일을 생성·완료·삭제하고, 필터와 남은 개수를 통해 상태를 확인할 수 있으며, 브라우저의 localStorage를 통해 새로고침과 재시작 후에도 데이터가 유지되도록 한다.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic, Jinja2, pytest, httpx/fastapi TestClient

**Storage**: SQLite, 데이터베이스 경로는 .env의 DATABASE_URL 환경변수로 관리

**Testing**: pytest + FastAPI TestClient

**Target Platform**: 웹 브라우저 기반

**Project Type**: web-service

**Performance Goals**: 단일 사용자 기준, 동시 접속이 많지 않으므로 기본 응답성 유지

**Constraints**: 별도 빌드 도구 없이 단일 HTML 페이지로 구현하고, 환경 변수 기반 설정으로 로컬/배포 환경을 분리해야 함

**Scale/Scope**: 단일 사용자 기준의 작은 규모 앱

## Constitution Check

- [x] 스펙 우선: 기능 범위는 명시된 스펙 문서에 정리되어 있다.
- [x] 테스트 필수: 핵심 API 동작은 pytest로 검증한다.
- [x] 설정 분리: SQLite 경로는 .env 기반으로 관리한다.
- [x] 추적 가능한 커밋: 구현 단계에서 태스크 ID를 붙여 관리한다.
- [x] 단순성: 서버/DB를 과도하게 확장하지 않고 단순 구조로 구현한다.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-app/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
app/
├── main.py
├── models.py
├── schemas.py
├── crud.py
└── database.py

app/templates/
└── index.html

tests/
└── test_api.py
```

**Structure Decision**: FastAPI 애플리케이션을 app 패키지로 구성하고, 템플릿은 app/templates/index.html에 두며, API 테스트는 tests/test_api.py에서 관리한다.

## Complexity Tracking

없음.
