# -*- coding: utf-8-*-
import numpy as numpy
import csv
import sys
from scipy import sparse
import numpy as np
import math
from scipy.io import mmwrite

#item-id文件
itemidfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/items_id.csv'
#user-id文件
useridfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/users_id.csv'
#item—user-rating文件
datafilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/item_user_rating_Video_Games.csv'

def csv2dict(csvname):
    with open(csvname, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)
    return mydict

#用itemID和userID替换item-user-rating文件中的item和user名称，并存入稀疏矩阵中
def getSparseDataMat(item_id_dict, user_id_dict, filename):
	item = []
	user = []
	rating = []
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for i,u,r in spamreader:
			item.append(int(item_id_dict[i]))
			user.append(int(user_id_dict[u]))
			rating.append(float(r))
		print len(user_id_dict),len(item_id_dict)
	#coo适用于存三元组数据，但是csr可以做切分
	c = sparse.coo_matrix((rating,(user,item)), shape = (len(user_id_dict), len(item_id_dict))).tocsr()
	print c.shape
	return c

item_id_dict = csv2dict(itemidfilename)
user_id_dict = csv2dict(useridfilename)

#得到稀疏矩阵csr
csr = getSparseDataMat(item_id_dict,user_id_dict,datafilename)
#将csr矩阵保存
mmwrite('uir_sparse_mat_Video_Games',csr)



# row = [1,3]
# col = [3,4]
# data = [1,2]
# c = sparse.coo_matrix((data, (row, col)), shape=(6, 6))
# print c.col, c.row, c.data
# print c.toarray()