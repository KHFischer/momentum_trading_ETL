def extract_universe(path):
    universe = pd.read_csv(path)
    return universe

def ticker_data(symbol):
    
    this_month = datetime.today().replace(day=1)
    final_month = this_month + relativedelta(months=-12)

    # Downloading tickers and transforming df
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=final_month, end=this_month, interval='1d', actions=False).reset_index()
    df = df[['Date', 'Close']]
    
    return df

def sma_cols(df):
    # 200 day sma indicator
    sma = SMAIndicator(df['Close'], 200)
    df['dma200'] = sma.sma_indicator()

    # 100 day sma indicator
    sma = SMAIndicator(df['Close'], 100)
    df['dma100'] = sma.sma_indicator()

    # 50 day sma indicator
    sma = SMAIndicator(df['Close'], 50)
    df['dma50'] = sma.sma_indicator()
    
    return df

def condition(df, symbol):
    # Transform df
    df.dropna(inplace=True)
    df.sort_values('Date', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    # Filter empty df
    if len(df) > 1:
        # Append ticker to tickerlist based on condition
        if (df.Close[0] > df.dma200[0]) and (df.dma50[0] > df.dma100[0]) and df.dma100[0] > df.dma200[0]:
            return symbol
        else: pass
        
def execute_sma_list():
    print('-->              Screening SMA')
    
    path = f'C:\\Users\\kalle\\My python stuff\\output_{date.today().month}-{date.today().year}.csv'
    universe = extract_universe(path)
    
    tickerlist = []
    
    for i in universe.Ticker:
        price_data_df = ticker_data(i)
        sma_df = sma_cols(price_data_df)
        tickerlist.append(condition(sma_df, i))
    
    res = np.array(list(filter(lambda item: item is not None, tickerlist)))
    np.savetxt(f'dma_output_{date.today().month}-{date.today().year}.txt', res, delimiter=', ', fmt ='% s')
    
    print(f'-->              SMA screen completed, file saved as "dma_output_{date.today().month}-{date.today().year}.txt"')
