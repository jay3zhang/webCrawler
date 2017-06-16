from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
import json
from bs4 import BeautifulSoup
import re
import pymongo
import os
from hashlib import md5
from multiprocessing import Pool
# module define by self
from config import *

client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]

def get_page_index(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    #请求json格式的文件
    url = 'http://www.toutiao.com/search_content/?'+ urlencode(data)
    # print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except:  #RequestException:
        print("请求索引页出错")
        return ''

def parser_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except:
        pass

def get_page_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except: #RequestException:
        print("请求详情页出错")
        return ''

def parser_page_details(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    images_pattern = re.compile('var gallery = (.*?);',re.S)
    result = re.search(images_pattern,html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongodb成功')
        return True
    return False

def download_image(url):
    print('正在下载：',url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        #return response.text
        save_image(response.content)
    except RequestException:
        print("请求图片出错")
        return ''

def save_image(content):
    ##用md5值命名文件，兼带有去重的功能
    file_path = '{0}/{1}.{2}'.format(os.getcwd()+'/picture',md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):     #检查文件是否存在
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main():
    html = get_page_index(0,KEYWORD)
    for url in parser_page_index(html):
        html = get_page_details(url)
        if html:
            result = parser_page_details(html,url)
           # if result:     #mongodb配置有些问题，先放下
                # save_to_mongo(result)


if __name__ == '__main__' :
    #改进的地方：加个延时 sleep(1)
    groups = [x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool = Pool()
    pool.map(main(),groups)