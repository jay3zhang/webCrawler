#-*—coding:utf8-*-

#python2
import requests
import re
import urllib2
import urllib
#下面三行是编码转换的功能
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
        self.stories = []
        self.enable = False #程序是否继续运行
        
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/'+str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            #print type(pageCode)   #str
            return pageCode
        except:
            return ''
            
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败'
            return None
        pattern = re.compile('<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>(.*?)<div class="stats">.*?"number">(.*?)</i>.*?"number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            haveImg = re.search("img",item[2])
            if not haveImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR,"\n",item[1])
                pageStories.append([item[0],text,item[3],item[4]])
        return pageStories
      
    #缓存
    def loadPage(self):
        if self.enable == True:
            if len(self.stories)<2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex +=1
    #调用
    def getOneStory(self,pageStories,page):
        n = 0
        for story in pageStories:
            input = raw_input('')
            n+=1
            self.loadPage() #调用加载页面
            if input == 'Q':
                self.enable = False
                return 
            print u"第%d页\t第%d条\t发布人：%s\n%s" % (page,n,story[0],story[1])  
            print u"\n阅读量%s，评论%s条" % (story[2],story[3])
    
    def start(self):
        print u"正在读取糗事百科，回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        nowPage = 0 #控制当前读到第几页
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0] #删掉打印过的笑话
                self.getOneStory(pageStories,nowPage)
                
spider = QSBK()
spider.start()

                 