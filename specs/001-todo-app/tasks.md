# Tasks: 오늘의 할 일 웹 앱

**Input**: 설계 문서 /specs/001-todo-app/plan.md, spec.md, research.md, data-model.md, contracts/

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ 모두 준비되어 있어야 한다.

**Organization**: 사용자 스토리 우선순위(P1 → P2)에 따라 배치하고, 화면(UI)은 API 구현 이후에 진행한다.

## Format: `[ID] [P?] [Story] Description — 완료 조건`

- **[P]**: 다른 파일을 수정하고 의존성이 없는 경우 병렬로 진행 가능
- **[Story]**: 사용자 스토리 식별자 (예: US1, US2)
- 완료 조건은 해당 태스크가 완료되었다고 판단할 수 있는 테스트 또는 검증 기준을 포함한다.

## Phase 1: Setup (공통 인프라)

**Purpose**: 프로젝트 구조와 기본 환경 구성

- [ ] T001 프로젝트 구조를 구현 계획에 맞게 생성한다. 완료 조건: app/, app/templates/, tests/ 디렉터리가 생성되고 기본 파일 경로가 정리되어 있다.
- [ ] T002 FastAPI, SQLAlchemy, Pydantic, pytest 의존성을 설치하고 기본 실행 환경을 구성한다. 완료 조건: `pytest`와 `fastapi`가 정상 import된다.
- [ ] T003 [P] 환경 변수 관리용 `.env` 및 `.env.example` 파일을 준비한다. 완료 조건: `DATABASE_URL`이 문서화되고 기본 실행에 필요한 값이 정의되어 있다.

---

## Phase 2: Foundational (공통 기반)

**Purpose**: 사용자 스토리 구현 전에 필요한 공통 기반을 구성한다.

- [ ] T004 데이터베이스 연결 설정과 세션 관리 모듈을 구현한다. 완료 조건: `app/database.py`에서 세션 생성이 가능하고, SQLite 연결 경로가 환경 변수로 읽힌다.
- [ ] T005 ORM 모델과 스키마를 정의한다. 완료 조건: `Todo` 모델과 생성/응답 스키마가 정의되어 있고, 기본 필드 검증이 가능하다.
- [ ] T006 [P] CRUD 로직 모듈을 구현한다. 완료 조건: 생성, 목록 조회, 완료 토글, 삭제 로직이 각각 호출 가능하다.
- [ ] T007 [P] 메인 라우터와 헬스 체크 엔드포인트를 연결한다. 완료 조건: `/`, `/health`, `/api/todos` 경로가 FastAPI에서 정상 등록된다.

---

## Phase 3: User Story 1 - 할 일 생성과 입력 검증 (우선순위: P1)

**Goal**: 사용자가 새 할 일을 추가하고 잘못된 입력을 거절할 수 있다.

**Independent Test**: 생성 API와 입력 검증을 통해 핵심 생성 흐름이 독립적으로 검증 가능하다.

### Tests for User Story 1

- [ ] T008 [P] [US1] 생성 API의 성공/실패 케이스 테스트를 작성한다. 완료 조건: 빈 제목으로 생성 요청 시 422 응답이 발생하고, 정상 제목은 200/201 응답과 함께 생성된다.
- [ ] T009 [P] [US1] 목록 조회 API의 기본 응답 테스트를 작성한다. 완료 조건: 생성 후 목록 조회 시 새 항목이 포함된다.

### Implementation for User Story 1

- [ ] T010 [US1] 생성 API를 구현한다. 완료 조건: `POST /api/todos` 요청이 성공하면 할 일이 저장되고 응답 본문에 title/completed 값이 포함된다.
- [ ] T011 [US1] 빈 제목 검증 로직을 구현한다. 완료 조건: 공백만 있는 제목은 저장되지 않고 422 응답을 반환한다.
- [ ] T012 [US1] 목록 조회 API를 구현한다. 완료 조건: `GET /api/todos`가 저장된 할 일 목록을 반환한다.

---

## Phase 4: User Story 2 - 완료 토글, 삭제, 남은 개수 (우선순위: P1)

**Goal**: 사용자가 할 일을 완료/취소하고 삭제하며 남은 개수를 확인할 수 있다.

