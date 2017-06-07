import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import datetime
import time

ITEMS = requests.get('https://rsbuddy.com/exchange/summary.json').json()
SERVER = 'https://api.rsbuddy.com/grandExchange?'

###### helper functions ######

# quickly get current prices for a given item id
def price(item_id):
    try:
        return ITEMS[item_id]
    except:
        return None

# converts epoch to human readable
def epoch2datetime(epoch):
    return datetime.datetime.fromtimestamp(epoch/1000.)
    
def datetime2epoch(date):
    # epoch milliseconds
    return str(int(date.strftime('%s'))*1000)

##############################

class Item:
    '''
    Class that defines an item in osrs
    '''
    
    def __init__(self,item_id=0):
        self.item_id = str(item_id)

    # returns the guidePrice for an item at a current time.
    # optional:
    #   date: datetime object (e.g. datetime.datetime(2017,12,31,11,59,59,0))
    def guidePrice(self,date=-1):
        
        if date == -1:
            r = requests.get(SERVER+'a=guidePrice&i='+self.item_id)
            return r.json()
        else:
            date = datetime2epoch(date)
            r = requests.get(SERVER+'a=graph&i='+self.item_id+'&start='+date)
            return r.json()[0]
    
    # default is 6 hours of date in 30 minute increments
    # plots and returns data
    def graph(self,g=None,start=None,data=False):
    
        if g and start:        
            g = str(g)
            date = datetime2epoch(start)
            opt_str = '&start='+date+'&g='+g
        elif start:        
            date = datetime2epoch(start)
            opt_str = '%start='+date
        elif g:
            g = str(g)
            opt_str = '&g='+g
        else:
            opt_str=''
        
        r = requests.get(SERVER+'a=graph&i='+self.item_id+opt_str)
        
        if data:
            return r.json()
        else:
            self.plot(r.json())
        
    def plot(self,json_data):
        times = []
        buyingC = []
        overallC = []
        sellingC = []
        buyingP = []
        overallP = []
        sellingP = []
        
        for price in json_data:
            times.append(epoch2datetime(price["ts"]))
            buyingC.append(price["buyingCompleted"])
            overallC.append(price["overallCompleted"])
            sellingC.append(price["sellingCompleted"])
            buyingP.append(price["buyingPrice"])
            overallP.append(price["overallPrice"])
            sellingP.append(price["sellingPrice"])
            
        times = mdates.date2num(times)
        plt.plot(times,buyingP,marker='.',label='Buying Price')
        plt.plot(times,sellingP,marker='.',label='Selling Price')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m - %H:%M:%S'))
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.ylabel('price (gp)')
        plt.title(ITEMS[self.item_id]["name"])
        plt.tight_layout()
        plt.show()
    
    
    
    
    
    
    
    
