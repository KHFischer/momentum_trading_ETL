def extract_universe(path):
    res = pd.read_csv(path, usecols=[0], names=['Ticker'])
    return res

def extract_price_df(ticker):
    this_month = datetime.today().replace(day=1)
    final_month = this_month + relativedelta(months=-24)

    symbol = ticker

    # Downloading ticker and transforming df
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=final_month, end=this_month, interval='1d', actions=False)
    df = df['Close'].to_frame()
    
    # Calculate 100dma
    df['sma100'] = df['Close'].rolling(100).mean()
    df.dropna(inplace=True)
    df.sort_index(ascending=False, inplace=True)
    
    return df

def calc_above(df):
    above_count = 0

    for i in range(len(df)):
        if df['Close'].iloc[i] > (df['sma100'].iloc[i] * 0.98):
            above_count += 1
        else: break

    return above_count

def execute_rolling_method():
    print('-->              Screening days above SMA')
    
    path = f'C:\\Users\\kalle\\My python stuff\\dma_output_{date.today().month}-{date.today().year}.txt'
    universe = extract_universe(path)
    delta_dict = {}
    
    for i in universe['Ticker']:
        df = extract_price_df(i)
        delta_dict[i] = calc_above(df)
    
    df = pd.DataFrame(delta_dict, index=['Delta']).T
    res = list(df[(df.Delta > 100)].index)
    np.savetxt(f'above_output_{date.today().month}-{date.today().year}.txt', res, delimiter=', ', fmt ='% s')
    
    print(f'-->              Process finished. File saved as: "final_output_{date.today().month}-{date.today().year}.txt"')
