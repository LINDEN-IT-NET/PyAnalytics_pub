import MetaTrader5 as mt5
import pandas as pd
import pytz
from datetime import datetime

pd.set_option('display.max_rows', None)
pd.options.display.width = None

# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

account = 1805266 # fxflat daytrading 118
authorized = mt5.login(account, password="Z3r#<#4Lr#?Qd4", server="FXFlatMT5-LiveServer")
if authorized:
    account_info_dict = mt5.account_info()._asdict()
    for prop in account_info_dict:
        print("   {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))


# get the number of deals in history
from_date=datetime(2023,3,28)
to_date=datetime(2023,3,29)
#to_date=datetime.now()


# get deals for symbols whose names contain "USTEC" within a specified interval
#deals=mt5.history_deals_get(from_date, to_date, group="USTEC")
#if deals==None:
#    print("No deals with group=\"USTEC\", error code={}".format(mt5.last_error()))
#elif len(deals)> 0:
#    print("history_deals_get({}, {}, group=\"*USTEC*\")={}".format(from_date,to_date,len(deals)))


# get deals for symbols whose names contain neither "EUR" nor "GBP"
deals = mt5.history_deals_get(from_date, to_date, group="*,!*EUR*")
if deals == None:
    print("No deals, error code={}".format(mt5.last_error()))
elif len(deals) > 0:
    print("history_deals_get(from_date, to_date, group=\"*,!*EUR*,\") =", len(deals))
    # display all obtained deals 'as is'
    for deal in deals:
        print("  ",deal)
    print()
    # display these deals as a table using pandas.DataFrame
    df=pd.DataFrame(list(deals),columns=deals[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit='s')
    print(df)
print("")


# calc point: if win: profit * vol * digits; bsp: 0,5 * 0,1 * 100 = 5P (5P * 10ct = 50ct)
df_points = pd.DataFrame(columns=('time','symbol','volume','price','profit','points'))
for pos, d in df.iterrows():
    points = d.profit * d.volume * 100
    df_points.loc[pos] = [d.time,d.symbol,d.volume,d.price,d.profit,points]

print(df_points)
print("")

df_points = df_points.astype({"points": float})
df_points['cumulative_points'] = df_points['points'].cumsum().round(2)
df_points = df_points.astype({"cumulative_points": float})
print(df_points)

print("")

mt5.shutdown()
