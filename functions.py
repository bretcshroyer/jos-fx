import pandas as pd
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import configparser

config = configparser.ConfigParser()
config.read('../config/config_v20.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']

client = oandapyV20.API(access_token=access_token)

def candle_data(client,instrument="EUR_USD",granularity="M5",parms={}):
    parms['granularity']=granularity
    print(parms)
    #other parms:
    #   from, to  2023-01-01T15%3A00%3A00.000000000Z
    #   count  default = 500 candles, maximum = 5000
    r=instruments.InstrumentsCandles(instrument,params=parms)
    client.request(r)

    cd={}
    for candle in r.response['candles']:
        if candle['complete']==True:
            volume=candle['volume']
            time=candle['time']
            o=candle['mid']['o']
            h=candle['mid']['h']
            l=candle['mid']['l']
            c=candle['mid']['c']
            cd[time]=[time,instrument,granularity,volume,o,h,l,c]
            print(time)
            print(type(time))
    df=pd.DataFrame.from_dict(cd,orient='index',columns=['time','instrument','granularity','volume','o','h','l','c']).reset_index()
    df=df.drop(columns=['index'])        
    return df

parms={"count":"4"}
d=candle_data(client,parms=parms)
print(d)