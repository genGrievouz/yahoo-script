import csv
import sys
import pandas
import datetime as dt
from createAll import loadData
import matplotlib.pyplot as plt

class Options:
    def __init__(self, price, reserve, names, percentage, year_s, year_e, interval):
        self.price = price
        self.reserve = reserve
        self.names = names
        self.percentage = percentage
        self.year_s = year_s
        self.year_e = year_e
        self.interval = interval
        self.start_p = []
        self.next_p = []
        self.df_plot = pandas.DataFrame(columns=names)

        proc = (self.price-self.reserve)/self.price

        if sum(self.percentage) > proc:
            print("Suma procent je wiynkszo niz " + str(proc*100) + "%. Rezerwa a percentage som inne. Sprawdz")
            sys.exit()
    
    def getSumPrice(self):
        if len(self.names) == len(self.percentage):
            for i in range(len(self.percentage)):
                se = self.price * self.percentage[i]
                self.start_p.append(se)
        else:
            print("Delka miana a delka percentage nie som stejne")       

    def openIt(self, file_name):
        df = pandas.read_csv(file_name)
        return df

    def chooseYear(self):
        df = self.openIt()
        year = self.years
        df['Date'] = pandas.to_datetime(df['Date'])
        include = df[df['Date'].dt.year == year]
        exclude = df[df['Date'].dt.year != year]
        return include

    def buySell(self, a, next_a):
        d = sum(a) / len(next_a)
        all_price = []
        for i in range(len(next_a)):
            all_price.append(round(d/next_a[i]))    
        return all_price  

    def calculateDiff(self):        
        a = loadData(self.names, self.year_s, self.year_e, self.interval)
        b = a.createDF()
        file_name = str(self.year_s) + "-" + str(self.year_e) + ".csv"
        data = self.openIt(file_name)
        diff_all = pandas.DataFrame(columns=self.names)
        for i in self.names:
            list = []
            for j in range(len(data.index)-1):
                list.append(data[i].iloc[j+1] - data[i].iloc[j])
            diff_all[i] = list
        return diff_all

    def calculateCount(self):
        self.getSumPrice()
        diff = self.calculateDiff()
        file_name = str(self.year_s) + "-" + str(self.year_e) + ".csv"
        data = self.openIt(file_name)
        data = self.deleteDate(data.values.tolist())
        for i in range(len(data)):
            if i == 0:
                count1 = [round(a/b) for a,b in zip(self.start_p,data[i])]
                next_budget = [round(a*b) for a,b in zip(count1, data[i+1])]
                #print(next_budget)
                print(count1)
                count2 = self.buySell(next_budget, data[i+1])
                series = pandas.Series(next_budget, index = self.names)
                self.df_plot = self.df_plot.append(series, ignore_index=True)
                self.next_p = next_budget                
            elif i == len(data)-1:
                sum_all = sum([a*b for a,b in zip(count2, data[i])])
                break
            else:
                count1 = [round(a/b) for a,b in zip(self.next_p,data[i])]
                next_budget = [round(a*b) for a,b in zip(count1, data[i+1])]
                print(count1)
                count2 = self.buySell(next_budget, data[i+1])
                series = pandas.Series(next_budget, index = self.names)
                self.df_plot = self.df_plot.append(series, ignore_index=True)
                self.next_p = next_budget
        
        print("Za rok " + str(self.year_s) + "-" + str(self.year_e) + " zarobiles " + str(round(sum_all - sum(self.start_p),2)) + "$ ,czyli " + str(round(((sum_all/sum(self.start_p))-1)*100,2)) + "%")
    
    def deleteDate(self,df):
        for i in range(len(df)):
            df[i].pop(0)
        return df

    def plotData(self):
        df = self.df_plot
        (df.plot(title=str(self.year_s) + "-" + str(self.year_e) + " " + str(self.names))
           .set(xlabel = "months", ylabel="USD"))
        plt.show()

    def plotDataSum(self):
        df1 = self.df_plot
        column_list = list(df1)
        df1["sum"] = df1[column_list].sum(axis=1)
        df1["sum"].plot()
        plt.show()

def main():
    # Nastaw Options na budzet, rezerwa, [nazwy], [procenta], lata, interval
    a = Options(10000, 0,["SPY","TLT","GLD"], [0.33,0.33,0.33], 2005, 2020, '1mo')
    a.calculateCount()
    a.plotData()
    a.plotDataSum()

main()
    


    
    

    

