import yfinance as yf
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)
st.write("""
## Simple Stock Price App 

Shown are the stock price data for many companies!

**Credits**\n
-**App built by Dhanya Hegde**\n
-**Built in Python using streamlit library**
""")
st.write('---')

image = Image.open('stockpic.jpg')

st.image(image, use_column_width=True)


#Sidebar
st.sidebar.subheader('Query Parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))


#Web scraping
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()


#define ticker symbol and retrieving tickers data
ticker_list=pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
tickerSymbol=st.sidebar.selectbox('Stock ticker',ticker_list)#Select ticker of your choice

#get data on this ticker
tickerData=yf.Ticker(tickerSymbol)

#get the historical prices for this ticker

#Open High Low Close Volume Dividends Stock Splits

# Ticker Information
string_logo='<img src=%s>'% tickerData.info['logo_url']
st.markdown(string_logo, unsafe_allow_html=True)

string_name=tickerData.info['longName']
st.header('**%s**'% string_name)

string_summary=tickerData.info['longBusinessSummary']
st.info(string_summary)
st.write(tickerData.info)

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)


data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot()

num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
