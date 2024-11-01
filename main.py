
import pandas as pd
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import configparser

from functions import candle_data
from stockplot import simple_plot

config = configparser.ConfigParser()
config.read('../config/config_v20.ini')
accountID = config['oanda']['account_id']
access_token = config['oanda']['api_key']
client = oandapyV20.API(access_token=access_token)

parms={"granularity":"M5", "count":"40"}

df=candle_data(client,parms=parms)

# Run just one time
#from database_functions import create_database
#create_database(df)

#generate a simple plot    
#fig=simple_plot(df)
#fig.show()
#fig.write_image("test.png")


# abstract the chart by scaling everything to 1.00 = first price, then take 
# off the date axis

