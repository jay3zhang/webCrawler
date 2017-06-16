# -*- coding: utf-8 -*-
##使用requests-bs4库

import requests
import bs4
from bs4 import BeautifulSoup
import re
#解决中文编码问题
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:
    def __init__(self,baseurl,seeLZ,floorTag):
        self.baseurl=baseurl
        self.seeLZ='?see_lz='+str(seeLZ)
        self.file=None
        self.floor=1
        self.floorTag=floorTag
        self.defaultTitle=u"百度贴吧"
        # HTML标签剔除工具类对象
        self.tool = Tool()
#获取帖子页面，换页
    def getpage(self,pagenum):
        try:
            url = self.baseurl + self.seeLZ + '&pn=' + str(pagenum)
            r = requests.get(url)
            html = BeautifulSoup(r.text,"html.parser")
            return html

        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u"连接百度贴吧失败，错误原因",e.reason
                return None
#获取帖子标题
    def getTitle(self):
        page=self.getpage(1)
        # print type(page)
        tag=page.h3
        title=tag['title']
        print title
        return title
#获取帖子页数
    def getPageNum(self):
        page=self.getpage(1)
        num=page.find_all(attrs={"class":"red"})
        pagenum=num[1].string
        return int(pagenum)
#获取帖子内容
    def getcontent(self):
        pagenum=self.getPageNum()+1
        contents=[]
        for num in range(1,pagenum):
            page = self.getpage(num)
            num = page.find_all('cc')
            for item in num:
                #content=item.get_text()
                content = "\n" + self.tool.replace(item.get_text()) + "\n"
                contents.append(content.encode('utf-8'))
        return contents
#写帖子标题
    def getFileTitle(self):
        title=self.getTitle()
        if title is not None:
            self.file=open(title+".txt","w+")
        else:
            self.file=open(self.defaultTitle+".txt","w+")
#写帖子内容
    def writeData(self):
        contents=self.getcontent()
        for item in contents:
            if self.floorTag =='1':
                floorLine='\n'+str(self.floor)+u'---------------------------------------------\n'
                self.file.write(floorLine)
            self.file.write(item)
            self.floor +=1

    def start(self):
        self.getFileTitle()
        pagenum=self.getPageNum()
        if pagenum == None:
            print "URL已失效，请重试"
            return
        try:
            print "该帖子共有"+str(pagenum)+"页"
            self.writeData()
        except IOError,e:
            print "写入异常，原因"+e.message
        finally:
            print "写入成功"

print u"请输入帖子代号"
baseurl = 'http://tieba.baidu.com/p/' + str(raw_input(u':>'))
#baseurl = 'http://tieba.baidu.com/p/3138733512'
seeLZ=raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag=raw_input("是否写入楼层信息，是输入1否输入0\n")
bdtb=BDTB(baseurl,seeLZ,floorTag)
bdtb.start()