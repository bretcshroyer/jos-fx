import pandas as pd
import oandapyV20
import oandapyV20.endpoints.instruments as instruments


def candle_data(client,instrument="EUR_USD",parms={}):
    #default instrument, all else passed in via parms dict

    #other parms:
    #   granularity  e.g. "M5"
    #   from, to     e.g. 2023-01-01T15%3A00%3A00.000000000Z
    #   count        default = 500 candles, maximum = 5000
    r=instruments.InstrumentsCandles(instrument,params=parms)
    granularity=parms['granularity']
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

    df=pd.DataFrame.from_dict(cd,orient='index',columns=['time','instrument','granularity','volume','o','h','l','c']).reset_index()
    df=df.drop(columns=['index'])        
    return df

def big_candle_data(client,size,instrument="EUR_USD",parms={}):
    #a high-level wrapper to successively call to API in bite-sized chunks to build the full dataset
    
    chunksize=250  #by default, OANDA has chunksize (count) max at 500

    #1. pull the most recent chunk with count == chunksize
    parms["count"]=chunksize
    df=candle_data(client=client,parms=parms)
    result=df.copy()   
    print(len(result))
    #2. if we don't have enough then repeat with another chunk
    
    while (len(result)<size):  
        f=df['time'][0]
        parms['to']=f
        df=candle_data(client=client,parms=parms)
        result=pd.concat([result,df],ignore_index=True)
        print(len(result))
    #3. limit final set to desired count size
    #sort
    result=result.sort_values(by=["time"])
    return(result.tail(size))


if __name__=="__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read('../config/config_v20.ini')
    accountID = config['oanda']['account_id']
    access_token = config['oanda']['api_key']
    client = oandapyV20.API(access_token=access_token)

    #vignette="test two pulls"
    vignette="test large pull"

    match vignette:
        case "test two pulls":
            parms={"count":"10","granularity":"M1"}
            df=candle_data(client=client,parms=parms)
            print(df)

            f=df['time'][0]

            parms['to']=f
            df=candle_data(client=client,parms=parms)
            print(df)
        case "test large pull":
            parms={"granularity":"M1"}
            df=big_candle_data(client=client,size=2000,parms=parms)
            print(df)
            print(len(df))
