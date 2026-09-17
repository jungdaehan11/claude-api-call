from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# 1. 에이전트 (모델 + 시스템 프롬프트 + 도구)
agent = client.beta.agents.create(
    name="Line Counter",
    model="claude-sonnet-5",  # 강의는 opus-5, 크레딧 아끼려고 sonnet으로
    system="You are a helpful agent that completes small file tasks.",
    tools=[
        {"type": "agent_toolset_20260401", "default_config": {"enabled": True}}
    ],
)
print(f"[에이전트] {agent.id}")

# 2. 환경 (실행 장소)
environment = client.beta.environments.create(
    name="line-counter-env",
    config={
        "type": "cloud",
        "networking": {"type": "unrestricted"},
    },
)
print(f"[환경] {environment.id}")

# 3. 세션 (한 번의 작업)
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Count lines demo",
)
print(f"[세션] {session.id}\n")

# 4. 스트림을 먼저 열고 → 시작 메시지 전송
with client.beta.sessions.events.stream(session_id=session.id) as stream:
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[
            {
                "type": "user.message",
                "content": [
                    {
                        "type": "text",
                        "text": "Create a file in the temp directory, "
                                "count its lines, and report back.",
                    }
                ],
            }
        ],
    )

    # 5. 이벤트 읽기
    for event in stream:
        if event.type == "agent.message":
            for block in event.content:
                if block.type == "text":
                    print(block.text, end="", flush=True)
        elif event.type == "agent.tool_use":
            print(f"\n[tool] {event.name}")
        elif event.type == "session.status_idle":
            print("\n--- Agent done ---")
            break