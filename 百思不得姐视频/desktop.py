# -*- coding:utf8 -*-
#python2
from Tkinter import *
from ScrolledText import ScrolledText
import threading
import re
import urllib
import requests
# from bs4 import BeautifulSoup
import time
import json

# 编码问题
import sys
reload(sys)
sys.setdefaultencoding('utf8')

info = []
page = 1
def getpage():
    global page
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 '}
    url = 'http://www.budejie.com/video/'+str(page)
    html = requests.get(url,headers = headers)
    varl.set('获取第%s页视频'% (page))
    print ('获取第%s页视频'% (page))
    page = page+1
    #print html.status_code
    html.encoding = 'utf-8'

    ## 先抓大再抓小的策略
    url_contents = re.findall(r'<div class="j-r-list-c">(.*?)<div class="j-v-d-c',html.text,re.S)
    if url_contents:
        for i in url_contents:
            # print (type(i))  #tuple类型
            url_links = re.findall(r'data-mp4="(.*?)">',i,re.S)
            url_names = re.findall(r'<a href=.*?>(.*?)</a>',i,re.S)
            for name,link in zip(url_names,url_links):
                info.append([name,link])
                #print name,link

        # options:写入文件，以中文写入而不是以ascii/Unicode写入
        # with open('budejie.txt','a') as f:
        #     f.write(json.dumps(info,ensure_ascii=False))
        #     f.write('\n')
        #     f.close()
    return info


tt = 1
def write():
    global tt
    while tt<10:
        time.sleep(5)
        url_name = getpage()
        for i in url_name:
            # 视频下载
            # urllib.urlretrieve(i[1],'%s.mp4' % (i[0]).encode('gbk'))
            text.insert(END,str(tt)+'.'+i[1]+'\n'+i[0]+'\n')
            url_name.pop(0)
        tt = tt +1
    varl.set('抓取完毕')

def start():
    th = threading.Thread(target=write)
    th.start()

def main():
    root = Tk()
    root.title('test')
    root.geometry('+1000+400')
    global  text
    text = ScrolledText(root, font=('微软雅黑',10))
    text.grid()
    button = Button(root,text='开始爬取', font=('微软雅黑',10),command = start())
    button.grid()
    global varl
    varl = StringVar()

    label = Label(root, font=('微软雅黑', 10), fg='red',textvar=varl)
    label.grid()
    varl.set('已准备好...')
    root.mainloop()

main()
