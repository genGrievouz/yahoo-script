import sys
import http.client
import yfinance as yf
import pandas as pd
import os

class loadData:
    def __init__(self,name,year_s,year_e, interval):
        self.name = name
        self.start = str(year_s) + "-01-01"
        self.end = str(year_e+1) + "-01-04"
        self.y_s = str(year_s)
        self.y_e = str(year_e)
        self.interval = interval

    def loadMarket(self,i):
        data = yf.download(self.name[i], start=self.start, end=self.end, interval=self.interval)
        data = data['Close']
        return data

    def createDF(self):
        df = pd.DataFrame() 
        for i in range(len(self.name)):            
            d = pd.DataFrame(self.loadMarket(i))
            d.columns = d.columns.str.replace('Close',self.name[i])
            d.dropna(subset = [self.name[i]], inplace=True)
            df = pd.concat([df,d], axis=1)
        output = df.to_csv(self.y_s + "-" + self.y_e + ".csv")
        return output