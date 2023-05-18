# Directional-Change-Algorithm-for-stock-analysis![DC analysis result](https://github.com/sheepbacon/Directional-Change-Algorithm-for-stock-analysis/assets/72983721/2064f8f4-c12a-475b-a97a-d3abb65b9345)
This python code implement Directional Chnage Algorithm introduced by Professor Edwarrd P.K. Tsang
Reference paper:
https://www.researchgate.net/publication/228316274_A_Directional-Change_Event_Approach_for_Studying_Financial_Time_Series

Use dectect_dc(stockdata) to generate the Directional Change happening time point.
Also, dectect_dc can manipulate threshold value to control DC threshold.
Use plt_dc(stockdata, dc_point, 'stock_name') to show the DC line and original stock data.
More DC happen means stocks fluctuate more and active.
