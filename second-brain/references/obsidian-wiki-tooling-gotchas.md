---
title: obsidian-wiki 도구 동작 함정
tags: [tooling, knowledge-management, gotcha]
summary: >-
  graph-query는 frontmatter의 폴디드 스칼라 summary를 리터럴 '>-'로 읽어,
  요약이 사실상 비어 있는데도 index_only:true를 반환한다. 그대로 따르면 빈 답이 나온다.
project: second-brain
base_confidence: 0.75
provenance:
  extracted: 0.8
  inferred: 0.2
lifecycle_changed: 2026-08-04
sources:
  - "second-brain session (2026-08-04)"
category: references
lifecycle: draft
tier: supporting
created: 2026-08-04
updated: 2026-08-04
---

# obsidian-wiki 도구 동작 함정

## Findings

- `obsidian-wiki graph-query <vault> "<질문>"`은 후보 페이지의 `summary`를 문자열 `">-"`로 반환한다. 이 볼트의 페이지들이 YAML 폴디드 스칼라(`summary: >-` + 다음 줄 본문)로 요약을 쓰는데, graph-query의 frontmatter 파서가 `key: value` 한 줄 형태만 처리해 구분자 자체를 값으로 저장하기 때문이다.^[inferred]
- 그 결과 요약 길이가 2자가 되어 "요약만으로 답할 수 있다"는 판정이 잘못 발동하고, `index_only: true` + 빈 `should_read: []`가 함께 나온다. `wiki-query` 스킬의 결정 트리는 `index_only: true`면 `candidates[0].summary`만으로 답하라고 지시하므로, 그대로 따르면 **내용 없는 답**이 만들어진다.
- 대응: `summary`가 `">-"`·`">"`·`"|"`이면 `index_only`를 무시하고 섹션 grep 단계로 바로 내려간다. `candidates[].page` 경로와 `score` 랭킹은 정상이므로 "어느 페이지를 열지" 판단에는 그대로 쓸 수 있다.
- 근본 해결은 두 갈래 — (1) 페이지 frontmatter를 한 줄 `summary: "..."`로 통일, (2) graph-query 파서 수정. 볼트 쪽 통일이 싸지만 요약 200자 제한과 줄바꿈 가독성이 걸린다.^[ambiguous] 이 볼트 페이지 대부분이 Notion 심층 수집분이라 동일 패턴을 공유하므로 영향 범위는 전체다.
- 확인 근거: 후보로 뜬 4개 페이지 전부 `">-"` 반환, 실제 파일에는 정상적인 2줄 폴디드 summary 존재.

## Related

- [[references/claude-code-permission-guardrails|Claude Code 권한 가드레일 동작]]
- [[index|Wiki Index]]
- [[ROUTING|적재 라우팅 규칙]]
