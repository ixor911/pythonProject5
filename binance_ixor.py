import numpy as nm
import numpy as np
from binance.spot import Spot
import pandas as pd

api_key = "4bRqCMlCkjxLoIfAT6NBwFHG15VtbmJ1WtI1JZgb0E3tfRasJjSPi12icZotddV5"
secret_key = "WYnoEo1mIhAQWqzpXSqAEXVeEXsVSv3iQc08yACFUAuCrh7vRGwgpYzwy50UHeCl"
spot = Spot(api_key, secret_key)


def get_init_df(coin):
    rough_candles = spot.klines(f"{coin}USDT", interval="5m", limit=1000)
    data = {
        'open': [],
        'max': [],
        'min': [],
        'close': []
    }

    for candle in rough_candles:
        data['open'].append(round(float(candle[1]), 2))
        data['max'].append(round(float(candle[2]), 2))
        data['min'].append(round(float(candle[3]), 2))
        data['close'].append(round(float(candle[4]), 2))

    df = pd.DataFrame(data=data)
    return df


def RSIcalc_strategy(df):
    df['MA200'] = df['close'].rolling(window=200).mean()
    df['price change'] = df['close'].pct_change()
    df['up move'] = df['price change'].apply(lambda x: x if x > 0 else 0)
    df['Down move'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)
    df['avg up'] = df['up move'].ewm(span=19).mean()
    df['avg down'] = df['Down move'].ewm(span=19).mean()
    df['RS'] = df['avg up'] / df['avg down']
    df['RSI'] = df['RS'].apply(lambda x: 100-(100/(x+1)))

    buy_list = []
    sell_list = []

    flag_buy = False
    j = 0
    for i in range(0, len(df)):
        if (df['close'][i] > df['MA200'][i]) & (df['RSI'][i] < 60) & (flag_buy == False):
            buy_list.append(True)
            sell_list.append(np.nan)
            flag_buy = True
            continue
        elif (df['close'][i] < df['MA200'][i]) & (df['RSI'][i] > 60) & (flag_buy == True):
            j = 0
            buy_list.append(np.nan)
            sell_list.append(True)
            flag_buy = False
            continue

        if flag_buy:
            if j < 10:
                j += 1
            elif j == 10:
                j = 0
                buy_list.append(np.nan)
                sell_list.append(True)
                flag_buy = False
                continue

        buy_list.append(np.nan)
        sell_list.append(np.nan)

    df['flag buy RSI'] = buy_list
    df['flag sell RSI'] = sell_list

    return df


def EMA3calc_strategy(df):
    df['EMA5'] = df.end.ewm(span=5, adjust=False).mean()
    df['EMA21'] = df.end.ewm(span=21, adjust=False).mean()
    df['EMA63'] = df.end.ewm(span=63, adjust=False).mean()
    buy_list = []
    sell_list = []
    flag_short = False
    flag_long = False

    for i in range(0, len(df)):
        short = df['EMA5'][i]
        middle = df['EMA21'][i]
        long = df['EMA63'][i]

        if (long * 0.95) > middle > (short * 1.05) and flag_short == False and flag_long == False:
            buy_list.append(True)
            sell_list.append(np.nan)
            flag_short = True
        elif flag_short and short > middle:
            buy_list.append(np.nan)
            sell_list.append(True)
            flag_short = False
        elif (long * 1.05) < middle < (short * 0.95) and flag_short == False and flag_long == False:
            buy_list.append(True)
            sell_list.append(np.nan)
            flag_long = True
        elif flag_long and short < middle:
            buy_list.append(np.nan)
            sell_list.append(True)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

    df['flag sell EMA3'] = sell_list
    df['flag buy EMA3'] = buy_list

    return df


def own_strategy(df):
    df['MA100'] = df['end'].rolling(window=100).mean()












    return df


