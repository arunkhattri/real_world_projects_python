#!/usr/bin/env python3
import pandas as pd
import numpy as np
import pandas_datareader as pdr
from time import sleep


# quotes for akk stocks
def get_quotes(tickers):
    """
    Parameters
    ----------
    tickers: list, list of tickers

    Returns
    -------
    dict, ticker: quote_price
    """
    data_dict = dict()
    for _, t in enumerate(tickers):
        data_dict[t] = pdr.get_quote_yahoo(t)["price"][0]
        sleep(1)
    print("Refreshed...")
    return data_dict


def akk_stock_status(data, stock_df):
    """
    Parameters
    ----------
    data: dict, ticker: quote_price
    stock_df: dataframe, contains symbol, qty, avg cost price

    Returns
    -------
    dataframe

    """
    curr_price = pd.DataFrame.from_records(np.array(list(data.items())))
    curr_price.columns = ["ticker", "quote"]

    merged_stocks = stock_df.merge(curr_price, left_on="yahoo", right_on="ticker")
    merged_stocks.drop(["Company Name", "ticker"], axis=1, inplace=True)
    merged_stocks["quote"] = merged_stocks["quote"].astype(float)
    merged_stocks["up_down"] = (
        merged_stocks["quote"] - merged_stocks["Average Cost Price"]
    )
    merged_stocks["profit_loss"] = merged_stocks["Qty"] * merged_stocks["up_down"]

    return merged_stocks


if __name__ == "__main__":
    stocks = pd.read_csv("akk_stocks.csv")
    tickers = stocks["yahoo"].tolist()
    data = get_quotes(tickers)
    df = akk_stock_status(data, stocks)
    print(df)
    print(f"Total Profit/Loss: ₹{round(df['profit_loss'].sum(), 2)}")
