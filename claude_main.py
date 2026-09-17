from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

buggy_code = """
def update_odom(v_left, v_right, wheel_base):
    v = (v_left + v_right) / 2
    w = (v_left - v_right) / wheel_base
    return v, w
"""

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system="You are a terse senior robotics code reviewer. Give feedback in one paragraph.",
    messages=[{"role": "user", "content": f"Review this code:\n{buggy_code}"}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)

print(f"\n[토큰] 입력: {response.usage.input_tokens}, 출력: {response.usage.output_tokens}")