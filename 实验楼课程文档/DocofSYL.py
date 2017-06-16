# coding:utf-8
import requests
from bs4 import BeautifulSoup

# 使用cookie模拟登录实验楼，下载课程文档
# cookie 长字符文本，中间元素太多，用'''…'''比较好
cookie = yourCookie
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'Connection': 'keep-alive',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Cookie': cookie}

# 爬取实验楼python3简明教程的所有文档，分析文档的url，
# 可知该课程的文档从"/courses/596/labs/2036/document"到"/courses/596/labs/2054/document"
for page in range(2036,2054+1):
    #用一个for循环改变url
    url = 'https://www.shiyanlou.com/courses/596/labs/{}/document'.format(page)
   
    try:
        r = requests.get(url,headers=header)
        #print(r.status_code)  #检查连接状态，200为正常
        r.encoding = 'utf-8'
        data = r.text
        soup = BeautifulSoup(data,'lxml')
        # print(soup)
    except:
        print('error')

    title = soup.find('title').string   #对应的标签只有一个
    # page为int，后面是str，不能用+连接，可以用逗号分隔
    print (page,':'+title)

    text = soup.find('textarea',id = "editor")  ##对应的id只有一个

    with open(title+'.md','w',encoding='utf-8') as f:
        # 分析网页，文档以markdown格式编写，所以保存为.md文件，
        # 以文章的标题title为文件名，win上用markdownpad打开就可以看到和网页上一样的效果
        # 指定utf-8编码，默认使用gbk，会出错
        # 'w' 格式写入str，'wb' 格式写入byte
        f.write(str(text.string))
        f.close()