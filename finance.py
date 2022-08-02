from yfapi import YahooFinanceAPI
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import csv


sector_tickers = {'AMZN' : 'face',}
api = YahooFinanceAPI()
price_column = "Close"
date_column = "Date"
sp_data = api.get_ticker_data("spy", datetime.datetime(2022, 1, 1), datetime.datetime(2022, 7, 6))
normal_sp_close = (sp_data[price_column] - sp_data[price_column].min())/ \
                  (sp_data[price_column].max() - sp_data[price_column].min())
for key in sector_tickers:

    ticker, desc = key, sector_tickers[key]
    comp_data = api.get_ticker_data(ticker, datetime.datetime(2022, 1, 1), datetime.datetime(2022, 7, 6))
    normal_comp_data = (comp_data[price_column] - comp_data[price_column].min()) / \
                       (comp_data[price_column].max() - comp_data[price_column].min())
    divergence = normal_comp_data - normal_sp_close
    div, = plt.plot(comp_data[date_column], divergence, label="Divergence")

    sp, = plt.plot(sp_data[date_column], normal_sp_close, label="SPY - S&P 500")
    comp, = plt.plot(comp_data[date_column], normal_comp_data, label="{} - {}".format(ticker, desc))
    plt.legend(handles=[div, sp, comp])
    plt.axhline(0, color="black")
    plt.savefig("{}.png".format(ticker))
    plt.clf()






# ticker -> description dict (place new tickers here)
sector_tickers = {'Meta' : 'face'}
reader = csv.DictReader(open('IWM_holdings.csv'))
row_count = 0




# just in case these change
price_column = "Close"
date_column = "Date"

api = YahooFinanceAPI()
sp_data = api.get_ticker_data("spy", datetime.datetime(2022, 1, 1), datetime.datetime(2022, 7, 6))
normal_sp_close = (sp_data[price_column] - sp_data[price_column].min())/ \
                  (sp_data[price_column].max() - sp_data[price_column].min())

for key in sector_tickers:
    ticker, desc = key, sector_tickers[key]
    try:
        comp_data = api.get_ticker_data(ticker, datetime.datetime(2022, 1, 1), datetime.datetime(2022, 7, 6))
    except:
        pass
    normal_comp_data = (comp_data[price_column] - comp_data[price_column].min())/ \
                       (comp_data[price_column].max() - comp_data[price_column].min())
    divergence = normal_comp_data - normal_sp_close
    if sum(divergence)/len(divergence) < -0.5:

        #print(key)
        #print(comp_data)
        #print(normal_comp_data)

        ## Divergence = 0 -> no divergence between S&P and Sector (or stock)
        ## Divergence < 0 -> sector gains less than S&P gains (sector may be undervalued)
        ## Divergence > 0 -> sector gains greater than S&P gains (sector may be overvalued)
        try:
            div, = plt.plot(comp_data[date_column], divergence, label="Divergence")
        except:
            pass
        sp, = plt.plot(sp_data[date_column], normal_sp_close, label="SPY - S&P 500")
        comp, = plt.plot(comp_data[date_column], normal_comp_data, label="{} - {}".format(ticker, desc))
        plt.legend(handles=[div, sp, comp])
        plt.axhline(0, color="black")
        plt.savefig("{}.png".format(ticker))
        plt.clf()
#print(key)
        continue