**Independent Test**: 상태 변경과 삭제 동작을 하나씩 독립적으로 검증할 수 있다.

### Tests for User Story 2

- [ ] T013 [P] [US2] 완료 토글 API 테스트를 작성한다. 완료 조건: 완료 여부가 true/false로 바뀌고 응답이 갱신된다.
- [ ] T014 [P] [US2] 삭제 API 테스트를 작성한다. 완료 조건: 존재하는 ID 삭제 시 204 응답, 없는 ID는 404 응답을 반환한다.
- [ ] T015 [P] [US2] 남은 개수 계산 로직 테스트를 작성한다. 완료 조건: 완료되지 않은 항목 수가 정확히 계산된다.

### Implementation for User Story 2

- [ ] T016 [US2] 완료 토글 API를 구현한다. 완료 조건: `PATCH /api/todos/{id}` 요청으로 completed 값이 토글된다.
- [ ] T017 [US2] 삭제 API를 구현한다. 완료 조건: `DELETE /api/todos/{id}`가 삭제 후 정상 응답을 반환하고, 없는 ID는 404를 반환한다.
- [ ] T018 [US2] 남은 개수 계산과 상태 응답 로직을 구현한다. 완료 조건: 목록 응답에 완료되지 않은 항목 수가 정확히 반영된다.

---

## Phase 5: User Story 3 - 필터링과 빈 상태 (우선순위: P2)

**Goal**: 사용자가 필터 조건에 따라 목록을 확인하고 빈 상태를 인지할 수 있다.

**Independent Test**: 필터링과 빈 상태 표시 로직이 독립적으로 검증 가능하다.

### Tests for User Story 3

- [ ] T019 [P] [US3] 필터 파라미터 테스트를 작성한다. 완료 조건: `status=all|active|completed`에 따라 올바른 항목만 반환된다.
- [ ] T020 [P] [US3] 빈 상태 응답 테스트를 작성한다. 완료 조건: 항목이 없을 때 빈 상태에 대한 응답/표시 값이 제공된다.

### Implementation for User Story 3

- [ ] T021 [US3] 목록 조회에 필터 파라미터를 적용한다. 완료 조건: `status=active`와 `status=completed` 요청이 각각 올바른 결과를 반환한다.
- [ ] T022 [US3] 빈 상태 데이터와 안내 메시지를 준비한다. 완료 조건: 항목이 없을 때 사용자에게 빈 상태 안내가 제공된다.

---

## Phase 6: User Story 4 - 화면(UI)과 비동기 동작 (우선순위: P2)

**Goal**: 화면에서 API를 호출하고 목록, 남은 개수, 필터, 빈 상태를 실시간으로 갱신한다.

**Independent Test**: 화면 렌더링과 비동기 이벤트가 독립적으로 검증 가능하다.

### Tests for User Story 4

- [ ] T023 [P] [US4] 화면 렌더링과 이벤트 동작 테스트를 작성한다. 완료 조건: 추가/완료/삭제/필터 동작 후 목록과 남은 개수가 갱신된다.

### Implementation for User Story 4

- [ ] T024 [US4] 메인 템플릿을 구현한다. 완료 조건: 입력 폼, 목록 영역, 필터 버튼, 빈 상태 메시지, 남은 개수 영역이 표시된다.
- [ ] T025 [US4] 클라이언트 JavaScript로 fetch 기반 CRUD 이벤트를 연결한다. 완료 조건: 추가/완료/삭제/필터 변경 시 화면이 즉시 갱신된다.
- [ ] T026 [US4] 반응형 스타일과 완료 항목 시각화를 적용한다. 완료 조건: 360px 폭에서도 주요 UI가 정상적으로 보이고, 완료 항목은 취소선과 흐린 색으로 표시된다.

---

## Phase 7: Integration & Polish

**Purpose**: 전체 흐름을 통합하고 회귀를 검증한다.

- [ ] T027 통합 테스트를 작성하고 전체 테스트 스위트를 실행한다. 완료 조건: 전체 pytest 테스트가 통과한다.
- [ ] T028 코드 정리와 문서 보완을 진행한다. 완료 조건: README 또는 구현 문서에 핵심 실행 방법이 정리되어 있다.
