# momentum_trading_ETL

This is a pipeline that extracts stock price data, calculates momentum and returns the stocks with the strongest momentum.
Extract - universe of stocks from local file + stock data from Yahoo Finance API
Transform - calculates momentum indicators based on stock-price data and moving averages
Load - a .txt file with the most interesting stocks to local directory

This pipeline was develop to quantitatively exploit the momentum anamoly as described by Eugene Fama and Kenneth French:
Fama, Eugene F. and French, Kenneth R., Dissecting Anomalies (June 2007). CRSP Working Paper No. 610, Available at SSRN: https://ssrn.com/abstract=911960 or http://dx.doi.org/10.2139/ssrn.911960 
