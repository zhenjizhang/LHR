# -*- coding: utf-8-*-
import numpy as numpy
import csv
import sys
from scipy import sparse
import numpy as np
import math
from scipy.io import mmwrite
import random

#uij偏序全集
datafilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/u_i_j_uniform.csv'
#uij训练集
traindatafilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/train66_u_i_j_uniform.csv'
#uij测试集
testdatafilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/test33_u_i_j_uniform.csv'

#从文件取出三元组，返回三个list
def gettriples(filename):
	ele1 = []
	ele2 = []
	ele3 = []
	with open(filename, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for e1,e2,e3 in spamreader:
			ele1.append(e1)
			ele2.append(e2)
			ele3.append(e3)
	return ele1, ele2, ele3

#生成训练与测试样本
def generate_train_test_samples(ele1,ele2,ele3):
    #计算三个list长度，因为三个list长度相同，所以用其中一个list来计算即可
    #得到一个等长均匀list
    idxs = range(len(ele1))
    #随机重排这个list
    random.shuffle(idxs)
    train_list = []
    test_list = []
    triple_list = []
    #用此list为索引，取三个list的值，等于带约束随机重排了三个list
    for i in idxs:
    	list_tem = []
    	list_tem.append(ele1[i])
    	list_tem.append(ele2[i])
    	list_tem.append(ele3[i])
    	triple_list.append(list_tem)
    listlen = len(triple_list)
    #训练集个数
    traincnt = int(listlen * 0.66)
    #分训练集与测试集
    train_list = triple_list[:traincnt]
    test_list = triple_list[traincnt:]
    return train_list, test_list

#三元组输出至csv文件
def trilist2csv(trilist, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for e1, e2, e3 in trilist:
           writer.writerow([e1, e2, e3])
    return 1

ele1, ele2, ele3 = gettriples(datafilename)
train_list, test_list = generate_train_test_samples(ele1,ele2,ele3)
print len(train_list),len(test_list)
trilist2csv(train_list, traindatafilename)
trilist2csv(test_list, testdatafilename)







