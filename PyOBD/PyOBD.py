import requests
import json
import urllib3
urllib3.disable_warnings()
import pandas as pd
from pytz import timezone
from datetime import datetime
import datetime
import numpy as np





class openBYMAdata():

    def __init__(self):
        self.__columns_filter=["description","symbol","price","variation","highValue","minValue","previousClosingPrice"]
        self.__index_columns=["description","symbol","last","change","high","low","previous_close"]

        self.__securities_columns = ['symbol', 'settlement', 'bid_size', 'bid', 'ask', 'ask_size', 'last', 'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'group']
        self.__filter_columns=["symbol","settlementType","quantityBid","bidPrice","offerPrice","quantityOffer","settlementPrice","imbalance","openingPrice","tradingHighPrice","tradingLowPrice","previousClosingPrice","volumeAmount","volume","numberOfOrders","tradeHour","securityType"]
        self.__numeric_columns = ['last', 'open', 'high', 'low', 'volume', 'turnover', 'operations', 'change', 'bid_size', 'bid', 'ask_size', 'ask', 'previous_close']

        self.__fixedIncome_columns = ['symbol', 'settlement', 'bid_size', 'bid', 'ask', 'ask_size', 'last', 'change', 'open', 'high', 'low', 'previous_close', 'turnover', 'volume', 'operations', 'datetime', 'group',"expiration"]
        self.__filter_columns_fixedIncome=["symbol","settlementType","quantityBid","bidPrice","offerPrice","quantityOffer","settlementPrice","imbalance","openingPrice","tradingHighPrice","tradingLowPrice","previousClosingPrice","volumeAmount","volume","numberOfOrders","tradeHour","securityType","maturityDate"]

        self.__settlements_map = {
        '1': 'spot',
        '2': '24hs',
        '3': '48hs'}

        self.__s = requests.session()
        self.__s.get('https://open.bymadata.com.ar/#/dashboard', verify=False)

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
        response = self.__s.get('https://open.bymadata.com.ar/assets/api/langs/es.json', headers=self.__headers)
        self.__diction=json.loads(response.text)

    def isworkingDay(self):
        data = '{}'
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/market-time', headers=self.__headers, data=data)
        loaded= json.loads(response.content)
        return bool(loaded["isWorkingDay"])

    def indices(self):
        data = '{"Content-Type":"application/json"}'
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/index-price', headers=self.__headers, data=data, verify=False)
        indices = json.loads(response.text)['data']
        df = pd.DataFrame(indices)
        df = df[self.__columns_filter].copy()
        df.columns = self.__index_columns
        return df

    def get_bluchips(self):
        data = '{"excludeZeroPxAndQty":false,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/leading-equity', headers=self.__headers, data=data)
        panel_acciones_lideres = json.loads(response.text)
        df= pd.DataFrame(panel_acciones_lideres['data'])
        df = df[self.__filter_columns].copy()
        df.columns = self.__securities_columns
        df.settlement = df.settlement.apply(lambda x: self.__settlements_map[x] if x in self.__settlements_map else '')
        df = self.__convert_to_numeric_columns(df, self.__numeric_columns)
        return df

    def get_galpones(self):
        data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/general-equity', headers=self.__headers, data=data)
        panel_acciones_general = json.loads(response.text)
        df= pd.DataFrame(panel_acciones_general['data'])
        df = df[self.__filter_columns].copy()
        df.columns = self.__securities_columns
        df.settlement = df.settlement.apply(lambda x: self.__settlements_map[x] if x in self.__settlements_map else '')
        df = self.__convert_to_numeric_columns(df, self.__numeric_columns)
        return df


    def get_bonds(self):
        data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/public-bonds', headers=self.__headers, data=data)
        panel_letras = json.loads(response.text)
        df = pd.DataFrame(panel_letras['data'])
        df = df[self.__filter_columns_fixedIncome].copy()
        df.columns = self.__fixedIncome_columns
        df.settlement = df.settlement.apply(lambda x: self.__settlements_map[x] if x in self.__settlements_map else '')
        df.expiration=pd.to_datetime(df.expiration)
        df = self.__convert_to_numeric_columns(df, self.__numeric_columns)
        return df

    def get_corporateBonds(self):
        data = '{"excludeZeroPxAndQty":true,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/negociable-obligations', headers=self.__headers, data=data)
        panel_ons = json.loads(response.text)
        df= pd.DataFrame(panel_ons)
        df = df[self.__filter_columns_fixedIncome].copy()
        df.columns = self.__fixedIncome_columns
        df.settlement = df.settlement.apply(lambda x: self.__settlements_map[x] if x in self.__settlements_map else '')
        df.expiration=pd.to_datetime(df.expiration)
        df = self.__convert_to_numeric_columns(df, self.__numeric_columns)
        return df

    def marketResume(self):
        data = '{"Content-Type":"application/json"}'
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/total-negotiated', headers=self.__headers, data=data)
        totales_negociados = json.loads(response.text)
        df_totales = pd.DataFrame(totales_negociados)
        df_totales['symbol'] = df_totales['symbol'].replace(self.__diction, regex=True)
        df_totales['assetType'] = df_totales['assetType'].replace(self.__diction, regex=True)
        df_totales['parentKey'] = df_totales['parentKey'].replace(self.__diction, regex=True)
        return df_totales

    def byma_news(self):
        data = '{"filter":true,"fromDate":null,"toDate":null,"Content-Type":"application/json"}' ## Parametros de los filtros.
        response = self.__s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/bnown/byma-ads', headers=self.__headers, data=data)
        avisos_byma = json.loads(response.text)
        df = pd.DataFrame(avisos_byma['data'])
        df.descarga='https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/sba/download/'+df.descarga.astype(str)
        df.fecha=pd.to_datetime(df.fecha)
        df.drop(["tipoArchivo"],axis=1,inplace=True)
        return df



    def __convert_to_numeric_columns(self,df, columns):
        for col in columns:
            #df[col] = df[col].apply(lambda x: x.replace('.', '').replace(',','.') if isinstance(x, str) else x)
            df[col] = pd.to_numeric(df[col].apply(lambda x: np.nan if x == '-' else x))
        return df
