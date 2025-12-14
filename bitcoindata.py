# -*- coding: utf-8 -*-

import os
import sys
import csv
import pandas as pd

import ccxt  # noqa: E402

def retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
   num_retries = 0
   try:
       num_retries += 1
       ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
       # print('Fetched', len(ohlcv), symbol, 'candles from', exchange.iso8601 (ohlcv[0][0]), 'to', exchange.iso8601 (ohlcv[-1][0]))
       return ohlcv
   except Exception as e:
     print(f'Error: {e}')
     if num_retries > max_retries:
       raise  # Exception('Failed to fetch', timeframe, symbol, 'OHLCV in', max_retries, 'attempts')


def scrape_ohlcv(exchange, max_retries, symbol, timeframe, limit):
   df = pd.read_csv("binance.csv")
   timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
   timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
   timedelta = limit * timeframe_duration_in_ms
   since = df.iloc[-1, 0] + timeframe_duration_in_ms
   now = exchange.milliseconds()
   all_ohlcv = []
   fetch_since = int(since)
   while fetch_since < now:
       ohlcv = retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, fetch_since, limit)
       fetch_since = (ohlcv[-1][0] + 1) if len(ohlcv) else (fetch_since + timedelta)
       all_ohlcv = all_ohlcv + ohlcv
       if len(all_ohlcv):
           print(len(all_ohlcv), 'candles in total from', exchange.iso8601(all_ohlcv[0][0]), 'to', exchange.iso8601(all_ohlcv[-1][0]))
       else:
           print(len(all_ohlcv), 'candles in total from', exchange.iso8601(fetch_since))
   return exchange.filter_by_since_limit(all_ohlcv, since, None, key=0)


def write_to_csv(filename, data):
   with open(filename, mode='a', newline='') as output_file:
       csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       csv_writer.writerows(data)


def scrape_candles_to_csv(filename, exchange_id, max_retries, symbol, timeframe, limit):
   # instantiate the exchange by id
   exchange = getattr(ccxt, exchange_id)()
   # preload all markets from the exchange
   exchange.load_markets()
   # fetch all candles
   ohlcv = scrape_ohlcv(exchange, max_retries, symbol, timeframe, limit)
   # save them to csv file
   write_to_csv(filename, ohlcv)
   if len(ohlcv) > 0:
    print('Saved', len(ohlcv), 'candles from', exchange.iso8601(ohlcv[0][0]), 'to', exchange.iso8601(ohlcv[-1][0]), 'to', filename)
   else:
    print('Spreadsheet is up to date')

# Binance's BTC/USDT candles start on 2017-08-17
scrape_candles_to_csv('binance.csv', 'binance', 3, 'BTC/USDT', '15m', 96)
