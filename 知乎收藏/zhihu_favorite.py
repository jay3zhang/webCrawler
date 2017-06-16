# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.zhihu.com/collection/27109279?page=1'
hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
r = requests.get(url,headers=hea)
r.raise_for_status()
soup = BeautifulSoup(r.text,"html.parser")
All = soup.find_all(attrs={'class':["zm-item-title","content"]})

f = open('zhihu.txt','w')
for each in All:
    if (each.name == 'h2'):
        if (each.a is None):
            f.write('')
        elif each.a.string:
            f.write('问题：'+each.a.string+'\n')
        else:
            f.write('无内容')
    else:
        if each.name=='textarea':
            if each.get_text():
                x = each.get_text()
                removeImg = re.compile('<img.*?>| {7}|')
                replaceBR = re.compile('<br><br>|<br>')
                x = re.sub(removeImg, "", x)
                x = re.sub(replaceBR, "\n", x)
                f.write('回复：'+x.strip()+'\n'+'-----------------------'+'\n')
            else:
                f.write('无内容')

f.close()


