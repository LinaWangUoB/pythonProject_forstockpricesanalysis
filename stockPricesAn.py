# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import pandas as pd
import yfinance as yf
from datetime import datetime

#print(pd.Timestamp("2015-01-01") - pd.DateOffset(days=1))
start_date = datetime.now() - pd.DateOffset(months=3)
end_date = datetime.now()
tickers = ['AAPL', 'MSFT', 'NFLX', 'GOOG']
print('tickers:',tickers)
#data_1=yfinance.download(tickers,start="2015-01-01",end="2020-02-21")
#define df_list
df_list = []

for ticker in tickers:
    data =yf.download(ticker, start=start_date, end=end_date)
    df_list.append(data)
df = pd.concat(df_list, keys=tickers, names=['Ticker', 'Date'])
print(df.head())
#append() method add elements to the end of the list;
#df_head():pandas.DataFrame.head, returns the first n rows; df.head(3) first 3 rows;
#pd.concat:Concatenate pandas objects along a particular axis.pandas.concat(objs, *, axis=0, join='outer', ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=False, copy=None)
#pandas.DataFrame.reset_index: reset the index, or a level of it.
df = df.reset_index()
print(df.head())
#draw charts; plotly; same with plot;
import plotly.express as px
fig = px.line(df, x ="Date", y="Open", color='Ticker', title ='Stock Market Performance for the Last 3 Months')
fig.show()
#area plot; fx.area; facet and trellis plots;
fig = px.area(df, x='Date', y='Close', color='Ticker',
              facet_col ='Ticker',
              labels={'Date':'Date', 'Open':'Opening Price', 'Ticker':'Company'},
              title='Stock Market Performance for Apple, Microsoft, Netflix, and Google')
fig.show()
#df[['Asset1','Asset2']].rolling(10).corr().unstack().iloc[:,0];
#multiple assets;df[['Asset1','Asset2','Asset3']].rolling(100).corr().unstack().iloc[:,[0,1]];
df['MA10'] = df.groupby('Ticker')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
df['MA20'] = df.groupby('Ticker')['Close'].rolling(window=20).mean().reset_index(0, drop=True)

for ticker, group in df.groupby('Ticker'):
    print(f'Moving Averages for {ticker}')
    print(group[['MA10', 'MA20']])

for ticker, group in df.groupby('Ticker'):
    fig = px.line(group, x='Date', y=['Close', 'MA10', 'MA20'],
                  title=f"{ticker} Moving Averages")
    fig.show()
#statistical analysi: volatility etc.
df['Volatility'] = df.groupby('Ticker')['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)
fig = px.line(df, x='Date', y='Volatility',
              color='Ticker',
              title = 'Volatility of All Companies')
fig.show()
#correlation between the stock prices of apple and microsoft;
#creat a DataFrame with the stock prices of Apple and microsoft;
apple = df.loc[df['Ticker'] == 'AAPL', ['Date', 'Close']].rename(columns={'Close': 'AAPL'})
microsoft = df.loc[df['Ticker'] == 'MSFT', ['Date', 'Close']].rename(columns={'Close': 'MSFT'})
df_corr = pd.merge(apple, microsoft, on='Date')
fig = px.scatter(df_corr, x='AAPL', y='MSFT',
                 trendline='ols',
                 title='Correlation between Apple and Microsoft')
fig.show()

