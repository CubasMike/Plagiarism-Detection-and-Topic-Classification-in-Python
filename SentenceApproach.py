'''
Created on Feb 1, 2013

@author: MiguelAngel
'''
import nltk
import math

def calc_tf(doc):
    dic={}
    for i in doc:
        if not dic.has_key(i):
            dic[i]=1
        else:
            dic[i]+=1
    tw=len(doc)
    if tw==0: tw=1
    for i in dic.keys():
        dic[i]/=float(tw)
    return dic

def remove_stopwords(dic):
    stopwords=['the','of','and','a','in','to','is','was','it','for','with','he','be','on','i','that','by','at','you','\'s','are','not','his','this','from','but','had','which','she','they','or','an','were','we','their','been','has','have','will','would','her','\'t','there','can','all','as','if','who','what','said']
    for i in stopwords:
        if dic.has_key(i):
            dic.pop(i)
    return dic

def eucl_norm(d1):
    norm=0.0
    for val in d1.values():
        norm+=float(val*val)
    return math.sqrt(norm)

def cosine_measure(d1,d2):
    dot_prod=0.0
    det=eucl_norm(d1)*eucl_norm(d2)
    if det==0:
        return 0 
    for word in d1.keys():
        if d2.has_key(word):
            dot_prod+=d1[word]*d2[word]
    return dot_prod/det
    
path_source='D:\CIC\Research visit Greece\pan-plagiarism-corpus-2011\external-detection-corpus\source-document\source-document00178.txt'
path_suspicious='D:\CIC\Research visit Greece\pan-plagiarism-corpus-2011\external-detection-corpus\suspicious-document\suspicious-document00005.txt'
f_source=open(path_source,'rU')
source_text=(f_source.read()).lower()
f_source.close()
f_suspicious=open(path_suspicious,'rU')
suspicious_text=(f_suspicious.read()).lower()
f_suspicious.close()
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
source_sents=sent_detector.tokenize(source_text.strip())
print 'Source sentences:',len(source_sents)
suspicious_sents=sent_detector.tokenize(suspicious_text.strip())
print 'Suspicious sentences:',len(suspicious_sents)
pattern_word=r'''(?x) # set flag to allow verbose regexps
            ([A-Z]\.)+ # abbreviations, e.g. U.S.A.
            | \w+(-\w+)* # words with optional internal hyphens
            | \$?\d+(\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
            '''
source_sents_words=[nltk.regexp_tokenize(x, pattern_word) for x in source_sents]
suspicious_sents_words=[nltk.regexp_tokenize(x, pattern_word) for x in suspicious_sents]
source_matrix=[calc_tf(x) for x in source_sents_words]
suspicious_matrix=[calc_tf(x) for x in suspicious_sents_words]
#source_matrix=[nltk.FreqDist(x) for x in source_sents_words]
#suspicious_matrix=[nltk.FreqDist(x) for x in suspicious_sents_words]
source_matrix=[remove_stopwords(x) for x in source_matrix]
suspicious_matrix=[remove_stopwords(x) for x in suspicious_matrix]
P=[]
for i in suspicious_matrix:
    P.extend([(suspicious_matrix.index(i),source_matrix.index(j)) for j in source_matrix if cosine_measure(j,i)>0.5])
print P
print len(P)