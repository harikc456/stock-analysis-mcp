import os
import requests
import pandas as pd
from ta.trend import (
    macd,
    ema_indicator,
    ichimoku_a,
    ichimoku_b,
    adx,
    psar_up,
    psar_down,
    aroon_up,
    aroon_down,
)
from ta.momentum import tsi, rsi, stoch, stoch_signal, roc
from ta.volume import (
    on_balance_volume,
    chaikin_money_flow,
    volume_weighted_average_price,
)

from constants import NSE_HOST_URL, HISTORICAL_ENDPOINT, METADATA_ENDPOINT, DUMP_DIR


def get_data(symbol, start_date, end_date):
    files = os.listdir(DUMP_DIR)
    file_name = f"{symbol}_{start_date}_{end_date}.csv"
    if file_name in files:
        file_path = os.path.join(DUMP_DIR, file_name)
        df = pd.read_csv(file_path)
    else:
        df = get_historical_data(symbol, start_date, end_date)
    return df


def get_equity_metadata(symbol: str) -> dict:
    response = requests.get(NSE_HOST_URL + METADATA_ENDPOINT.format(symbol=symbol))
    print(response.json()["metadata"])
    return response.json()["metadata"]


def get_historical_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    response = requests.get(
        NSE_HOST_URL + HISTORICAL_ENDPOINT.format(symbol=symbol),
        params={"dateStart": start_date, "dateEnd": end_date},
    )
    merged_data = []
    for data in response.json():
        merged_data.extend(data["data"])

    df = pd.DataFrame(merged_data)
    file_name = f"{symbol}_{start_date}_{end_date}.csv"
    file_path = os.path.join(DUMP_DIR, file_name)
    df.to_csv(file_path, index=False)
    return merged_data


def get_macd(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return macd(df.CH_CLOSING_PRICE, fillna=True).tolist()


def get_rsi(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return rsi(df.CH_CLOSING_PRICE, fillna=True).tolist()


def get_tsi(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return tsi(df.CH_CLOSING_PRICE, fillna=True).tolist()


def get_stoch(
    symbol: str, start_date: str, end_date: str, window: int, smooth_window: int
) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return stoch(
        df.CH_TRADE_HIGH_PRICE,
        df.CH_TRADE_LOW_PRICE,
        df.CH_CLOSING_PRICE,
        window,
        smooth_window,
        fillna=True,
    ).tolist()


def get_roc(symbol: str, start_date: str, end_date: str, window: int) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return roc(df.CH_CLOSING_PRICE, window, fillna=True).tolist()


def get_ema(symbol: str, start_date: str, end_date: str, window: int) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return ema_indicator(df.CH_CLOSING_PRICE, window, fillna=True).tolist()


def get_ichimoku_a(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return ichimoku_a(
        df.CH_TRADE_HIGH_PRICE, df.CH_TRADE_LOW_PRICE, fillna=True
    ).tolist()


def get_ichimoku_b(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return ichimoku_b(
        df.CH_TRADE_HIGH_PRICE, df.CH_TRADE_LOW_PRICE, fillna=True
    ).tolist()


def get_adx(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return adx(
        df.CH_TRADE_HIGH_PRICE, df.CH_TRADE_LOW_PRICE, df.CH_CLOSING_PRICE, fillna=True
    ).tolist()


def get_psar_up(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return psar_up(
        df.CH_TRADE_HIGH_PRICE, df.CH_TRADE_LOW_PRICE, df.CH_CLOSING_PRICE, fillna=True
    ).tolist()


def get_psar_down(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return psar_down(
        df.CH_TRADE_HIGH_PRICE, df.CH_TRADE_LOW_PRICE, df.CH_CLOSING_PRICE, fillna=True
    ).tolist()


def get_aroon_up(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return aroon_up(
        df.CH_TRADE_HIGH_PRICE, df.CH_TRADE_LOW_PRICE, df.CH_CLOSING_PRICE, fillna=True
    ).tolist()


def get_aroon_down(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return aroon_down(
        df.CH_TRADE_HIGH_PRICE, df.CH_TRADE_LOW_PRICE, df.CH_CLOSING_PRICE, fillna=True
    ).tolist()


# Volume based metrics - On-Balance Volume (OBV), Chaikin Money Flow (CMF), Volume Weighted Average Price (VWAP)


def get_on_balance_volume(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return on_balance_volume(
        df.CH_CLOSING_PRICE, df.CH_TOT_TRADED_QTY, fillna=True
    ).tolist()


def get_chaikin_money_flow(symbol: str, start_date: str, end_date: str) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return chaikin_money_flow(
        df.CH_TRADE_HIGH_PRICE,
        df.CH_TRADE_LOW_PRICE,
        df.CH_CLOSING_PRICE,
        df.CH_TOT_TRADED_QTY,
        fillna=True,
    ).tolist()


def get_volume_weighted_average_price(
    symbol: str, start_date: str, end_date: str
) -> list[float]:
    df = get_data(symbol, start_date, end_date)
    return volume_weighted_average_price(
        df.CH_TRADE_HIGH_PRICE,
        df.CH_TRADE_LOW_PRICE,
        df.CH_CLOSING_PRICE,
        df.CH_TOT_TRADED_QTY,
        fillna=True,
    ).tolist()
