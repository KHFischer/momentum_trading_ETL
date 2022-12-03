import pandas as pd
import numpy as np
import yfinance as yf
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date

def extract_universe():
    path = 'C:\\Users\\kalle\\My python stuff\\universe_atr.csv'
    universe = pd.read_csv(path)
    universe.dropna()
        
    return universe
        
def initiate():
    ticker = 'AAPL'
        
    # Time period that we will request
    this_month = datetime.today().replace(day=1)
    six_month = this_month + relativedelta(months=-6)
    final_month = this_month + relativedelta(months=-12)

    # Requesting data and slicing relevant part
    aapl = yf.Ticker(ticker)
    df = aapl.history(start=final_month, end=this_month, interval='1mo', actions=False).reset_index()
    df = df[['Date', 'Close']]

    # Group dataframe by instrument
    df = df.set_index('Date').T

    # Add a ticker column
    df['Ticker'] = ticker

    # Normalise column names
    mapping = {
        df.columns[12]: 'month_0',
        df.columns[11]: 'month_1',
        df.columns[10]: 'month_2',
        df.columns[9]: 'month_3',
        df.columns[8]: 'month_4',
        df.columns[7]: 'month_5',
        df.columns[6]: 'month_6',
        df.columns[5]: 'month_7',
        df.columns[4]: 'month_8',
        df.columns[3]: 'month_9',
        df.columns[2]: 'month_10',
        df.columns[1]: 'month_11',
        df.columns[0]: 'month_12'}

    df = df.rename(columns=mapping)
        
    return df
    
def gen_data(ticker):
    
    # Time period that we will request
    this_month = datetime.today().replace(day=1)
    six_month_ago = this_month + relativedelta(months=-12)

    # Requesting data and slicing relevant part
    data = yf.Ticker(ticker)
    ticker_data = data.history(start=six_month_ago, end=this_month, interval='1mo', actions=False).reset_index()
    ticker_data = ticker_data[['Date', 'Close']]

    # Group dataframe by instrument
    ticker_data = ticker_data.set_index('Date').T

    # Add a ticker column
    ticker_data['Ticker'] = ticker
    
    # Some tickers produce errors, we will store these in a list for debugging purposes
    error_list = []

    # Make sure 12 months of data is available    
    if len(ticker_data.columns) == 14:
        
        # Normalise column names
        mapping = {
            ticker_data.columns[12]: 'month_0',
            ticker_data.columns[11]: 'month_1',
            ticker_data.columns[10]: 'month_2',
            ticker_data.columns[9]: 'month_3',
            ticker_data.columns[8]: 'month_4',
            ticker_data.columns[7]: 'month_5',
            ticker_data.columns[6]: 'month_6',
            ticker_data.columns[5]: 'month_7',
            ticker_data.columns[4]: 'month_8',
            ticker_data.columns[3]: 'month_9',
            ticker_data.columns[2]: 'month_10',
            ticker_data.columns[1]: 'month_11',
            ticker_data.columns[0]: 'month_12'}

        ticker_data = ticker_data.rename(columns=mapping)

        return ticker_data
    
    else:
        error_list.append(ticker)
    
def data_loop(df, universe):
    for i in universe.Ticker:
        df = pd.concat([df, gen_data(i)])
            
    df = df.merge(universe, how='inner', on='Ticker').drop(0)
        
    return df
    
def gen_momentum(df):
        
    df['%ATR'] = df['Average_True_Range_(14)'] / df['month_0']
    df['12M_move'] = (df['month_0'] / df['month_12']-1) / df['%ATR']
    df['6M_move'] = (df['month_0'] / df['month_6']-1) / df['%ATR']
    df['Combined_move'] = df['12M_move'] + df['6M_move']
    
    return df
    
def gen_output(df):
        
    equities = df[(df['12M_move'] >= 3) & (df['6M_move'] >= 1.5)]
    equities = equities[['Ticker', 'Market_Capitalization', 'Sector', '%ATR', '12M_move','6M_move','Combined_move']].sort_values(by='Market_Capitalization', ascending=False)
        
    return equities

def execute_screen_universe():
    print('-->              Screening universe')
    
    selected_universe = extract_universe()
    
    df = initiate()
    
    df = data_loop(df, selected_universe)
    
    df = gen_momentum(df)
    
    output = gen_output(df)
    output.to_csv(f'output_{date.today().month}-{date.today().year}.csv')
    
    print(f'-->              Screening finished, file saved as: output_{date.today().month}-{date.today().year}.csv \n')
