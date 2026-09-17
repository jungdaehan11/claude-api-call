from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

# 스킬 = 파일에서 규칙 불러오기 (Claude는 업로드 후 ID로 참조)
skill = Path("agv-report-skill/SKILL.md").read_text(encoding="utf-8")

activity_log = """
09:02 agv-01 task#101 start A->B
09:10 agv-01 task#101 done 240m
09:15 agv-02 task#102 start A->C
09:18 agv-02 WARN planner failed, retrying
09:19 agv-02 replan ok
09:31 agv-02 task#102 done 410m
10:05 agv-03 ERROR localization lost near zone C
10:06 agv-03 E-STOP triggered
10:20 agv-03 manual recovery, task#103 failed
11:40 agv-01 battery 18%
"""

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",  # 한도 아끼기
    contents=f"다음 로그로 일일 보고서를 작성해줘:\n{activity_log}",
    config=types.GenerateContentConfig(system_instruction=skill),
)

print(response.text)