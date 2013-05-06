'''
Created on Apr 12, 2013

@author: MiguelAngel
'''
from gensim import corpora,models,similarities
import time
import util

'''Parameters'''
numOfTopics=300
n=1
lemmatize='yes'
removeStopwords='yes'
lowerCase='yes'
other='yes'
lang='en'
'''end Parameters'''

t1=time.time()

doc1=r'D:\CIC\Research visit Greece\pan-plagiarism-corpus-2011\external-detection-corpus\source-document\source-document00178.txt'
doc2=r'D:\CIC\Research visit Greece\pan-plagiarism-corpus-2011\external-detection-corpus\suspicious-document\suspicious-document00005.txt'

#Reading files
text1=open(doc1,'rU').read()
text2=open(doc2,'rU').read()

#Extracting features
features1=util.NGrams(util.PreProcesser(util.Tokenizer(text1),lemmatize,removeStopwords,lowerCase,other),n,'yes')
features2=util.NGrams(util.PreProcesser(util.Tokenizer(text2),lemmatize,removeStopwords,lowerCase,other),n,'yes')
print 'Source sentences:',len(features1)
print 'Suspiciou sentences',len(features2)

#Loading models
dict=corpora.Dictionary.load('models/plagdict.dict')
tfidfmodel=models.TfidfModel.load('models/tfidfmodel.tfidf')
lsimodel=models.LsiModel.load('models/lsamodel.lsi')

#Calculating similarities
index=[]
for i,feaA in enumerate(features1):
    #print i,
    if len(feaA)==0:
        continue
    lsi1=lsimodel[tfidfmodel[dict.doc2bow(feaA)]]
    #print 'building index'
    sim=similarities.MatrixSimilarity([lsi1])
    for j,feaB in enumerate(features2):
        #print j
        if len(feaB)==0:
            continue
        #Generating vectors
        lsi2=lsimodel[tfidfmodel[dict.doc2bow(feaB)]]
        value=sim[lsi2][0]
        if value>0.75:
            index.append((i,j,value))
print index
print len(index)

for i,j,k in index:
    print features1[i]
    print lsimodel[tfidfmodel[dict.doc2bow(features1[i])]]
    print features2[j]
    print lsimodel[tfidfmodel[dict.doc2bow(features2[j])]]
    break

t2=time.time()
print t2-t1