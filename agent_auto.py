from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

# 평범한 Python 함수. 스키마를 따로 안 씁니다.
# 타입 힌트와 docstring이 곧 도구의 입력 형식과 설명이 됩니다.
def get_battery(robot_id: str) -> dict:
    """Get the current battery percentage of an AGV.

    Args:
        robot_id: AGV id, e.g. agv-01
    """
    print(f"  [도구 실행] get_battery({robot_id})")
    return {"robot_id": robot_id, "battery_percent": 24}


def get_nav_status(robot_id: str) -> dict:
    """Get the current navigation state and zone of an AGV.

    Args:
        robot_id: AGV id, e.g. agv-01
    """
    print(f"  [도구 실행] get_nav_status({robot_id})")
    return {"robot_id": robot_id, "state": "IDLE", "zone": "A"}


chat = client.chats.create(
    model="gemini-3.5-flash",
    config=types.GenerateContentConfig(
        tools=[get_battery, get_nav_status],  # 함수를 그대로 넘김
        system_instruction=(
            "You are an AGV fleet assistant. A delivery to zone B requires "
            "at least 30% battery and the robot must be IDLE. Answer in Korean."
        ),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            maximum_remote_calls=5  # 무한 호출 방지
        ),
    ),
)

response = chat.send_message("agv-01이 지금 B구역 배송 나갈 수 있어?")
print(response.text)