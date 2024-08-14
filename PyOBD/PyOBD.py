import json
import requests
import urllib3
import numpy as np
import pandas as pd
from pytz import timezone
from typing import List, Dict

urllib3.disable_warnings()


class openBYMAdata:
    def __init__(self):
        self.__columns_filter = ["description", "symbol", "price", "variation", "highValue", "minValue", "previousClosingPrice"]
        self.__index_columns = ["description", "symbol", "last", "change", "high", "low", "previous_close"]

        self.__securities_columns = ['symbol', 'settlement', 'bid_size', 'bid', 'ask', 'ask_size', 'last', 'close', 'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'group']
        self.__filter_columns = ["symbol", "settlementType", "quantityBid", "bidPrice", "offerPrice", "quantityOffer", "settlementPrice", "closingPrice", "imbalance", "openingPrice", "tradingHighPrice", "tradingLowPrice", "previousClosingPrice", "volumeAmount", "volume", "numberOfOrders", "tradeHour", "securityType"]
        self.__numeric_columns = ['last', 'open', 'high', 'low', 'volume', 'turnover', 'operations', 'change', 'bid_size', 'bid', 'ask_size', 'ask', 'previous_close']

        self.__fixedIncome_columns = ['symbol', 'settlement', 'bid_size', 'bid', 'ask', 'ask_size', 'last', 'close', 'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'group', "expiration"]
        self.__filter_columns_fixedIncome = ["symbol", "settlementType", "quantityBid", "bidPrice", "offerPrice", "quantityOffer", "settlementPrice", "closingPrice", "imbalance", "openingPrice", "tradingHighPrice", "tradingLowPrice", "previousClosingPrice", "volumeAmount", "volume", "numberOfOrders", "tradeHour", "securityType", "maturityDate"]

        self.__s = requests.session()
        self.__s.get('https://open.bymadata.com.ar/#/dashboard', verify=False)
        self.__data='{"excludeZeroPxAndQty":false,"T2":false,"T1":true,"T0":false,"Content-Type":"application/json"}'


        self.__headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://open.bymadata.com.ar',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://open.bymadata.com.ar/',
            'Accept-Language': 'es-US,es-419;q=0.9,es;q=0.8,en;q=0.7',
        }
        response = self.__s.get('https://open.bymadata.com.ar/assets/api/langs/es.json', headers=self.__headers, verify=False)
        self.__diction = response.json()

    def isworkingDay(self) -> bool:
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/market-time', headers=self.__headers, verify=False)
        return response.json().get("isWorkingDay", False)

    def indices(self) -> pd.DataFrame:
        data='{"Content-Type":"application/json"}'
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/index-price', headers=self.__headers, data=data, verify=False)
        print(response.json())
        df = pd.DataFrame(response.json().get('data', []))
        df = df[self.__columns_filter].copy()
        df.columns = self.__index_columns
        return df

    def get_bluechips(self) -> pd.DataFrame:
        return self.__get_securities('leading-equity')

    def get_galpones(self) -> pd.DataFrame:
        return self.__get_securities('general-equity')

    def get_cedears(self) -> pd.DataFrame:
        return self.__get_securities('cedears')

    def get_options(self) -> pd.DataFrame:
        data='{"Content-Type":"application/json"}'
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/options', headers=self.__headers, data=data, verify=False)
        df = pd.DataFrame(response.json())
        df = df[[
            "symbol", "quantityBid", "bidPrice", "offerPrice", "quantityOffer", "settlementPrice",
            "closingPrice", "imbalance", "openingPrice", "tradingHighPrice", "tradingLowPrice",
            "previousClosingPrice", "volumeAmount", "volume", "numberOfOrders", "tradeHour",
            "underlyingSymbol", "maturityDate"
        ]].copy()
        df.columns = [
            'symbol', 'bid_size', 'bid', 'ask', 'ask_size', 'last', 'close', 'change', 'open', 'high', 
            'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'underlying_asset', 
            'expiration'
        ]
        df['expiration'] = pd.to_datetime(df['expiration'])
        return df

    def get_bonds(self) -> pd.DataFrame:
        return self.__get_fixed_income('public-bonds')

    def get_short_term_bonds(self) -> pd.DataFrame:
        df = self.__get_fixed_income('lebacs')
        df['currency'] = df['denominationCcy']
        return df

    def get_corporateBonds(self) -> pd.DataFrame:
        return self.__get_fixed_income('negociable-obligations')
    
    def get_futures(self) -> pd.DataFrame:
        data = '{"page_number":1,"excludeZeroPxAndQty":true,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response =  self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/index-future', headers=self.__headers, data=data, verify=False)
        panel_futuros = json.loads(response.text)
        df = pd.DataFrame(panel_futuros['data'])

        filter_columns=["symbol","quantityBid","bidPrice","offerPrice","quantityOffer","settlementPrice","closingPrice","imbalance","openingPrice","tradingHighPrice","tradingLowPrice","previousClosingPrice","volumeAmount","volume","numberOfOrders","tradeHour","maturityDate","openInterest"]
        options_columns = ['symbol', 'bid_size', 'bid', 'ask', 'ask_size', 'last', 'close' , 'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'expiration','openInterest']
        df = df[filter_columns].copy()

        df.columns = options_columns
        df.expiration=pd.to_datetime(df.expiration)
        row100=['last','close','open','high','low','previous_close','turnover','volume']
    

        for i in range(len(row100)):
            df[row100[i]]=df[row100[i]]*1000
        return df
    
    def marketResume(self) -> pd.DataFrame:
        data='{"Content-Type":"application/json"}'
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/total-negotiated', headers=self.__headers, data=data, verify=False)
        df = pd.DataFrame(response.json().get('data', []))
        df['symbol'] = df['symbol'].replace(self.__diction, regex=True)
        #df['assetType'] = df['assetType'].replace(self.__diction, regex=True)
        #df['parentKey'] = df['parentKey'].replace(self.__diction, regex=True)
        return df.drop(['market','settlementType'],axis=1)

    def byma_news(self) -> pd.DataFrame:
        data='{"Content-Type":"application/json"}'
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/bnown/byma-ads', headers=self.__headers, data=data, verify=False)
        df = pd.DataFrame(response.json().get('data', []))
        df['descarga'] = 'https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/sba/download/' + df['descarga'].astype(str)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df.drop(["tipoArchivo"], axis=1, inplace=True)
        return df

    def income_statement(self, ticker) -> pd.DataFrame:
        data = json.dumps({"symbol": ticker, "Content-Type": "application/json"})
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/bnown/seriesHistoricas/balances', headers=self.__headers, data=data, verify=False)
        df = pd.DataFrame(response.json().get('data', []))
        df['balancesArchivo'] = 'https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/sba/download/' + df['balancesArchivo'].astype(str)
        #df['fecha'] = pd.to_datetime(df['fecha'])
        return df

    def __get_securities(self, endpoint: str) -> pd.DataFrame:

        response = self.__s.post(f'https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/{endpoint}',data=self.__data, headers=self.__headers, verify=False)
        df = pd.DataFrame(response.json().get('data', []))
        df = df[self.__filter_columns].copy()
        df.columns = self.__securities_columns
        df['datetime'] = pd.to_datetime(df['datetime'])
        df[self.__numeric_columns] = df[self.__numeric_columns].apply(pd.to_numeric, errors='coerce')
        return df

    def __get_fixed_income(self, endpoint: str) -> pd.DataFrame:
        response = self.__s.post(f'https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/{endpoint}', data=self.__data, headers=self.__headers, verify=False)
        df = pd.DataFrame(response.json())
        df = df[self.__filter_columns_fixedIncome].copy()
        df.columns = self.__fixedIncome_columns
        df['expiration'] = pd.to_datetime(df['expiration'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df[self.__numeric_columns] = df[self.__numeric_columns].apply(pd.to_numeric, errors='coerce')
        return df
