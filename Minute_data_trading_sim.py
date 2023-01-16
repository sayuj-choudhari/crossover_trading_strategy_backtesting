import numpy as np
import math
import csv
import time
import matplotlib.pyplot as plt

#TSLA : 1.8%
#NVDA : 2.3%
#SNOW : 6.0%

stoploss_sell = 0
second_hold = 0

from csv import reader
# skip first line i.e. read header first and then iterate over each row od csv as a list
with open('ETHUSD.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        count = 0
        low_list = []
        close_list = []
        dates = []
        sma = []
        lma = []

        for i in range (0, 11):
            sma.append(0)
        
        hold = 0
        profit = 0

        win = 0
        total_trade = 0
        total_gain = 0

        for row in csv_reader:
            close_list.append(float(row[5].replace(',', '')))
            low_list.append(float(row[4].replace(',', '')))
            dates.append(row[0])
            count += 1
            if count >= 5:
                sma.append((sum(low_list[len(low_list) - 5: len(low_list)])) / 5)
                #print(sma[len(sma) - 1])
            if count >= 15:
                lma.append((sum(low_list[len(low_list) - 15: len(low_list)])) / 15)

            if(count > 15):
                if hold!= 0:
                    if float(row[4].replace(',', '')) < hold * .999:
                        print("STOP SELL", row[0], "{:.2f}".format(hold*.999), ": -{:.2f}".format(hold* .00105))
                        profit -= hold - float(row[4].replace(',', '')) #hold* .00105
                        hold = 0
                        total_trade += 1
                        stoploss_sell = 1
                if stoploss_sell!= 0:
                    if float(row[4].replace(',', '')) > original_hold * 1.001:
                        if(hold!= original_hold * 1.00105):
                            print("RE-BUY", row[0], '{:2f}'.format(original_hold * 1.001))
                        hold = original_hold * 1.00105

                
                if(lma[len(lma) - 1] < sma[len(sma) - 1] and lma[len(lma) - 2] > sma[len(sma)- 2]):
                    if hold == 0:
                        print("BUY", row[0],  row[5].replace(',', ''))
                        hold = float(row[5].replace(',', ''))
                        stoploss_sell = 0
                        original_hold = hold
        
                if(lma[len(lma) - 1] > sma[len(sma) - 1] and lma[len(lma) - 2] < sma[len(sma)- 2]):
                    
                    if hold != 0:
                        print("SELL", row[0], float(row[5].replace(',', '')), ": {:.2f}".format(float(row[5].replace(',', '')) * .99995 - hold))
                        profit += float(row[5].replace(',', '')) * .99995 - hold
                        total_trade += 1
                        if (float(row[5].replace(',', '')) * .99995 - hold) > 0:
                            win += 1
                            total_gain += float(row[5].replace(',', '')) * .99995 - hold
                        hold = 0
                        stoploss_sell = 0
                    '''
                    if stoploss_sell!= 0:
                        if (float(row[5]) * .99995 - original_hold) > 0:
                            print("BUY", row[0], original_hold)
                            print("SELL", row[0], float(row[5]), ": {:.2f}".format(float(row[5]) * .99995 - original_hold))
                            profit += float(row[5]) * .99995 - original_hold
                    '''



                #print(row[0], row[5])

        
        
        

        
        
        print("Original Investment on {}: $1500.00".format(dates[0]))
        print("Current Investment Value on {}: ${:.2f}".format(dates[len(dates) - 1], 1500 + 1500 * profit / close_list[0]))





