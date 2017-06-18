#!/usr/bin/env python
# coding=utf-8

import re
import urllib2
from time import sleep

import sys
reload(sys)
sys.setdefaultencoding('utf8')

main_url = 'http://rank2013.netbig.com'


def parse():
    #所有分类名字和url后半段的dict
    half_url_dict = {'综合类院校': 'rnk_2_1_0', '理工类院校': 'rnk_2_2_0', '农林类院校': 'rnk_2_3_0',
                     '医药类院校':'rnk_2_5_0', '师范类院校': 'rnk_2_6_0', '语言类院校': 'rnk_2_7_0',
                     '财经类院校': 'rnk_2_8_0', '政法类院校': 'rnk_2_9_0', '体育类院校': 'rnk_2_10_0',
                     '艺术类院校': 'rnk_2_11_0', '民族类院校': 'rnk_2_12_0'}
    for half_url_key in half_url_dict:
        url = "%s/%s" % (main_url, half_url_dict[half_url_key])
        #分类学校的文件名,绝对路径. 文件名为url后半段
        filename = "/home/long/Documents/rank2013/classesification/%s.txt" % half_url_dict[half_url_key]
        file = open(filename, 'w')
        #分类名称
        file.write("%s\n\n" % half_url_key)
        #只爬取了分类排行中的综合学校名称
        parse_classesification(url, file)
        #如果要爬取声誉,学术资源排行等学校则取消此段注释
        '''sort_classesification = parse_sort_rules(url)
        for sec_url in sort_classesification:
            url = "%s/%s" % (main_url, sec_url)
            parse_classesification(url, file)
        '''
        file.close()
        sleep(10)

#获得分类院校的内容
def parse_classesification(url, file):
    #获得第一页学校名称
    parse_page(url, file)
    #如果有分页,则获得分页的url
    paging_list = parse_paging_url(url)
    for paging_url in paging_list:
        url = "%s/%s" % (main_url, paging_url)
        #爬取当页学校名称
        parse_page(url, file)

#获得某个排行的分页url(以防有分页)
def parse_paging_url(url):
    content = urllib2.urlopen(url).read()
    paging_list = re.findall(r'<li><a href=\"/(rnk_\d_\d_\d_\d)/\">.+</a></li>', content)
    if paging_list:
        return paging_list
    else:
        return list()

#获得声誉排行,学术资源排行........的url
def parse_sort_rules(url):
    content = urllib2.urlopen(url).read()
    sort_classesification = re.findall(r'<a href=\"/(rnk_\d_\d_\d)/\">.+?</a>', content)
    return sort_classesification

#获得某页的所有学校名
def parse_page(url, file):
    content = urllib2.urlopen(url).read()
    #python 正则匹配到学校信息的所有字符串列表, 相关文章url: nidong.de
    rank_list = re.findall(r'<div class=\"mtky( | mhbg)\">(.+?)<div class=\"clear\">', content, re.S)
    if rank_list:
        for school in rank_list:
            school = school[1]
            school_name_list = re.findall(r'target=\'_blank\'>(.+?)</a></li>', school)
            if school_name_list:
                #rank id
                school_name = school_name_list[0]
                file.write("%s\n" % school_name)

#程序入口
if __name__ == '__main__':
    parse()
