
import pandas as pd
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import configparser
import plotly.graph_objects as go

config = configparser.ConfigParser()
config.read('../config/config_v20.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']

client = oandapyV20.API(access_token=access_token)


parms={"granularity":"M5"}
#other parms:
#   from, to  2023-01-01T15%3A00%3A00.000000000Z
#default = 500 candles, maximum = 5000
r=instruments.InstrumentsCandles(instrument="EUR_USD",params=parms)
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
        cd[time]=[time,volume,o,h,l,c]
df=pd.DataFrame.from_dict(cd,orient='index',columns=['Date','volume','o','h','l','c'])        

fig=go.Figure(data=go.Ohlc(x=df['Date'],
                open=df['o'],
                high=df['h'],
                low=df['l'],
                close=df['c']))
fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()

# abstract the chart by scaling everything to 1.00 = first price, then take 
# off the date axis

