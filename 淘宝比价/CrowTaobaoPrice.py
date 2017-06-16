#python3
#CrowTaobaoPrice.py
import requests
import re
import csv
# 抓取淘宝指定商品的序号，价格，名称
def getHTMLText(url):
    try:
        hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        r = requests.get(url,headers=hea)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""
    
def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"',html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price , title])
    except:
        print("")

def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))
 
#存储到csv文件中，要导入csv库(系统自带)
def savetoCSV(ilt):
    csvFile = open("tb.csv",'w+')
    try:
        writer = csv.writer(csvFile)
        writer.writerow(("序号", "价格", "商品名称"))
        count = 0
        for g in ilt:
            count = count + 1
            writer.writerow((count, g[0], g[1]))
    finally:
        csvFile.close()
 
def main():
    goods = '书包'
    depth = 2   ##页数
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44*i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)
    savetoCSV(infoList)
    
main()
