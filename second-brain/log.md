---
title: Wiki Log
---

# Wiki Log

- [2026-08-06] CAPTURE type=decision page="synthesis/vault-governance-decisions.md" title="볼트 거버넌스 결정 — career 회사 라우팅·에이전트 규칙 단일화·브랜치 금지"
- [2026-08-06] UPDATE page="references/obsidian-wiki-tooling-gotchas.md" note="obsidian-git askpass chmod +x 반복 diff 함정 섹션 추가"

- [2026-08-04] INGEST source="_raw/ (15 files)" pages_updated=0 pages_created=15 mode=raw
- [2026-08-04] INIT vault_path="/Users/kakaogames/workspace/muto/second-brain" categories=concepts,entities,skills,references,synthesis,journal topics=dba,career
- [2026-08-04] QUERY query="SQL Server 설치와 관련된 설정" result_pages=2 mode=normal escalated=false
- [2026-08-04] QUERY query="메모리 사용량 보는 쿼리" result_pages=2 mode=normal escalated=false
- [2026-08-04] QUERY query="sql server sp_configure 관련 설정 설명해줘" result_pages=1 mode=normal escalated=false
- [2026-08-04] CAPTURE type=concept page="dba/postgresql-operations.md" title="psql 메타커맨드 — 타입 목록 \dT 계열"
- [2026-08-04] CAPTURE type=source page="references/obsidian-wiki-tooling-gotchas.md" title="obsidian-wiki 도구 동작 함정"
- [2026-08-04] QUERY query="aurora-dsql 관련 정리된 내용 알려줘" result_pages=1 mode=normal escalated=false
- [2026-08-04] UPDATE page="dba/aurora-dsql.md" source="AWS 공식 문서 대조" lifecycle=draft→verified confidence=0.6→0.85 note="스토리지 무제한 주장 정정, 공식 한도표·미지원 기능·DPU 과금 추가"
- [2026-08-04] QUERY query="위키에 운영 쿼리에 대한 내용 있어?" result_pages=7 mode=normal escalated=true
- [2026-08-04] CAPTURE type=concept page="dba/operational-queries.md" title="운영 진단 쿼리 모음 (MySQL·PostgreSQL·SQL Server)" note="볼트 첫 SQL 코드블록 페이지. 표준 시스템 뷰 기반, 실행 검증 전(draft)"
- [2026-08-04] UPDATE page="dba/operational-queries.md" note="권한 감사(12)·권한 부여(13)·DDL 안전 패턴(14)·DML 안전 패턴(15) 추가. search_path 설정 지식 흡수. 읽기전용/변경 경계 명시"
- [2026-08-05] CAPTURE type=concept page="dba/mysql-partition-pruning-prepared-stmt-bug.md" title="MySQL 8.0.42 파티션 pruning 캐시 회귀 (Bug #119309)" note="공식 버그 리포트 + 자체 재현 테스트. dba/career 양쪽 적재"
- [2026-08-05] UPDATE page="career/2026.md" note="8월 항목 추가 — Bug #119309 영향 조사·재현 테스트 (이후 career/kakaogames/2026.md로 이동)"
- [2026-08-06] QUERY query="aws aurora dsql 설명들은거 알려줘" result_pages=1 mode=normal escalated=false
- [2026-08-06] UPDATE page="dba/mysql-partition-pruning-prepared-stmt-bug.md" note="리포트 재확인 — 최소 재현 케이스·내부 함수명·SP 포함 추가. 사내 문서의 8.0.41 표기 정정(실제 8.0.42), Reorganize는 재발 방지가 아닌 리셋임을 명시"
- [2026-08-06] CAPTURE type=synthesis page="synthesis/verbal-source-verification-policy.md" title="구술·사내 출처는 공식 문서 대조 전까지 승격하지 않는다"
- [2026-08-06] QUERY query="MySQL 버전 업그레이드 관련 버그 내용 찾아서 보여줘" result_pages=2 mode=normal escalated=false
- [2026-08-06] FIX note="세션 날짜 오기 정정 — mysql-partition-pruning 페이지(created 08-05/updated 08-06), verbal-source-verification-policy(08-06), log.md 5줄, hot.md 재정렬"
- [2026-08-06] CAPTURE type=worklog page="career/kakaogames/dbgw-queries.md" title="dbgw 메타DB 운영 쿼리" note="원본 그대로 보관"
- [2026-08-04] CAPTURE type=concept page="dba/postgresql-operations.md" title="롤별 search_path 설정 (단일 스키마 DB)"
- [2026-08-04] CAPTURE type=decision page="ROUTING.md" title="career 범위 확장 — 회사 수행 작업 전체 기록"
- [2026-08-04] QUERY query="forum db에 권한 부여한 내용 알려줘" result_pages=2 mode=normal escalated=false
- [2026-08-04] LINT issues_found=4 orphans=0 broken_links=2 stale=0 contradictions=0 prov_issues=0 missing_summary=2 fragmented_clusters=0 visibility_issues=0 promotion_candidates=0 synthesis_gaps=0 relationship_issues=0 links_fixed=2
- [2026-08-04] LINT_FIX page="career/2026.md" added=summary,sources,category,lifecycle,base_confidence,tier,created,updated
- [2026-08-04] CAPTURE type=source page="references/obsidian-wiki-tooling-gotchas.md" title="Wikilink 경로 접두어 함정 (기존 페이지 병합)"
- [2026-08-04] EXPORT target="Notion 🗃️ DBA (3aefb969b8be801280b8dc2ff35fbefb)" pages=14 source="dba/*.md" direction=vault→notion
- [2026-08-04] CAPTURE type=source page="dba/aurora-dsql.md" title="AWS Aurora DSQL — 분산 서버리스 PostgreSQL 호환 DB"
- [2026-08-04] LINT issues_found=0 orphans=0 broken_links=0 stale=0 contradictions=0 prov_issues=0 missing_summary=0 fragmented_clusters=0 visibility_issues=0 promotion_candidates=0 synthesis_gaps=0 relationship_issues=0
- [2026-08-04] EXPORT target="Notion 🗃️ DBA" pages=1 source="dba/aurora-dsql.md"
- [2026-08-06T22:12:45+09:00] QUERY query="AWS Aurora DSQL 관련한 내용 찾아줘" result_pages=2 mode=normal escalated=false
- [2026-08-06T22:14:49+09:00] CAPTURE type=session page="career/kakaogames/dba-agent-work-plan.md" title="DBA Agent 구조 개편 및 주간 분석 작업 계획"
- [2026-08-06T22:58:55+09:00] QUERY query="내일 할 작업에 대해 정리해줘" result_pages=1 mode=normal escalated=false
- [2026-08-07T19:23:30+09:00] CAPTURE type=schedule page="personal/todo.md" title="DBGW 성능 개선 및 DBGWS 승인 절차" due="2026-08-10T10:00:00+09:00" source="Slack message"
