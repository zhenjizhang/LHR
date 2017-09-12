# -*- coding: utf-8-*-
import numpy as np
from math import exp
import random
import sys
from scipy.io import mmread
from scipy import sparse
import csv

#U_I_J(全id)偏序对
fliename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/u_i_j_uniform.csv'

#偏序对生成算法评分（4，5）正例，评分（1，2，3）负例，笛卡尔积生成偏序集
def generate_samples(data):
	num_users_n,wew = data.shape
	print data.shape
	u_i_j = []
	for user_i in xrange(num_users_n):
		item_list = data[user_i].indices
		# print 'itemlist',item_list
		rating_list = data[user_i].data
		# print 'rating_list',rating_list
		i = 0
		# print '---',len(item_list)
		pos_list = []
		neg_list = []
		while i < len(item_list):
			#如果评分大于3，加入user_i的正例集pos_list
			if(rating_list[i]>3):
				pos_list.append(item_list[i])
			#如果评分小于3，加入user_i的正例集neg_list
			else:
				neg_list.append(item_list[i])
			i += 1
		#两个集合做笛卡尔积，生成uij偏序对
		for k in xrange(len(pos_list)):
			for g in xrange(len(neg_list)):
				u_i_j.append([user_i,pos_list[k],neg_list[g]])
	return u_i_j

def uij2csv(uijlist, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for u, i, j in uijlist:
           writer.writerow([u, i, j])
    return 1

data = mmread("uir_sparse_mat_Video_Games.mtx").tocsr()
u_i_j = generate_samples(data)
print len(u_i_j)
uij2csv(u_i_j,fliename)
