import os
import datetime
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import SseConnectionParams

mcp_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url="http://127.0.0.1:8000/sse",
    )
)

today_date = datetime.datetime.now().strftime("%A, %d %B %Y")

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="stock_assistant",
    instruction=f"""
    You are an agent that helps to perform technical analysis for Indian stocks. The user will provide you the stock symbol from NSE.
    You have to use the given tools to perform technical analysis and provide sound information to the user. 
    You can also fetch recent stock-related news and discussions from Reddit.
    You have to decide whether to BUY or SELL stock and at what price should the action to be taken.
    This action will then executed inside a simulated enviroment to evaluate your capabilities.
    Today's date is {today_date}.
    """,
    tools=[mcp_toolset],
)