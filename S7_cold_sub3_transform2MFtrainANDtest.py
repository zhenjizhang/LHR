import numpy as np
from math import exp
import random
import sys
from scipy.io import mmread
import csv

data = mmread("uir_sparse_mat_Video_Games.mtx").tocsr()
train_u_i_j_csvfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/train66_cold_u_i_j_uniform.csv'
test_u_i_j_csvfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/test33_u_i_j_uniform.csv'
user_item_rating_train_csvfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/train66_cold_MF_u_i_r.csv'
user_item_rating_test_csvfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/test33_MF_u_i_r.csv'

def csv2dict(csvname):
	mydict = {}
	with open(csvname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for e1,e2,e3 in spamreader:
			e1 = int(e1)
			e2 = int(e2)
			e3 = int(e3)
			tem_list = [e2,e3]
			if e1 in mydict:
				mydict[e1].append(e2)
				mydict[e1].append(e3)
			else:
				mydict[e1] = tem_list
	return mydict

def list2csv(tripleslist, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for e1, e2, e3 in tripleslist:
           writer.writerow([e1, e2, e3])
    return 1

def generate_samples(data, u_ij_dict):
	uir = []
	for user,ij in u_ij_dict.items():
		ij = list(set(ij))
		for item in ij:
			rating = data[user].toarray()[0][item]
			uir.append([user,item,rating])
	return uir

train_u_ij_dict = csv2dict(train_u_i_j_csvfilename)
print 'csv already read'
train_uir = generate_samples(data, train_u_ij_dict)
print 'already done generate samples'
list2csv(train_uir, user_item_rating_train_csvfilename)
print 'already loaded in csv'

test_u_ij_dict = csv2dict(test_u_i_j_csvfilename)
print 'csv already read'
test_uir = generate_samples(data, test_u_ij_dict)
print 'already done generate samples'
list2csv(test_uir, user_item_rating_test_csvfilename)
print 'already loaded in csv'

