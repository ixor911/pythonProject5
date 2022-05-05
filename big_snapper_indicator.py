import numpy as nm
import numpy as np
from binance.spot import Spot
import pandas as pd


def getClosingPrices(dataframe, period):

    closing_prices = []
    for i in range(len(dataframe) - period, len(dataframe)):
        closing_prices.append(dataframe.close[i])
    return closing_prices


def calculate_sma(dataframe, period):

    df = pd.DataFrame(getClosingPrices(dataframe, period)).rolling(period).mean()
    return df[0][len(df) - 1]


def calculate_ema(dataframe, period):

    df = pd.DataFrame(getClosingPrices(dataframe, period)).ewm(period, adjust=False).mean()
    return df[0][len(df) - 1]


def calculate_hma(dataframe, period):

    df = pd.DataFrame(getClosingPrices(dataframe, period))
    df = df.rolling(period).apply(lambda x: ((np.arange(period)+1)*x).sum()/(np.arange(period)+1).sum(), raw=True)
    return df[0][len(df) - 1]










def indicator(dataframe):

    #  ===== INPUTS =====
    # coloured, fast, medium, slow
    hull_ma = calculate_hma(dataframe, 18)
    fast_ma = calculate_sma(dataframe, 21)
    medium_ma = calculate_sma(dataframe, 55)
    slow_ma = calculate_sma(dataframe, 89)







