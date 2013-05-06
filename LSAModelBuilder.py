'''
Created on Apr 12, 2013
Generates and saves a gensim lsa model for further use based in the corpuDir (all *.txt documents in the folder)
@author: MiguelAngel
'''
from gensim import models,corpora
import time
import util
import pan2011corpus_util
from nltk.corpus import wordnet as wn

######### MAIN ########
'''Parameters'''
numOfTopics=300
n=1
lemmatize='yes'
removeStopwords='yes'
lowerCase='yes'
other='yes'
lang='en'
wordnetDictionary='yes'
'''end Parameters'''

t0=time.time()
print 'Getting filenames .....'
corpusDir='D:/CIC/Research visit Greece/pan-plagiarism-corpus-2011/external-detection-corpus/source-document/'
pan=pan2011corpus_util.pan2011corpus(corpusDir)
filenames=pan.fn_per_lang(lang)
print 'Total of files:',len(filenames)
print 'Done!\t',
t1=time.time()
print 'Time:',t1-t0
'''
print 'Generating dictionary .....'
dictionary=corpora.Dictionary([list(wn.all_lemma_names())])
print 'Dictionary length: ',len(dictionary)
print 'Done!\t',
t2=time.time()
print 'Time:',t2-t1
'''
print 'Generating dictionary .....'
dictionary=util.DictionaryGenerator(corpusDir, filenames[:1000],n,lemmatize,removeStopwords,lowerCase,other,wordnetDictionary)
dictionary.save('models/plagdict.dict')
print 'Dictionary length: ',len(dictionary)
print 'Done!\t',
t2=time.time()
print 'Time:',t2-t1

print 'Generating tfidf model .....'
corpus=util.MyCorpus(dictionary,corpusDir,filenames[:1000],n,lemmatize,removeStopwords,lowerCase,other,wordnetDictionary)
tfidfModel=models.TfidfModel(corpus)
tfidfModel.save('models/tfidfmodel.tfidf')
print 'Done!\t',
t3=time.time()
print 'Time:',t3-t2
print 'Generating lsa model .....'
lsaModel=models.LsiModel(tfidfModel[corpus],num_topics=numOfTopics,id2word=dictionary)
lsaModel.save('models/lsamodel.lsi')
print 'Done!\t',

t4=time.time()
print t4-t3

t5=time.time()
print 'Spend time:',t5-t0