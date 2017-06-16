#-*—coding:utf8-*- 
#糗事百科，发布人，笑话内容，去除有图片的笑话
# python2
import requests
import re
#下面三行是编码转换的功能
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#hea是我们自己构造的一个字典，里面保存了user-agent
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}

html = requests.get('http://www.qiushibaike.com/hot/page/3',headers = hea)
html.encoding = 'utf-8' #这一行是将编码转为utf-8否则中文会显示乱码。

story = re.findall('<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>(.*?)<div class="stats">'+
                   '.*?<i class="number">(.*?)</i> 好笑.*?class="number">(.*?)</i> 评论'+
                   '.*?class="up">.*?class="number hidden">(.*?)</span>.*?class="down">.*?class="number hidden">(.*?)</span>',html.text,re.S)
######  (.*?)处不能为空; 每个(.*?)对应一个元素，依次为：
# 发布者，内容，图片链接，好笑数，评论数，up数，down数（up数-down数=好笑数）

count=1
for item in story:
    haveImg = re.search("img",item[2])
    if not haveImg:
        replaceBR = re.compile('<br/>')
        text = re.sub(replaceBR, "\n", item[1])
        print count,item[0]
        print text
        print item[5]+'up'+'\t'+item[6]+'down'+'\t'+item[3]+'好笑'+'\t'+item[4]+'评论'
        print "*****************"
        count=count+1



