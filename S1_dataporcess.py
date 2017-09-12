# -*- coding: utf-8-*-
import numpy as np
import pandas as pd
import csv
import re

#原始数据
file = "/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/reviews_Video_Games.json"

#json变dataframe的数据
df_file = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/dataFrame_Video_Games.csv'

#item——user——rating——review的datafram数据
orginal_file = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/orginal_dataFrame_Video_Games.csv'

#每个item下有全部对该item有交互的user的review数据的item-review集合
corpus_file = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/corpus_item_review_Video_Games.csv'

#item-user-rating的dataframe数据
iur_df_flie = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/item_user_rating_dataFrame_Video_Games.csv'

#item-user-rating的list2csv数据
iur_flie = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/item_user_rating_Video_Games.csv'

#eval 去单引号，parse用来取json文件每一行
def parse(path):
    f = open(path,'rb')
    for l in f:
        yield eval(l)

#将原始数据存成pandas数据
def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient = 'index')

#得到item——review数据
def getcorpus(dafr):
    item = {}
    n = np.shape(dafr)[0]
    for i in range(n):
        asin = dafr.at[i,"asin"]
        reviewText = dafr.at[i,"reviewText"]
        if asin in item:
            item[asin] = item[asin] + " " + reviewText
        else:
            item[asin] = reviewText
        print i
    return item

#去掉html，tags
def replaceCharEntity(htmlstr):
  CHAR_ENTITIES={'nbsp':' ','160':' ',
        'lt':'<','60':'<',
        'gt':'>','62':'>',
        'amp':'&','38':'&',
        'quot':'"','34':'"',}
   
  re_charEntity=re.compile(r'&#?(?P<name>\w+);')
  sz=re_charEntity.search(htmlstr)
  while sz:
    entity=sz.group()
    key=sz.group('name')
    try:
      htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
      sz=re_charEntity.search(htmlstr)
    except KeyError:
      htmlstr=re_charEntity.sub('',htmlstr,1)
      sz=re_charEntity.search(htmlstr)
  return htmlstr

#将dict存成csv
def dict2csv(my_dict, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in my_dict.items():
            value = replaceCharEntity(value)
            writer.writerow([key, value])
    return 1

#将csv读出成dict
def csv2dict(csvname):
    with open(csvname, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)
    return mydict

#从pandas datafram中，读出item_user_rating数组
def getiurlist(dafr):
    n = np.shape(df)[0]
    iur_list = []
    for i in range(n):
        asin = dafr.at[i, 'asin']
        reviewerID = dafr.at[i, 'reviewerID']
        overall = dafr.at[i, 'overall']
        t = (asin, reviewerID, overall)
        iur_list.append(t)
        print "iur ",i
    return iur_list

#将iur——list存成csv
def iur2csv(iurlist, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for i, u, r in iurlist:
           writer.writerow([i, u, r])
    return 1

df = getDF(file)
df.to_csv(df_file)

orginal_df = df.loc[:,['asin','reviewerID','overall','reviewText']]
print orginal_df
orginal_df.to_csv(orginal_file)

print np.shape(orginal_df)
item_corpus = getcorpus(orginal_df)
# print item_corpus['B00122P5P0']
# print item_corpus['B004P7UIRO']
dict2csv(item_corpus, corpus_file)

iur_df = df.loc[:,['asin', 'reviewerID', 'overall']]
df.to_csv(iur_df_flie)

iur_list = getiurlist(iur_df)
iur2csv(iur_list, iur_flie)