#-*- coding: utf-8 -*-
#CrawBaiduStocksB.py
import requests
from bs4 import BeautifulSoup
import traceback
import re
import csv

def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""

def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    '''
    在无关a标签中有一个东方财富网的股票代码a标签，所以第一个总是显示东方财富网的信息，代码列表中也有相应的信息，
    出现重复，这是无用数据，要过滤掉。3种方法：
        1.先定位div，再定位a标签
        2.加入去重复代码
        3.把stockList的第一个a标签pop()出去
    '''
    # div = soup.find('div',{'class':'quotebody'})
    # # print(type(div))
    # a = div('a')
    a = soup.find_all('a')
    for i in a:
        try:
            '''
                this is ok: a.get('href')
                but that is KeyError: a.attrs['href']
                print(a.get('href'))
            '''
            href = i.get('href')
            code = re.findall(r"[s][hz]\d{6}", str(href))
            #存在code为空的情况
            if code:
                ##下面两种方法都行，extend()方法不需要判断code是否为空
                #lst.extend(code)
                lst.append(code[0])
        except:
            continue
    lst.pop(0)

def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html=="":
                continue
           
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div',attrs={'class':'stock-bets'})
            if stockInfo:
                infoDict = {}
                name = stockInfo.find_all(attrs={'class':'bets-name'})[0]
                infoDict['股票名称'] = name.text.split()[0]
                infoDict['股票代码'] = stock
                
                keyList = stockInfo.find_all('dt')
                valueList = stockInfo.find_all('dd')
                
                ##keyList为空，结束本圈循环，清除一些无用股票
                if len(keyList) < 1:
                    continue
                
                for i in range(len(keyList)):
                    key = keyList[i].text
                    val = valueList[i].text
                    infoDict[key] = val
            
                # with open(fpath+'BaiduStockInfoB.txt', 'a', encoding='utf-8') as f:
                #     f.write( str(infoDict) + '\n' )

                with open(fpath+'stockB.csv', 'a', newline='') as f:
                    w = csv.writer(f)
                    #以键值对的格式存储到csv，eg.('k','v')
                    w.writerow(infoDict.items())
                f.close()

                count = count + 1
                print("\r当前进度: {:.2f}%".format(count*100/len(lst)),end="")
        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count*100/len(lst)),end="")
            continue


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'E:/python/exercise/p3/'
    slist=[]
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)

main()
