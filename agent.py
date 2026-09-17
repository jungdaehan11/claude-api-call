from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

# 1. 도구 정의: 이름, 설명, 입력 형식(JSON 스키마)
get_battery = types.FunctionDeclaration(
    name="get_battery",
    description="Get the current battery percentage of an AGV.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "robot_id": {"type": "string", "description": "AGV id, e.g. agv-01"}
        },
        "required": ["robot_id"],
    },
)

get_nav_status = types.FunctionDeclaration(
    name="get_nav_status",
    description="Get the current navigation state and zone of an AGV.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "robot_id": {"type": "string", "description": "AGV id, e.g. agv-01"}
        },
        "required": ["robot_id"],
    },
)

# 2. 실제 도구 실행: 지금은 가짜 데이터
#    나중에 ROS 2 토픽(/battery_state, Nav2 상태)을 읽도록 바꿀 부분
def run_tool(name, args):
    if name == "get_battery":
        return {"robot_id": args["robot_id"], "battery_percent": 24}
    if name == "get_nav_status":
        return {"robot_id": args["robot_id"], "state": "IDLE", "zone": "A"}
    raise ValueError(f"Unknown tool: {name}")

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[get_battery, get_nav_status])],
    # 자동 실행을 끄고 루프를 직접 돌림 (아까 뜬 경고의 그 기능)
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    system_instruction=(
        "You are an AGV fleet assistant. A delivery to zone B requires "
        "at least 30% battery and the robot must be IDLE. Answer in Korean."
    ),
)

contents = [
    types.Content(
        role="user",
        parts=[types.Part(text="agv-01이 지금 B구역 배송 나갈 수 있어?")],
    )
]

# 3. 에이전트 루프 (무한 반복 방지용 최대 5턴)
for turn in range(1, 6):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents,
        config=config,
    )

    if not response.function_calls:
        # Claude의 end_turn에 해당
        print(f"[턴 {turn}] 최종 답변:\n{response.text}")
        break

    # Claude의 tool_use에 해당
    contents.append(response.candidates[0].content)

    result_parts = []
    for call in response.function_calls:
        result = run_tool(call.name, call.args)
        print(f"[턴 {turn}] 도구 호출: {call.name}({call.args}) -> {result}")
        result_parts.append(
            types.Part.from_function_response(name=call.name, response=result)
        )

    contents.append(types.Content(role="user", parts=result_parts))
else:
    print("최대 턴 수에 도달해 중단했습니다.")