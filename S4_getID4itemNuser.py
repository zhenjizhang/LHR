# -*- coding: utf-8-*-
import numpy as numpy
import csv
import sys
from scipy import sparse

#item 集合
itemfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/items.csv'
#user 集合
userfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/users.csv'
id_item_filename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/id_items.csv'
id_user_filename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/id_users.csv'
item_id_filename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/items_id.csv'
user_id_filename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/users_id.csv'

def getIDaskey(filename):
	temdict = {}
	i = 0
	with open(filename) as csvfile:
		csvreader = csv.reader(csvfile)
		for on in csvreader:
			temdict[i] = on[0] 
			i = i + 1
		return temdict

def dict2csv(my_dict, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in my_dict.items():
            writer.writerow([key, value])
    return 1

#dict value在前key在后存入csv文件
def dict2convertcsv(my_dict, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in my_dict.items():
            writer.writerow([value, key])
    return 1

id_item_dict = getIDaskey(itemfilename)
id_user_dict = getIDaskey(userfilename)
dict2csv(id_item_dict,id_item_filename)
dict2csv(id_user_dict,id_user_filename)

dict2convertcsv(id_item_dict,item_id_filename)
dict2convertcsv(id_user_dict,user_id_filename)