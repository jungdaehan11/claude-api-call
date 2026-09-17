import asyncio
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
client = genai.Client()
params = StdioServerParameters(command=sys.executable, args=["agv_mcp_server.py"])

SYSTEM = "You are an AGV fleet assistant. Use the tools. Answer in Korean."


async def main():
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. MCP 서버의 도구 목록 → Gemini 도구 형식으로 변환
            mcp_tools = await session.list_tools()
            declarations = [
                types.FunctionDeclaration(
                    name=t.name,
                    description=t.description,
                    parameters_json_schema=t.inputSchema,
                )
                for t in mcp_tools.tools
            ]
            print(f"[MCP] 도구 {len(declarations)}개 로드: {[d.name for d in declarations]}")

            config = types.GenerateContentConfig(
                system_instruction=SYSTEM,
                tools=[types.Tool(function_declarations=declarations)],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            )

            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part(text="agv-01을 충전소로 보내줘. 안 되면 이유를 설명해.")],
                )
            ]

            # 2. 에이전트 루프 (최대 5턴)
            for turn in range(1, 6):
                response = await client.aio.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=contents,
                    config=config,
                )

                if not response.function_calls:
                    print(f"\n[턴 {turn}] 최종 답변:\n{response.text}")
                    break

                contents.append(response.candidates[0].content)
                result_parts = []

                for call in response.function_calls:
                    args = dict(call.args or {})
                    # 3. 모델 대신 MCP 서버에 실행 요청
                    result = await session.call_tool(call.name, args)
                    text = "".join(c.text for c in result.content if hasattr(c, "text"))
                    print(f"[턴 {turn}] {call.name}({args}) -> {text}")

                    result_parts.append(
                        types.Part.from_function_response(
                            name=call.name, response={"result": text}
                        )
                    )

                contents.append(types.Content(role="user", parts=result_parts))
            else:
                print("최대 턴 수에 도달해 중단했습니다.")


asyncio.run(main())