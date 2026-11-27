# universal-rag

**AI 어시스턴트의 클라우드 운영 지식 보강을 위한 Multimodal RAG** — 공개 커뮤니티에서 장애 유형별 해결 지식을 모으고, 메트릭 분석과 근본원인 진단을 LLM에 묻는 프롬프트를 제공합니다.

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

## 배경

RAG는 대개 텍스트 문서 중심으로 설계되어, 문서·차트·대시보드·Q&A 스레드가 섞여 있는 클라우드 운영 환경에서는 필요한 지식을 충분히 찾지 못합니다.
이 저장소는 1차년도 연구로 (1) 장애 유형과 증상을 키워드로 공개 Q&A 사이트에서 질문·답변 쌍을 모아 RAG 지식 저장소를 만들고,
(2) 메트릭을 LLM 친화적 표현으로 분석한 리포트를 근거로 근본 원인을 진단하는 2단계 프롬프트를 제공합니다.

## 구성

| 파일 | 내용 |
|---|---|
| `data_search.py` | 장애 지식 수집기. 장애 유형별 키워드로 웹 검색 → Stack Exchange 계열 사이트(Stack Overflow, Server Fault 등)의 답변이 달린 질문과 답변, Reddit 스레드와 댓글을 API로 받아 `knowledges/<장애 유형>.json`에 저장 |
| `prompt_store.py` | `analysis_prompt`: 장애 VM의 메트릭 시계열을 통계·메타데이터 근거로 분석하게 하는 지시문 / `agentic_prompt`: 분석 리포트를 근거로 SRE 관점에서 근본 원인 장애를 지목하고 대응을 제안하게 하는 지시문 |

### 수집 흐름

```
keyword_sheet.json  {"장애 유형": "증상 설명", ...}
        │  "Cloud {장애 유형}: {증상}" 으로 웹 검색 (최대 100건/유형)
        ├─ Stack Exchange 링크 → 사이트별 질문 ID 묶음 → 질문 본문 + 답변(점수 포함)
        └─ Reddit 링크        → 제출물 본문 + 댓글(점수 포함)
        ▼
knowledges/<장애 유형>.json   {"items": [{"question": ..., "answer": [{"score", "body"}, ...]}, ...]}
```

### 실행 준비

```bash
pip install requests praw tqdm
```

- `keyword_sheet.json`: 장애 유형 → 증상 설명 사전 (직접 작성)
- 웹 검색: Google Programmable Search(Custom Search JSON API)의 API 키와 검색 엔진 ID를 요청 파라미터(`key`, `cx`)에 넣어야 한다
- Reddit: `praw.ini` 또는 환경 변수에 Reddit API 자격 증명 설정
- `knowledges/` 출력 디렉터리 생성

```bash
mkdir -p knowledges
python data_search.py
```

수집한 지식은 [incident-retriever](https://github.com/OKESTRO-AICloudRecovery/incident-retriever)의 색인이나 일반 벡터 저장소에 넣어 검색할 수 있고,
`prompt_store.py`의 두 프롬프트는 메트릭 분석 → 근본원인 진단 순서로 이어 쓰면 됩니다.

## 관련 저장소

- [ts-align](https://github.com/OKESTRO-AICloudRecovery/ts-align) — 메트릭 시계열의 LLM 임베딩 정렬 (같은 1차년도 연구)
- [Structural_Chunking](https://github.com/OKESTRO-AICloudRecovery/Structural_Chunking) — RAG 문서 청킹 비교 실험
- [incident-retriever](https://github.com/OKESTRO-AICloudRecovery/incident-retriever) — 2차년도: 이종 관측 데이터 기반 유사 인시던트 하이브리드 검색
- [rca-reasoning](https://github.com/OKESTRO-AICloudRecovery/rca-reasoning) — 2차년도: 근본원인 추론 프롬프트와 가설 검증
- [과제 소개와 전체 저장소](https://github.com/OKESTRO-AICloudRecovery)

## 라이선스

[MIT License](LICENSE). 수집한 게시물의 저작권과 이용 조건은 각 사이트(Stack Exchange: CC BY-SA, Reddit API 이용약관)를 따릅니다.

## 사사

이 소프트웨어는 2025년도 정부(과학기술정보통신부)의 재원으로 정보통신기획평가원의 지원을 받아 수행된 연구의 결과물입니다.
(RS-2025-25441560, 클라우드 장애극복을 위한 AI 어시스턴트 기반 운영·관리 자동화 기술개발)

## Who We Are

오케스트로 주식회사 — http://okestro.com/
