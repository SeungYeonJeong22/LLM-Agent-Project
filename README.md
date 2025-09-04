# 🧠 LLM 에이전트 프로젝트

> 프롬프트 입력만으로 맞춤형 [채용 정보, 식당, ...] 등 탐색할 수 있는 지능형 LLM 에이전트

---

## 📌 프로젝트 개요

이 프로젝트는 유저의 자연어 질문을 기반으로 적절한 파라미터를 추출하고, 사람인(Saramin) API 호출, 식당 데이터 등을 활용하여 전문적이고 최신화된 정보를 반환하는 **LLM 기반 에이전트 시스템**입니다.  
LangChain과 OpenAI의 Function Calling 기능을 활용하여 **멀티 API 대응**이 가능한 구조로 확장성을 고려하여 설계되었습니다.

---

## 🛠️ 주요 기능

- ✅ 자연어 질문에서 채용 정보 검색을 위한 파라미터 추출
- ✅ OpenAI Function Calling 기반 파라미터 추론
- ✅ 사람인 API를 호출하여 채용 공고 조회
- ✅ API 응답을 정제하여 LLM에 입력 → 자연어 요약 응답 생성
- ✅ 멀티 API 확장을 위한 범용 설계 구조

---

## 📂 프로젝트 구조
```
workspace/
│
├── main.py                        # 실행 진입점
├── README.md                      # 프로젝트 설명서
│
├── Functions/
│   ├── chat.py                    # 전체 챗 흐름 (쿼리 → API → LLM 응답)
│
├── Settings/
│   ├── agent.py                   # LLM 및 FunctionChain 관리
│   ├── apis.py                    # SaraminAPI 등 외부 API 정의
│   ├── router.py                  # 유저 쿼리 → 적절한 API 라우팅
│
├── Schema/
│   └── api.json                   # API용 function-calling 스키마
│
```
---

## 💬 유저 흐름 예시
초기 단계에서는 "취업", "식당" 과 같은 명확한 카테고리를 입력받고 있습니다. 추후에 자동으로 context에 기반해 이를 유추하고 답변을 제공할 예정입니다.

User: "취업"  AI직무와 관련해서 나와있는 공고문들을 모두 알려줘

→ Saramin API로 라우팅
→ Function Calling으로 파라미터 추출
→ Saramin API 호출
→ 응답 파싱
→ LLM이 자연어로 결과 요약 및 응답

---

## 🚀 실행 방법

`pip install -r requirements.txt` \
`python main.py`