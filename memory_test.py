import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

params = StdioServerParameters(command=sys.executable, args=["agv_mcp_server.py"])


async def main():
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            r = await session.call_tool("save_note", {
                "robot_id": "agv-03",
                "note": "zone C 부근에서 위치 추정 상실 후 E-STOP 발생 (유리벽 반사 의심)",
            })
            print("[저장]", r.content[0].text)

            r = await session.call_tool("read_notes", {"robot_id": "agv-03"})
            print("[조회]", r.content[0].text)


asyncio.run(main())