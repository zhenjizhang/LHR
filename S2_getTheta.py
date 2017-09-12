# -*- coding: utf-8-*-
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import csv
import pandas as pd
import numpy as np
import sys

csv.field_size_limit(sys.maxsize)

#用来去标点
tokenizer = RegexpTokenizer(r'\w+')

#用来去a, the , of等无意义的词
en_stop = get_stop_words('en')

#原来找词的原型，比如likes-->like
p_stemmer = PorterStemmer()

#item-review全集文件
filename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/corpus_item_review_Video_Games.csv'

#item—theta文件 ——change K number
csvname = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/item_theta_Video_Games.csv'

#item-corpus文件，load lda model时候有用
icdcsvname = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/ic_dict_Video_Games.csv'

#dictionary文件地址
dictionaryfilename = '/Users/zhangzhenji/Desktop/BUPT/petitePaper/data/amazonReview/full/Video_Games/dictionary_Video_Games.dict'

#去每个item的review作为doc，形成集合docSet，返回docSet和item-reviewlist
def getDocSet(filename):
	docSet = []
	item_review_list = []
	with open(filename, 'rb') as csv_file:
		reader = csv.reader(csv_file)
		mydict = dict(reader)
	for k, v in mydict.items():
		i = [k, v]
		item_review_list.append(i)
		docSet.append(v)
	mydict = {}
	print 'done with getdocset'
	return docSet, item_review_list

#将docset中的每个doc进行tokennize，stop，stemmer处理，返回corpus和dictionary	
def ldapreclean(doc_set):
	texts = []
	for i in doc_set:
	    raw = i.lower()
	    tokens = tokenizer.tokenize(raw)
	    stopped_tokens = [i for i in tokens if not i in en_stop]
	    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
	    texts.append(stemmed_tokens)
	# turn our tokenized documents into a id <-> term（词） dictionary
	dictionary = corpora.Dictionary(texts)

	# convert tokenized documents into a document-term（词） matrix
	corpus = [dictionary.doc2bow(text) for text in texts]
	'''	>>> print(stemmed_tokens)
		['brocolli', 'good', 'eat', 'brother', 'like', 'eat', 'good', 'brocolli', 'mother']
		>>>dictionary = corpora.Dictionary(texts)
		>>>corpus = [dictionary.doc2bow(text) for text in texts]
		>>>print(corpus[0])
		[(0, 2), (1, 1), (2, 2), (3, 2), (4, 1), (5, 1)]	'''
		#(0,2) 0代表brocolli, 2代表出现了两次
	print 'done with ldaclean'
	return corpus, dictionary

#输出成item-theta文件
def getITcsv(csvname, ldamodel, item_review_list):
	with open(csvname, 'wb') as csv_file:
		writer = csv.writer(csv_file)
		for i in range(len(item_review_list)):
			print i
			item = item_review_list[i][0]
			theta = ldamodel.get_document_topics(corpus[i], minimum_probability=0, minimum_phi_value=None, per_word_topics=False)
			writer.writerow([item, theta])
	return 1

#获得item——corpus的dict
def getItemCorpusDict(item_review_list, corpus):
	item_corpus_dict = {}
	for i in range(len(item_review_list)):
		item = item_review_list[i][0]
		item_corpus_dict[item] = corpus[i]
	return item_corpus_dict

#输出item-corpus csv文件
def dict2csv(my_dict, csvname):
    with open(csvname, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in my_dict.items():
            writer.writerow([key, value])
    return 1

doc_set, item_review_list = getDocSet(filename)
corpus, dictionary = ldapreclean(doc_set)
# store dictionary to disk, for later use. use dictionary.load('fname') to load.
dictionary.save(dictionaryfilename)
#将corpus存成item-document dict方便之后使用
print 'dictionary already saved'
ic_dict = getItemCorpusDict(item_review_list, corpus)
dict2csv(ic_dict, icdcsvname)
print 'corpus already saved'

#训练lda model，传入corpus和dictionary，change K number
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=20)
#lda model保存 change K number
ldamodel.save('Video_Games_lda.model')
getITcsv(csvname, ldamodel, item_review_list)



lda = models.ldamodel.LdaModel.load('Video_Games_lda.model')








