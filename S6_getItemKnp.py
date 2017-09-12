# -*- coding: utf-8-*-
import csv
import numpy as np

#item-id文件
itemidfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/items_id.csv'
#item-主题分布文件
itemThetafilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/item_theta_Video_Games.csv'

def csv2dict(csvname):
    with open(csvname, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)
    return mydict

#将原来的item-theta中的item名称换为itemID表示
def getitemKdict(item_id_dict, filename):
	item_K = {}
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for i,K in spamreader:
			K = eval(K)
			item_K[int(item_id_dict[i])] = K
	return item_K

def getitemKnp(item_K_dict, K):
	item_K_list = []
	tem_list = []
	for i in range(len(item_K_dict)):
		for j in range(5):
			tem_list.append(item_K_dict[i][j][1])
		item_K_list.append(tem_list)
		tem_list = []
	return item_K_list

K = 5
item_id_dict = csv2dict(itemidfilename)
item_K_dict = getitemKdict(item_id_dict, itemThetafilename)
ikl = getitemKnp(item_K_dict, K)
item_K_list_np = np.array(ikl)

#保存为np数组
np.save("item_K_list_np.npy",item_K_list_np)

# a = np.load("item_K_list_np.npy")
# print a[45139]
# print type(a)

# print item_K_list_np[45139]
# print type(item_K_list_np)

# print item_id_dict['B00122P5P0']
# print ikl[45139]

