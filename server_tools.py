from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

# # 호출 1: 웹 검색 (Google 서버가 검색)
# search_response = client.models.generate_content(
#     model="gemini-3.5-flash",
#     contents="What is the latest ROS 2 distribution release? Answer in one sentence.",
#     config=types.GenerateContentConfig(
#         tools=[types.Tool(google_search=types.GoogleSearch())],
#     ),
# )

# print("===== 웹 검색 =====")
# print(search_response.text)

# meta = search_response.candidates[0].grounding_metadata
# if meta and meta.web_search_queries:
#     print(f"[검색어] {meta.web_search_queries}")
# if meta and meta.grounding_chunks:
#     for chunk in meta.grounding_chunks[:3]:
#         print(f"[출처] {chunk.web.title}")

# 호출 2: 코드 실행 (Google 샌드박스에서 Python 실행)
battery_log = [98, 96, 95, 91, 90, 87, 85, 82, 80, 77]  # 1분 간격 배터리 %

code_response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=(
        f"AGV battery log sampled every minute: {battery_log}. "
        "Using code, compute the mean drain per minute and its standard deviation, "
        "then estimate how many minutes until the battery reaches 20%."
    ),
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    ),
)

print("\n===== 코드 실행 =====")
for part in code_response.candidates[0].content.parts:
    if part.executable_code:
        print(f"[모델이 작성한 코드]\n{part.executable_code.code}")
    elif part.code_execution_result:
        print(f"[실행 결과]\n{part.code_execution_result.output}")
    elif part.text:
        print(f"[최종 답변]\n{part.text}")