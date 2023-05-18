import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from IPython.display import display, HTML
import seaborn as sns
from time import gmtime
import os
import time
import pickle
import quantstats as qs

def detect_dc(data, threshold = 0.05):
    
    # Initialization 
    dc = threshold  # threshold 
    reference_price = data[0]
    start_dc = 0   #start index of DC
    end_dc = 0   #end  index of DC
    start_os = 0   #start index of Overshoots
    end_os = 0   #end index of Overshoots
    dc_lst = []
    
    # detect first dc change
    for idx in range(1, len(data)):
        if abs((data[idx]/reference_price)-1)>=dc:  # dc happened
            end_dc = idx
            start_os = idx
            end_os = idx
            #print(reference_price)
            if (data[idx]/reference_price)-1 >=0: # upward dc at first
                event = True
                break
            else:                                   # downward dc at first
                event = False
                break      
        else:
            pass
    
    highest_idx = end_dc+1
    lowest_idx = end_dc+1
    
    reference_price = data[end_dc]
    #print(reference_price)
    
    # detect first overshoot
    for idx in range(end_dc+1, len(data)):
        if event:   # upward dc
            if data[idx] >= reference_price:
                reference_price = data[idx]  # renew highest price
                highest_idx = idx
            else:
                if ((data[idx]/reference_price))<1-dc: # end of overshoot
                    start_os = end_dc
                    end_os = highest_idx
                    #print(idx)
                    break
                else:
                    pass
        else:   # downward dc
            if data[idx] >= reference_price:
                reference_price = data[idx]  # renew lowest price
                lowest_idx = idx
            else:
                if ((data[idx]/reference_price))>1+dc: # end of overshoot
                    start_os = end_dc
                    end_os = lowest_idx
                    break
            
    dc_lst.append([event,start_dc,end_dc,start_os,end_os])
    
    # find further DC
    check = end_os
    while check <len(data)-1:
        for i in range(check,len(data)):
            
            if dc_lst[-1][0]: # previous dc is upward trend
                if (data[i]/reference_price) <=1-dc: # downward dc happen
                    event = False
                    start_dc = dc_lst[-1][4]
                    end_dc = i
                    start_os = i
                    lowest_idx = i
                    # find the end point of the overshoot
                    for idx in range(i, len(data)):
                        if data[idx] <= reference_price:
                            reference_price = data[idx]  # renew lowest price
                            lowest_idx = idx
                        else:
                            if ((data[idx]/reference_price))>=1+dc: # end of overshoot
                                end_os = lowest_idx
                                #print(idx)
                                break
                    if dc_lst[-1][4] != end_os:
                        dc_lst.append([event,start_dc,end_dc,start_os,end_os])
                        break
                    else:   #last point
                        dc_lst.append([event,start_dc,end_dc,start_os,len(data)-1])
                        break
                    
                    
            else:   # previous dc is downward
                if (data[i]/reference_price) >=1+dc: # upward dc happen
                    event = True
                    start_dc = dc_lst[-1][4]
                    end_dc = i
                    start_os = i
                    lowest_idx = i
                    # find the end point of the overshoot
                    for idx in range(i, len(data)):
                        if data[idx] >= reference_price:
                            reference_price = data[idx]  # renew lowest price
                            highest_idx = idx
                        else:
                            if ((data[idx]/reference_price))<=1-dc: # end of overshoot
                                end_os = highest_idx
                                #print(idx)
                                break
                    if dc_lst[-1][4] != end_os:
                        dc_lst.append([event,start_dc,end_dc,start_os,end_os])
                        break
                    else:   #last point
                        dc_lst.append([event,start_dc,end_dc,start_os,len(data)-1])
                        break
        check = dc_lst[-1][4]
    
    return dc_lst

def plt_dc(data, dc_lst, name):
    plt.figure(figsize=(10,4))
    ax=plt.axes()
    plt.plot(data,alpha=0.5)
    for i in range(0,len(dc_lst)): 
        tdc_0 = dc_lst[i][1]
        tdc_1 = dc_lst[i][2]
        tos_0 = tdc_1
        tos_1 = dc_lst[i][4]
        arrow1 = ax.arrow(tos_0, data[tos_0], tos_1-tos_0, data[tos_1]-data[tos_0], head_length=20, length_includes_head=True, width=1, fc='g', ec='g') 
        arrow2 = ax.arrow(tdc_0, data[tdc_0], tdc_1-tdc_0, data[tdc_1]-data[tdc_0], head_length=20, length_includes_head=True, width=1, fc='r', ec='r') 
    ax.grid()
    plt.legend((arrow1,arrow2), ['Overshoots','Directional Changes'])
    plt.xlabel("Record time")
    plt.ylabel("Close price")
    plt.title('Directional Change in ' +str(name))
    plt.show()
    
if __name__ == '__main__':
    
    datafilename = "./DailyClosing-SelectedIndices-2019to2021.xlsx"
    index_data = pd.read_excel(datafilename, index_col=0, parse_dates=True, sheet_name=None)
    for i in index_data['Indices']['Index']:
        print(i)
        
    all_return_record = []
    all_return_mean = []
    all_volatilities = []
    all_VaR = []
    all_CVaR = []
    all_sharpe = []


    for i in index_data['Indices']['Index']:
        current_price = index_data[i]['Close']
        returns = current_price.pct_change() # caculate the array of return
        all_return_record.append(returns) # store to the record
        all_return_mean.append(returns.mean())
        all_volatilities.append(returns.std())
        all_VaR.append(qs.stats.var(current_price))
        all_CVaR.append(qs.stats.cvar(current_price))
        all_sharpe.append(qs.stats.sharpe(current_price))


    data=index_data['ASX200']['Close']
    data.reset_index(drop=True, inplace=True)
    dc_lst = detect_dc(data,threshold=0.05)
    plt_dc(data, dc_lst,'ASX200')
    print(dc_lst)