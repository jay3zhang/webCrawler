#!/usr/bin/env python
# coding=utf-8

import re
import urllib2
from time import sleep
from os import makedirs

import sys
reload(sys)
sys.setdefaultencoding('utf8')

main_url = 'http://rank2013.netbig.com'

def parse():
    #所有综合学校分类名称和url后半段
    compre_url_dict = {'综合排行': 'rnk_1_0_0', '声誉排行': 'rnk_1_0_1', '学术资源排行': 'rnk_1_0_2',
                     '学术成果排行': 'rnk_1_0_3', '学生情况排行': 'rnk_1_0_4', '教师资源排行': 'rnk_1_0_5',
                     '物资资源排行': 'rnk_1_0_6'}
    #药类
    medicine_url_dict = {'综合排行': 'rnk_2_5_0', '声誉排行': 'rnk_2_5_1', '学术资源排行': 'rnk_2_5_2',
                     '学术成果排行': 'rnk_2_5_3', '学生情况排行': 'rnk_2_5_4', '教师资源排行': 'rnk_2_5_5',
                     '物资资源排行': 'rnk_2_5_6'}
    all_url_list = {'compre': compre_url_dict, 'medicine': medicine_url_dict}

    #综合分类数据文件夹
    comprehensive_rank_dir = "Rank_Data/Comprehensive_Rank"
    makedirs(comprehensive_rank_dir)
    #药类单独一个文件夹
    medicine_rank_dir = "Rank_Data/Medicine_Rank"
    makedirs(medicine_rank_dir)
    
    for rank_categories, tail_url_dict in all_url_list.items():
        for rank_name, tail_url in tail_url_dict.items():
            url = "%s/%s" % (main_url, tail_url)
            if rank_categories == 'compre':
                filename = "%s/%s.txt" % (comprehensive_rank_dir, tail_url_dict[rank_name])
            else:
                filename = "%s/%s.txt" % (medicine_rank_dir, tail_url_dict[rank_name])
            file = open(filename, 'w')
            #第一行为分类名称
            file.write("%s\n\n" % rank_name)
            
            #爬取第一页学校信息
            parse_page(url, file)
            #爬取当前分类中的分页url
            paging_list = parse_paging_url(url)
            for paging_url in paging_list:
                url = "%s/%s" % (main_url, paging_url)
                #解析当前url页的学校信息
                parse_page(url, file)
            file.close()
            sleep(10)
'''
    for half_url_key in half_url_dict:
        #保存信息的文件绝对路径,文件名为url后半段
        url = "%s/%s" % (main_url, half_url_dict[half_url_key])
        filename = "%s/%s.txt" % (comprehensive_rank_dir, half_url_dict[half_url_key])
        file = open(filename, 'w')
        #第一行为分类名称
        file.write("%s\n\n" % half_url_key)
        #爬取第一页学校信息
        parse_page(url, file)
        #爬取当前分类中的分页url
        paging_list = parse_paging_url(url)
        for paging_url in paging_list:
            url = "%s/%s" % (main_url, paging_url)
            #解析当前url页的学校信息
            parse_page(url, file)
            sleep(5)
        file.close()
        sleep(10)
'''
#爬取当前分类中的分页url后半段
def parse_paging_url(url):
    content = urllib2.urlopen(url).read()
    paging_list = re.findall(r'<li><a href=\"/(rnk_\d_\d_\d_\d)/\">.+</a></li>', content)
    if paging_list:
        return paging_list
    else:
        return list()

#获取当前url页的学校的得分信息
def parse_page(url, file):
    content = urllib2.urlopen(url).read()
    rank_list = re.findall(r'<div class=\"mtky( | mhbg)\">(.+?)<div class=\"clear\">', content, re.S)
    if rank_list:
        #filename = "/home/long/Documents/rank2013/%s.txt" % half_url_dict[half_url_key]
        for school in rank_list:
            school = school[1]
            #获得学校名称列表
            school_name_list = re.findall(r'target=\'_blank\'>(.+?)</a></li>', school)
            if school_name_list:
                #rank id排名
                school_name = school_name_list[0]
                school_rank_id_list = re.findall(r'mtky_n_t_no float_l f.*0\">(\d+?)</li>', school)
                #如果没有,则和上一次的排名一样.
                if school_rank_id_list:
                    school_rank_id = int(school_rank_id_list[0])
                #学校总得分
                school_final_score_list = re.findall(r'<li class=\"float_l facearial f14 f.+? fbold left pl14">(.+?)</li>', school)
                if school_final_score_list:
                    school_final_score = school_final_score_list[0]
                else:
                    #没有则特殊标记为-1000,再处理
                    school_final_score = -1000
                #排名变化情况字符串
                rank_change = re.findall(r'<font.*>(.+?)</font></li>', school)
                if not rank_change:
                    rank_change = ' '
                else:
                    rank_change = rank_change[0]
                    rank_change = rank_change.replace('&nbsp;', '')
                #相信得分的总字符串列表
                score_list = re.findall(r'class=\"mtkgh\">.+<ul>(.+?)</ul>.+</div>', school, re.S)
                score_list_str = score_list[0]
                #score_list = re.findall(r'<li>.+<br />(.+?)</li>', score_list_str)
                #匹配每个得分项
                score_list = re.findall(r'<li>.+<br />(.+?)</li>', score_list_str)
                #如果当前子得分项的html中li有css 的 width, 则匹配
                if not score_list:
                    score_list = re.findall(r'<li style=\"width:\d+px;\">.+<br />(.+?)</li>', score_list_str)
                if not score_list:
                    #没有找到子得分项则报错
                    print 'get score list failed!'
                    print 'url: %s' % url
                    print score_list_str
                    print school_rank_id
                    print school_name
                    sleep(20)
                else:
                    score_str = '\t'.join(score_list)
                rank_str = "%s\t%s\t%s\t%s\t%s\n" % (school_rank_id, school_name, school_final_score, rank_change.encode('utf-8'), score_str)
                file.write(rank_str)

#parse_rank_page()
#parse_paging_url('http://rank2013.netbig.com/rnk_1_0_0')
#程序入口
if __name__ == '__main__':
    parse()
