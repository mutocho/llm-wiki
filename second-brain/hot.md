---
title: Hot Cache
updated: 2026-08-04
---

# Hot Cache

*A ~500-word semantic snapshot of recent activity. Updated after every major write operation.*

## Recent Activity

- [2026-08-04] CAPTURE — obsidian-wiki graph-query의 폴디드 summary 파싱 함정을 [[references/obsidian-wiki-tooling-gotchas]]로 승격. psql `\dT` 메타커맨드는 [[dba/postgresql-operations]]에 섹션 추가.
- [2026-08-04] INGEST — `_raw/` 15건을 정식 페이지로 승격 (dba 13, career 1, references 1). Notion 'Muto - DBA 통합 포털' 전체 뎁스(~140페이지) 수집분 포함.
- [2026-08-04] Notion 포털 심층 감사 — 교정 백로그 20건(P1: TRUNCATE 생성기, QA 호스트명 노출, 개인 이메일 잔존 등) 도출.
- [2026-08-04] INIT — DBA/커리어 이중 허브 볼트 생성, git auto-sync 훅 구성.

## Active Threads

- Notion 원본 P1 교정 6건 대기 — [[dba/notion-remediation-backlog]]
- Notion 포털 vs 로컬 볼트 역할 분담 미결정 — [[dba/notion-llm-wiki-governance]]

## Key Takeaways

- MySQL 회수 릴리스(8.0.29, 8.0.38/8.4.1)는 사용 금지 — [[dba/mysql-operations]]
- `idle_in_transaction_session_timeout` 미설정이 PG bloat 장애 1순위 원인 — [[dba/postgresql-operations]]
- AWS PI 콘솔 2026-07-31 종료 → Database Insights 전환 — [[dba/monitoring-incident-runbook]]
- graph-query의 `index_only: true`는 신뢰 금지 — 폴디드 summary를 못 읽어 오탐 — [[references/obsidian-wiki-tooling-gotchas]]

## Flagged Contradictions

- KB 색인 실측 33건/검증완료 19건 vs 포털 기록 31건/17건 — 수기 집계 드리프트 확인됨.
