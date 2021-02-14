import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('AAPL.csv')

df = df.set_index(pd.DatetimeIndex(df['Date'].values))


# Create a function to calcualte the Double Exponential Moving Average (DEMA)


def DEMA(data, time_period, column):
    # Calcualte DEMA
    EMA = data[column].ewm(span=time_period, adjust=False).mean()
    DEMA = 2*EMA - EMA.ewm(span=time_period, adjust=False).mean()

    return DEMA

# Store the short term DEMA (20 day period) and the long term DEMA (50 day period) into the data set


df['DEMA_short'] = DEMA(df, 20, 'Close')

df['DEMA_long'] = DEMA(df, 50, 'Close')


# plot the chart
# create a list of columns to keep

column_list = ['DEMA_short', 'DEMA_long', 'Close']


# Visually show the clsoe price
#df[column_list].plot(figsize=(12.2, 6.4))
#plt.title('Close Price for Amazon')
#plt.ylabel('USD Price ($)')
# plt.xlabel('Date')
# plt.show()

# Create a function to bus and sell the stock (The trading strtegy)


def DEMA_strategy(data):
    buy_list = []
    sell_list = []
    flag = False
    # Loop through the data
    for i in range(0, len(data)):
        if data['DEMA_short'][i] > data['DEMA_long'][i] and flag == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag = True
        elif data['DEMA_short'][i] < data['DEMA_long'][i] and flag == True:
            buy_list.append(np.nan)
            sell_list.append(data['Close'][i])
            flag = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

    # sotre buy and sell signal/lists into the data set
    data['Buy'] = buy_list
    data['Sell'] = sell_list


# Run the stretegy to get the buy and sell signals
DEMA_strategy(df)

# Visually show the stocks buy and sell signals

plt.figure(figsize=(12.2, 4.5))
plt.scatter(df.index, df['Buy'], color='green',
            label='Buy Signal', marker='^', alpha=1)
plt.scatter(df.index, df['Sell'], color='red',
            label='sell Signal', marker='v', alpha=1)
plt.plot(df['Close'], label='Close Price', alpha=0.35)
plt.plot(df['DEMA_short'], label='DEMA_short', alpha=0.35)
plt.plot(df['DEMA_long'], label='DEMA_long', alpha=0.35)
plt.xticks(rotation=45)
plt.title('Close Price Buy and Sell Signals')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price ($)', fontsize=18)
plt.legend(loc='upper left')
plt.show()
