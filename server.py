from fastmcp import FastMCP

from utils import get_historical_data, get_equity_metadata, get_macd, get_rsi, get_tsi

# Create a server instance
mcp = FastMCP(name="NSE stock Analysis Server")


@mcp.tool
def get_stock_metadata_tool(symbol: str) -> list[float]:
    """
    Gets general information about the stock like PE ratio, sector etc

    Params:
    symbol: Upper case symbol of the stock
    """
    return get_equity_metadata(symbol)

@mcp.tool
def get_equity_data(symbol: str, start_date: str, end_date: str) -> list[dict]:
    """
    Gets the historical data for the given stock based on the dates provided

    Params:
    symbol: Upper case symbol of the stock
    start_date: the start date of the range, should be in YYYY-MM-DD
    end_date: the end date of the range, should be in YYYY-MM-DD
    """
    return get_historical_data(symbol, start_date, end_date)

@mcp.tool
def get_macd_tool(symbol: str, start_date: str, end_date: str) -> list[float]:
    """
    Gets the macd numbers for the given symbol

    Params:
    symbol: Upper case symbol of the stock
    start_date: the start date of the range, should be in YYYY-MM-DD
    end_date: the end date of the range, should be in YYYY-MM-DD
    """
    return get_macd(symbol, start_date, end_date)


@mcp.tool
def get_rsi_tool(symbol: str, start_date: str, end_date: str) -> list[float]:
    """
    Gets the rsi for the given symbol

    Params:
    symbol: Upper case symbol of the stock
    start_date: the start date of the range, should be in YYYY-MM-DD
    end_date: the end date of the range, should be in YYYY-MM-DD
    """
    return get_rsi(symbol, start_date, end_date)


@mcp.tool
def get_tsi_tool(symbol: str, start_date: str, end_date: str) -> list[float]:
    """
    Gets the tsi for the given symbol

    Params:
    symbol: Upper case symbol of the stock
    start_date: the start date of the range, should be in YYYY-MM-DD
    end_date: the end date of the range, should be in YYYY-MM-DD
    """
    return get_tsi(symbol, start_date, end_date)

@mcp.tool
def perform_calculation(equation :str) -> float:
    """
    Computes the solution of the equation given,
    
    Params:
    equation: a mathematical equation without any variables
    """

    return eval(equation)

if __name__ == "__main__":
    # mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
    mcp.run(transport="sse", host="0.0.0.0", port=8000)