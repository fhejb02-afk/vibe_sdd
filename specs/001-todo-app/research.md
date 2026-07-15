# 연구 결과: 오늘의 할 일 웹 앱

## Decision 1: 데이터 저장 방식

**Decision**: 브라우저의 localStorage를 사용해 할 일 데이터를 저장한다.

**Rationale**: 요구사항에 명시된 데이터 영속성을 만족하면서도 서버 기반 저장소를 도입하지 않아 구현 복잡도를 낮출 수 있다. 단일 사용자, 작은 규모 앱에 적합하다.

**Alternatives considered**:
- 서버 기반 DB와 REST API: 더 범용적이지만 백엔드와 배포 구성이 복잡해진다.
- 메모리 저장: 새로고침 시 데이터가 사라져 요구사항을 만족하지 못한다.

## Decision 2: API 구조

**Decision**: REST 스타일의 간단한 API를 사용한다.

**Rationale**: 할 일 CRUD와 완료 토글이 명확하게 표현되며, FastAPI와 TestClient 조합으로 테스트가 용이하다.

**Alternatives considered**:
- GraphQL: 기능은 과도하고 현재 범위와 불필요하게 맞지 않는다.
- 단일 엔드포인트로 모든 동작 처리: 확장성과 가독성이 떨어진다.

## Decision 3: 프론트엔드 렌더링 방식

**Decision**: 서버가 HTML 템플릿을 제공하고, 클라이언트는 fetch로 비동기적으로 데이터를 갱신한다.

**Rationale**: 요구사항에 따라 페이지 새로고침 없이 동작해야 하며, 별도 빌드 도구 없이도 구현 가능하다.

**Alternatives considered**:
- 순수 서버 렌더링만 사용: 상태 변경 시 전체 페이지를 다시 그려야 하므로 UX가 떨어진다.
- React/Vue 같은 프레임워크: 빌드 도구가 필요해 현재 계획과 어긋난다.
