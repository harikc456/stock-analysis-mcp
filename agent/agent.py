import datetime
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import SseConnectionParams
from google.adk.tools.tool_context import ToolContext


# --- State Keys ---
STATE_TA = "technical_analysis"
STATE_EVAL = "evaluation"
COMPLETION_PHRASE = "STOP EXECUTION"


def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling
    the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {}


mcp_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url="http://127.0.0.1:8000/sse",
    )
)

today_date = datetime.datetime.now().strftime("%A, %d %B %Y")

ta_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="stock_ta_assistant",
    instruction=f"""
    You are an agent that helps to perform technical analysis for Indian stocks. The user will provide you the stock symbol from NSE.
    You have to use the given tools to perform technical analysis and provide sound information to the user. 
    You can also fetch recent stock-related news and discussions from Reddit.
    You have to decide whether to BUY or SELL stock and at what price should the action to be taken.
    This action will then executed inside a simulated enviroment to evaluate your capabilities.
    Today's date is {today_date}.
    """,
    tools=[mcp_toolset],
    output_key=STATE_TA,
)

eval_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="eval_agent",
    instruction="""
    You are an agent that evaluates the analysis performed on stock by another agent, if the analysis is sufficient and the accurate, 
    then You MUST call the 'exit_loop' function. Do not output any text. Else (the critique contains actionable feedback)
    Carefully apply the suggestions.
    """,
    tools=[exit_loop],
)

root_agent = LoopAgent(name="OrchestratorAgent", sub_agents=[ta_agent, eval_agent], max_iterations=5)
