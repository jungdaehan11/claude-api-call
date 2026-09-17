# claude-platform-101

Anthropic Academy **Claude Platform 101** 과정(2026.09 수료)을 따라가며 LLM API 연동을 실습한 저장소입니다.
Gemini API와 Claude API로 같은 개념을 구현해 비교했고, AGV 상태 조회·이동 명령용 MCP 서버를 만들어 서버 측 안전 검증을 적용했습니다.

## 실습 목록

| 파일 | 내용 | API |
|---|---|---|
| `main.py` / `claude_main.py` | 첫 API 호출, 코드 리뷰 | Gemini / Claude |
| `agent.py` | 에이전트 루프 직접 구현 (AGV 상태 도구) | Gemini |
| `agent_auto.py` | 자동 함수 호출 | Gemini |
| `thinking.py` | 생각 수준(low/high) 비교, 배차 판단 | Gemini |
| `server_tools.py` | 서버 도구 (코드 실행) | Gemini |
| `skill_report.py` + `agv-report-skill/` | 스킬 방식 AGV 일일 보고서 | Gemini |
| `agv_mcp_server.py` | AGV MCP 서버 (조회·이동 명령·메모리, 안전 검증) | - |
| `mcp_list.py` / `mcp_agent.py` | MCP 도구 목록 조회 / 에이전트 연결 | - / Gemini |
| `managed_agent.py` | 관리형 에이전트 | Claude |

## 설계 포인트
- LLM이 이동 명령을 요청해도 **MCP 서버가 배터리·맵 범위·상태를 코드로 검증**해 거절 가능
- 충전소 이동은 배터리 검사 예외로 처리 (실행 중 발견한 설계 버그 수정)
- 실시간 제어(SLAM·장애물 회피)에는 LLM을 넣지 않고 상위 판단에만 사용