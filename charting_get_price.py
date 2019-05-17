import pandas as pd
import time
import threading
import tkinter
import datetime as dt
import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import os

def get_price(ticker):
    data = requests.get('https://api.bithumb.com/public/ticker/'+ticker).text
    price = data.split(',')[2].split(':')[1]
    price = float(price.strip("\""))

    return price

def make_file(name):
    if os.path.exists(name+'_price_krw.csv'):
        df = pd.read_csv(name+'_price_krw.csv',index_col=0)
    else:
        df = pd.DataFrame({'datetime':[],'price':[]})

    price = [get_price(name)]
    now = [dt.datetime.now()]

    df2 = pd.DataFrame({'datetime':now,'price':price})

    df3= df.append(df2,ignore_index=True)
    df3.to_csv(name+'_price_krw.csv')


def monitoring():
    data = pd.read_csv('eos_price_krw.csv')
    target_price = data['price'][0]
    current_price = data['price'][len(data)-1]
    if current_price >= target_price*1.01 or current_price <= target_price*0.99:
        window = tkinter.Tk()
        window.title("Alarm")
        window.geometry("640x400")
        label = tkinter.Label(window,text="기준 : "+str(target_price)+"   현재 :"+str(current_price))
        label.pack()

        window.mainloop()

    threading.Timer(10,monitoring).start()


def processing():
    make_file('eos')
    make_file('btc')
    threading.Timer(10,processing).start()

def charting(i):
    x1 = pd.read_csv('eos_price_krw.csv',index_col=0)
    x2 = pd.read_csv('btc_price_krw.csv',index_col=0)

    ys = x1.price
    xs = x1.index

    y2s = x2.price
    x2s = x2.index

    ax1.clear()
    ax1.plot(xs,ys)

    ax2.clear()
    ax2.plot(x2s,y2s)


processing()

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

ani = animation.FuncAnimation(fig,charting,interval=1000)
plt.show()
