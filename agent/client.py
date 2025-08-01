import os
import asyncio
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import SseConnectionParams
import nest_asyncio

nest_asyncio.apply()

async def get_agent_async():
    """Creates an ADK Agent equipped with tools from the MCP Server."""
    mcp_toolset = MCPToolset(
        connection_params=SseConnectionParams(
            url="http://mcp:8000/sse",
        )
    )
    tools = await mcp_toolset.get_tools()
    print(f"Fetched {len(tools)} tools from MCP server.")
    
    root_agent = LlmAgent(
        model="gemini-1.5-flash",
        name="stock_assistant",
        instruction="""
        You are an agent that helps to perform technical analysis for Indian stocks. The user will provide you the stock symbol from NSE.
        You have to use the given tools to perform technical analysis and provide sound information to the user. 
        The user will decide whether to buy or sell the given stock based on this analysis
        """,
        tools=tools,
    )
    return root_agent

async def main():
    """Initializes the agent and runs the ADK web server."""
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("The GOOGLE_API_KEY environment variable is not set.")

    agent = await get_agent_async()
    
    runner = Runner(
        agent=agent,
        app_name="mcp_app",
        session_service=InMemorySessionService()
    )
    
    print("Starting ADK web server on http://0.0.0.0:8501")
    await runner.run_in_web(host="0.0.0.0", port=8501)

if __name__ == "__main__":
    asyncio.run(main())
