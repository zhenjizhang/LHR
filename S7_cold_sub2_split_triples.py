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
traindatafilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/train66_cold_u_i_j_uniform.csv'
#uij测试集
testdatafilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/test33_u_i_j_uniform.csv'
#items_id.csv生成cold_item
itidname = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/items_id.csv'

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
def generate_train_test_cold_samples(ele1,ele2,ele3,cold_item_list):
    #计算三个list长度，因为三个list长度相同，所以用其中一个list来计算即可
    #得到一个等长均匀list
    idxs = range(len(ele1))
    #随机重排这个list
    random.shuffle(idxs)
    train_list = []
    test_list = []
    triple_list = []
    train_cold_list = []
    test_cold_list = []
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
    print 'train_list',len(train_list)
    print 'cold in train',len(cold_item_list)
    # print cold_item_list
    test_list = triple_list[traincnt:]
    
    for i in range(len(train_list)):
        if train_list[i][1] not in cold_item_list:
            if train_list[i][2] not in cold_item_list:
                # print train_list[i][1],train_list[i][2]
                train_cold_list.append(train_list[i])
            else:
                # print 'c2:',int(train_list[i][2])
                continue
        else:
            # print 'c1:',int(train_list[i][1])
            continue

    for i in range(len(test_list)):
        if test_list[i][1] not in cold_item_list:
            if test_list[i][2] not in cold_item_list:
                # print train_list[i][1],train_list[i][2]
                test_cold_list.append(test_list[i])
            else:
                # print 'c2:',int(train_list[i][2])
                continue
        else:
            # print 'c1:',int(train_list[i][1])
            continue
    print 'train',len(train_list),'train_d_cold',len(train_cold_list),'test',len(test_list), 'test_d_cold',len(test_cold_list)
    return train_cold_list, test_list

#生成cold_item_list

def getColdItemList(itidname):
    cold_item_list = []
    item_list = []
    with open(itidname, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for items, itid in spamreader:
            item_list.append(itid)
    print 'itemlist',len(item_list) 
    n = len(item_list)
    print len(item_list)
    random.shuffle(item_list)
    cn = n * 0.2
    cn = int(cn)
    cold_item_list = item_list[:cn]
    print 'cold',len(cold_item_list)
    return cold_item_list

#三元组输出至csv文件
def trilist2csv(trilist, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for e1, e2, e3 in trilist:
           writer.writerow([e1, e2, e3])
    return 1

cold_item_list = getColdItemList(itidname)
ele1, ele2, ele3 = gettriples(datafilename)
train_cold_list, test_list = generate_train_test_cold_samples(ele1,ele2,ele3,cold_item_list)
print len(train_cold_list),len(test_list)

np.save("cold_item_list.npy",np.array(cold_item_list))

trilist2csv(train_cold_list, traindatafilename)
trilist2csv(test_list, testdatafilename)

