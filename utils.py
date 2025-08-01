import os
import requests
import pandas as pd
from ta.trend import macd
from ta.momentum import tsi, rsi

from constants import NSE_HOST_URL, HISTORICAL_ENDPOINT, METADATA_ENDPOINT, DUMP_DIR

def get_equity_metadata(symbol: str) -> dict:
	response = requests.get(NSE_HOST_URL + METADATA_ENDPOINT.format(symbol=symbol))
	print(response.json()["metadata"])
	return response.json()["metadata"]

def get_historical_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
	response = requests.get(
	    NSE_HOST_URL + HISTORICAL_ENDPOINT.format(symbol=symbol), 
	    params={
	        "dateStart": start_date,
	        "dateEnd": end_date
	    }
	)
	merged_data = []
	for data in response.json():
		merged_data.extend(data['data'])

	df = pd.DataFrame(merged_data)
	file_name = f"{symbol}_{start_date}_{end_date}.csv"
	file_path = os.path.join(DUMP_DIR, file_name)
	df.to_csv(file_path, index=False)

	print(merged_data)
    
	return merged_data

def get_macd(symbol: str, start_date: str, end_date: str) -> list[float]:
	files = os.listdir(DUMP_DIR)
	file_name = f"{symbol}_{start_date}_{end_date}.csv"
	if file_name in files:
		file_path = os.path.join(DUMP_DIR, file_name)
		df = pd.read_csv(file_path)
	else:
		df = get_historical_data(symbol, start_date, end_date)	
	return macd(df.CH_CLOSING_PRICE, fillna=True).tolist()

def get_rsi(symbol: str, start_date: str, end_date: str) -> list[float]:
	files = os.listdir(DUMP_DIR)
	file_name = f"{symbol}_{start_date}_{end_date}.csv"
	if file_name in files:
		file_path = os.path.join(DUMP_DIR, file_name)
		df = pd.read_csv(file_path)
	else:
		df = get_historical_data(symbol, start_date, end_date)	
	return rsi(df.CH_CLOSING_PRICE, fillna=True).tolist()

def get_tsi(symbol: str, start_date: str, end_date: str) -> list[float]:
	files = os.listdir(DUMP_DIR)
	file_name = f"{symbol}_{start_date}_{end_date}.csv"
	if file_name in files:
		file_path = os.path.join(DUMP_DIR, file_name)
		df = pd.read_csv(file_path)
	else:
		df = get_historical_data(symbol, start_date, end_date)	
	return tsi(df.CH_CLOSING_PRICE, fillna=True).tolist()