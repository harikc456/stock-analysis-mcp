import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import SseConnectionParams

os.environ["GOOGLE_API_KEY"] = "AIzaSyDWRE42ozhuAfSIAt92pccu3GgDDkILCfU"

mcp_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url="http://127.0.0.1:8000/sse",
    )
)
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="stock_assistant",
    instruction="""
    You are an agent that helps to perform technical analysis for Indian stocks. The user will provide you the stock symbol from NSE.
    You have to use the given tools to perform technical analysis and provide sound information to the user. 
    You have to decide whether to BUY or SELL stock and at what price should the action to be taken.
    This action will then executed inside a simulated enviroment to evaluate your capabilities.
    """,
    tools=[mcp_toolset],
)