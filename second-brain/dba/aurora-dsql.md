---
title: AWS Aurora DSQL — 분산 서버리스 PostgreSQL 호환 DB
tags: [dba, aws, aurora, architecture]
topics: [dba]
summary: >-
  Aurora DSQL 핵심 특성 — 멀티 리전 multi-master ACID, 낙관적 락, 커넥션당
  Firecracker VM, FK/Trigger/VACUUM 없음, 앱 리트라이 필수. 세미나 노트 기반.
project: second-brain
base_confidence: 0.6
provenance:
  extracted: 0.85
  inferred: 0.15
lifecycle_changed: 2026-08-04
sources:
  - "AWS Aurora DSQL 세미나 노트 (2026-08-04)"
category: dba
lifecycle: draft
tier: supporting
created: 2026-08-04
updated: 2026-08-04
---

# AWS Aurora DSQL

세미나 노트 기반 — 공식 문서 대조 전이므로 수치·제약은 재검증 필요.

## 아키텍처

- 분산 데이터베이스(QP 플릿). 멀티 리전 **multi-master**에서 ACID 보장.
- 내부 아키텍처는 PostgreSQL이 아니지만 **문법은 PostgreSQL 호환** — PG 16 기반, 차기 v2는 PG 18 기반 예정(내년).^[세미나 발언 — 로드맵은 변동 가능]
- 커넥션당 VM 1:1 매칭 (Firecracker microVM).
- VACUUM 없음. 실행 계획은 PG와 동일.
- **buffer pool 개념이 없어 모든 read가 disk에서 읽음.**
- 버전 업그레이드 다운타임 zero. 스토리지 크기 제약 없음. 스케일링 고민 불필요.
- MySQL용 DSQL 계획 없음.

## 동시성 — 낙관적 락

- UPDATE 시 경합이 없다는 가정으로 진행, **commit 시점에 비교 후 처리**.
- 경합 실패 시 앱 레벨 비즈니스 로직 필요: 재처리 or 실패 처리.
- **자체 리트라이 로직·Failover 대응을 앱에서 구현해야 함.**

## 제약·주의점

- FK, Trigger 미지원 (외 몇몇 제약 존재 — 공식 제약 목록 확인 필요).
- 결과셋 크기 제한 있음 (작은 VM 단위 특성).
- OLAP 성능은 나오지 않음 — OLTP 용도.
- 커넥션 풀링 사용 권장.
- throughput은 높으나 멀티 리전 구성 시 write latency 증가 가능.

## 적용 판단

- **단일 리전이라도 Write가 많은 워크로드라면 DSQL이 해법이 될 수 있다.**
- 비용 = IO + storage size.

## Related

- [[dba/cloud-platform-knowledge|클라우드·플랫폼 지식]]
- [[dba/postgresql-operations|PostgreSQL 운영 지식]]
- [[dba/_hub|DBA 지식베이스]]
