#!/usr/bin/env python
# coding=utf-8

import re
import urllib2
from time import sleep

import sys
import xlwt

reload(sys)
sys.setdefaultencoding('utf8')

excel_name = "g://python//data_clect.xls"
excel_name2 = "g://python//data_med.xls"

half_url_dict2 = {'综合排行': 'rnk_1_0_0', '声誉排行': 'rnk_1_0_1', '学术资源排行': 'rnk_1_0_2',
                     '学术成果排行': 'rnk_1_0_3', '学生情况排行': 'rnk_1_0_4', '教师资源排行': 'rnk_1_0_5',
                     '物资资源排行': 'rnk_1_0_6', '医药类': 'rnk_2_5_0'}

half_url_dict1 = {'综合类院校': 'rnk_2_1_0', '理工类院校': 'rnk_2_2_0', '农林类院校': 'rnk_2_3_0',
                     '医药类院校':'rnk_2_5_0', '师范类院校': 'rnk_2_6_0', '语言类院校': 'rnk_2_7_0',
                     '财经类院校': 'rnk_2_8_0', '政法类院校': 'rnk_2_9_0', '体育类院校': 'rnk_2_10_0',
                     '艺术类院校': 'rnk_2_11_0', '民族类院校': 'rnk_2_12_0'}
medicine_url_dict = {'综合排行': 'rnk_2_5_0', '声誉排行': 'rnk_2_5_1', '学术资源排行': 'rnk_2_5_2',
                     '学术成果排行': 'rnk_2_5_3', '学生情况排行': 'rnk_2_5_4', '教师资源排行': 'rnk_2_5_5',
                     '物资资源排行': 'rnk_2_5_6'}
					 

book = xlwt.Workbook(encoding='utf-8')
book2 = xlwt.Workbook(encoding='utf-8')
'''
for half_url_key3 in medicine_url_dict:
	file_name2 = "g://python//med_rnk//%s.txt" % medicine_url_dict[half_url_key3]
		
	file_med = open(file_name2)
	line_med = file_med.readline()

	rnk_name  = line_med
	print rnk_name
	
	sheet2 = book2.add_sheet(rnk_name)
	
	row_med = 0
	while line_med:
		line_med = file_med.readline()
		row_med = row_med + 1
		col_med = 0
		list_med = line_med.split('\t')
		for word_med in list_med:
				word_replace2 = word_med.replace("↔","0")
				word_replace2 = word_replace2.replace("↓","-")
				word_replace2 = word_replace2.replace("↑","+")
				col_med = col_med +1
				sheet2.write(row_med,col_med,word_replace2)
				
book2.save(excel_name2)
file_med.close()
'''


for half_url_key2 in half_url_dict2:
        filename_data = "g://python//%s.txt" % half_url_dict2[half_url_key2]
		
        file = open(filename_data)
	line = file.readline()
	rank_name = line
	print rank_name
	line = file.readline()
	sheet = book.add_sheet(rank_name)
	row = 0
	while line:
		line = file.readline()
		#print line
		list = line.split('	')
		if(line):
			sch_name = list[1]
			#print line
			for half_url_key1 in half_url_dict1:
        			filename_sort = "g://python//class//%s.txt" % half_url_dict1[half_url_key1]
				file_sort = open(filename_sort)
				line2 = file_sort.readline()
				find = 0
				sort_name = line2
				#print sort_name
				while line2:
					line2 = file_sort.readline()
					if line2:
						#print line2
						if (cmp(line2,sch_name+'\n') == 0):
							line = line.strip('\n')
							line = line  + "\t" + sort_name
							find = 1
							break
					
				if (find == 1):
					break
			#print line
			row = row +1
			col = 0
			list = line.split('\t')
			for word in list:
				word_replace = word.replace("↔","0")
				word_replace = word_replace.replace("↓","-")
				word_replace = word_replace.replace("↑","+")
				'''
				if (word.find("↑") == 0):
					print word
					word_replace = word.replace("↑","+")
					print word_replace
				'''
				col = col +1
				sheet.write(row,col,word_replace)
book.save(excel_name)		
			
file.close()
