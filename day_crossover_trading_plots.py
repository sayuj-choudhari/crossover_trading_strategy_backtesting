"""
CS1 22fa MP5 Part C

Student Name: Sayuj Choudhari

Brief Overview: 
This program simulates a crossover trading strategy on daily stock data, in this
case Apple stock, Microsoft. Crossover trading is a trading strategy that aims to capture 
the price momentum of a stock through the intersection of short-term and long-term
moving averages. If the short-term moving average rises above the long-term moving
average there is an indicator that the stock price will go down and should therefore
signal the trader to sell the stock and/ or take a short position on it. Alternatively,
if the short-term moving average goes below the long-term moving average, there is an
indicator that stock price will go up and should therefore signal the trader to buy the
stock and/ or sell there short position. 

This code plots the Apple stock and Microsoft pricing data along with the short-term moving average
(5 days) and long-term moving average (20 days), signalling sell/ short points in red
and buy/ sell short points in green.

Note: Calculated the profit in another code file for both cases of Apple/ Microsoft data, if a trader had
just bought a stock on the first date of data collected and sold it on the last date of data collected,
they would have lost ~$10, but with the crossover strategy implemented the trader would have made $31
when trading Apple. With Microsoft the trader would have lost ~$95 but with crossover strategy implemented
the trader would have made ~$33, which is suggestive that the strategy is pretty effective.


Data Source(s): Any Yahoo! Finance Daily Pricing data csv file, Apple stock data
                in this case
Data Science Question: 
    Identify crossovers in the short-term and long-term moving averages of Apple
    stock data, and marking the crossover point and price with buy/ sell points
    dependent on the type of crossover.

Room for Improvement: (Optional)
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
# You may add additional imports if you choose to use them

# You may choose to change/add constants here as appropriate for
# your plotting program.

# Default marker size for plotted points
MARKER_SIZE = 8
# Default line width for plotted trajectories
LINE_WIDTH = 2


def get_pricing_coords(filename):
    """
    Returns the lists of date, price points in the daily stock data file inputed
    as 'filename'

    Arguments:
        - filename (String): csv file path for Yahoo! Finance Daily Stock Data

    Returns:
        - time, price (tuple): a tuple of list 'time' that contains all the dates
                               of daily data, and list 'price' which contains all
                               daily open price data corresponding to those dates
    """
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        result = {}
        # Initialize the keys for the result dictionary with empty
        # lists we'll populate with row data
        for column_name in csvreader.fieldnames:
            result[column_name] = []

        for row in csvreader:
            # We have to do a nested loop since we're processing row-by-row
            # but need to collect each key=value pair for the result dict
            for column_name, value in row.items():
                result[column_name].append(value)
        price = []
        time = []
        for i in range(0, len(result['Date'])):
            price.append(float(result['Open'][i]))
            time.append(result['Date'][i])
        return (time, price)
        #return (result['Date'], result['Open'])


def plot_pricing_coords(filename, ax):
    """
    Reads in date and price data for inputed filename and plots the data
    with date on the x-axis and daily price on the y-axis, sets xticks
    for dates as well for the plot.

    Arguments:
        - filename (String): csv file path for Yahoo! Finance Daily Stock Data
        - ax (Axes object): Axes object to plot on

    Returns:
        - None (plots pricing data)
    """
    time, price = get_pricing_coords(filename)
    ax.plot(time, price, label = 'Daily Price')
    x_ticks = []
    for i in range(0, len(time), 60):
        x_ticks.append(time[i])

    ax.set_xticks(x_ticks)




def get_ma_coords(increment, filename):
    """
    Reads in date and price data for inputed filename and creates new date and
    price points of moving averages for the inputed 'increment' amount of days
    (e.g. get_ma_coords(20, AAPL_data.csv) creates 20 day moving average of 
    daily stock price for Apple)

    Arguments:
        - increment (int): amount of days to take moving average of
        - filename (String): csv file path for Yahoo! Finance Daily Stock Data

    Returns:
        - ma_time, ma_price, label (tuple): 
    """
    time, price = get_pricing_coords(filename)
    ma_price = []
    ma_time = []
    for i in range(increment, len(price)):
        total = 0
        for n in range(i- increment, i):
            total += price[n]
        ma_price.append(total / increment)
        ma_time.append(time[i])

    label = '{}-day moving average'.format(increment)
    return(ma_time, ma_price, label)

def plot_ma_coords(increment, filename, ax):
    """
    Plots the moving average data for inputed filename of stock data for the
    inputed increment of time

    Arguments:
        - increment (int): amount of days to take moving average of
        - filename (String): csv file path for Yahoo! Finance Daily Stock Data
        - ax (Axes object): Axes object to plot on

    Returns:
        - None (plots pricing data for moving average)
    """
    ma_time, ma_price, ma_label = get_ma_coords(increment, filename)
    ax.plot(ma_time, ma_price, label = ma_label)

def plot_short_crossovers(short_inc, long_inc, filename, ax):
    """
    Identifies and marks sell/ short crossovers of moving average data for inputed short increment
    and long increment (e.g. 5 days and 20 days) for inputed filename of stock daily
    daily pricing data.

    Arguments:
        - short_inc (int): amount of days to take short-term moving average of
        - long_inc (int): amount of days to take long-term moving average of
        - filename (String): csv file path for Yahoo! Finance Daily Stock Data
        - ax (Axes object): Axes object to plot on

    Returns:
        - None (plots crossover markers and action signals in red)
    """
    s_time, s_price, empty = get_ma_coords(short_inc, filename)
    l_time, l_price, empty = get_ma_coords(long_inc, filename)
    price = get_pricing_coords(filename)[1]

    diff = long_inc - short_inc

    for i in range (0, len(l_time) - 2):
        if (s_price[i + diff] > l_price[i]) and (s_price[i + diff + 1] < l_price[i + 1]):

            ax.plot(l_time[i + 1], l_price[i + 1], marker='D',
            color = 'r', markersize = MARKER_SIZE)
            
            ax.plot(l_time[i + 1], price[i + 1 + long_inc], marker = '*',
            color = 'r', markersize = MARKER_SIZE)

def plot_long_crossovers(short_inc, long_inc, filename, ax):
    """
    Identifies and marks buy/ sell short crossovers of moving average data for inputed short increment
    and long increment (e.g. 5 days and 20 days) for inputed filename of stock daily
    daily pricing data.

    Arguments:
        - short_inc (int): amount of days to take short-term moving average of
        - long_inc (int): amount of days to take long-term moving average of
        - filename (String): csv file path for Yahoo! Finance Daily Stock Data
        - ax (Axes object): Axes object to plot on

    Returns:
        - None (plots crossover markers and action signals in green)
    """
    s_time, s_price, empty = get_ma_coords(short_inc, filename)
    l_time, l_price, empty1 = get_ma_coords(long_inc, filename)
    price = get_pricing_coords(filename)[1]

    diff = long_inc - short_inc

    for i in range (0, len(l_time)-2):
        if (s_price[i+15] < l_price[i]) and (s_price[i+16] > l_price[i+1]):


            ax.plot(l_time[i+1], l_price[i+1], marker='D',
            color= 'g', markersize=MARKER_SIZE)
            
            ax.plot(l_time[i+1], price[i + 1 + long_inc], marker='*',
            color= 'g', markersize=MARKER_SIZE)
            



def configure_plot(stock_name, ax, hold_profit, profit):
    """
    Configures plot axes, labels, and legend

    Arguments:
        - stock_name (string): name of stock data analyzed for title
        - ax (Axes object): Axes object to plot on

    Returns:
        - None (configures plot)
    """
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    ax.set_title(f'{stock_name} Stock Crossover Plot (Profit of just holding stock: \${hold_profit:.2f}'+
    f', Profit with strategy: ${profit:.2f})')
    ax.plot([], [], 'r*', label='Sell/ Short Price', markersize=MARKER_SIZE - 5)
    ax.plot([], [], 'rD', label='Sell/ Short Crossover', markersize=MARKER_SIZE - 5)

    ax.plot([], [], 'g*', label='Buy/ Sell Short Price', markersize=MARKER_SIZE - 5)
    ax.plot([], [], 'gD', label='Buy/ Sell Short Crossover', markersize=MARKER_SIZE - 5)
    ax.legend(loc='upper right', prop={'size': 6})





# Provided
def start(filename, stock_name, short_inc, long_inc, ax, hold_profit, profit):
    """
    "Launching point" of the program! Sets up the plotting configuration
    and initializes the plotting of 
    
    Plots the pricing data, short-term moving average, and long-term moving
    averages based on inputed filename of data and length of short and long
    moving averages. Indicates strategic points of sell/ short in red and
    buy/ sell short in green

    Arguments:
        - filename (String): csv file path for Yahoo! Finance Daily Stock Data
        - stock_name (String): Name of stock being analyzed for plot title
        - short_inc (int): amount of days to take short-term moving average of
        - long_inc (int): amount of days to take long-term moving average of
        - ax (Axes object): Axes object to plot on

    Returns:
        - None (plots the analysis)

    """
    # Provided as a start for Part C, modify as needed

    # TODO: Call a function that plots your data, similar to plot_trial_data
    # in Part B

    # Recommended: But you would need to change based on your
    # plot programming. Remove if you don't use this.



    plot_pricing_coords(filename, ax)
    plot_ma_coords(long_inc, filename, ax)
    plot_ma_coords(short_inc, filename, ax)

    plot_short_crossovers(short_inc, long_inc, filename, ax)
    plot_long_crossovers(short_inc, long_inc, filename, ax)

    fig.set_size_inches(12, 18)
    configure_plot(stock_name, ax, hold_profit, profit)


if __name__ == '__main__':
    fig, axes = plt.subplots(2, 1)
    axis_1, axis_2 = axes

    start('AAPL_data.csv', 'Apple', 5, 20, axis_1, -9.79, 31.77)
    start('ETH-USD.csv', 'Ethereum', 5, 20, axis_2, -3310.09, 2456.18)

    plt.show()
