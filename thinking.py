from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

question = """
B구역에 급한 배송 1건을 배정해야 해. 규칙:
- 배터리 30% 이상이어야 출발 가능
- 이동 1m당 배터리 0.1% 소모, 도착 후에도 20% 이상 남아야 함
- 적재 중인 로봇은 현재 짐을 먼저 내려야 해서 +60초
- 가장 빨리 도착하는 로봇 선택 (속도는 모두 1 m/s)

agv-01: 배터리 45%, B까지 180m, 빈 상태
agv-02: 배터리 90%, B까지 120m, 적재 중
agv-03: 배터리 32%, B까지 40m, 빈 상태

누구를 보내야 해? 마지막 줄에 로봇 id만 적어줘.
"""

for level in ["low", "high"]:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=question,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level=level,
                include_thoughts=True,
            ),
        ),
    )

    print(f"\n===== thinking_level: {level} =====")
    for part in response.candidates[0].content.parts:
        if not part.text:
            continue
        if part.thought:
            print(f"[생각 요약]\n{part.text}\n")
        else:
            print(f"[최종 답변]\n{part.text}")

    usage = response.usage_metadata
    print(f"[토큰] 생각: {usage.thoughts_token_count}, 답변: {usage.candidates_token_count}")