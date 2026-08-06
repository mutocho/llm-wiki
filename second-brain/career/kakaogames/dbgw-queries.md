---
title: dbgw 메타DB 운영 쿼리
topics: [career]
tags: [worklog, snippet, dbgw]
summary: >-
  dbgw 메타DB에서 인스턴스별 권한 현황을 뽑는 쿼리 모음. 업무 중 작성해 사용한 원본 그대로 보관.
sources:
  - internal:worklog
category: career
lifecycle: draft
lifecycle_changed: 2026-08-06
tier: supporting
base_confidence: 0.9
created: 2026-08-06
updated: 2026-08-06
---

# dbgw 메타DB 운영 쿼리

업무 중 작성해 사용한 쿼리를 원본 그대로 보관한다.

## 인스턴스에 부여된 권한 목록 추출

DB별로 접근 권한이 부여된 사용자를 묶어서 조회한다.

```sql
select c.dbName, group_concat(b.userName)
from user_grants as a
join users as b on b.id = a.userId
join `databases` as c on c.instanceId = a.instanceId and a.dbId = c.dbId
where a.instanceId = 26
group by c.dbName;
```

- `a.instanceId`가 대상 dbgw 인스턴스. 위 예시는 26.
- `databases`는 MySQL 예약어라 백틱이 필요하다.

## Related

- [[career/kakaogames/2026|2026년 작업 내역]]
- [[career/_hub|커리어 관리]]
- [[dba/operational-queries|운영 쿼리 모음 — 진단·권한·DDL/DML]]
