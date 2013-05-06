'''
Created on Apr 12, 2013

@author: MiguelAngel
'''
import nltk
import re
from gensim import corpora

class MyCorpus(object):
    def __init__(self,dictionary,corpusDir,filenames,n=1,lemmatize='no',removeStopwords='no',lowerCase='no',other='no',wordnetDictionary='no'):
        self.dictionary=dictionary
        self.corpusDir=corpusDir
        self.filenames=filenames
        self.n=n
        self.lemmatize=lemmatize
        self.removeStopwords=removeStopwords
        self.lowerCase=lowerCase
        self.other=other
        self.wordnetDictionary=wordnetDictionary
        
    def __iter__(self):
        for filename in self.filenames:
            fid=open(self.corpusDir+filename,'rU')
            text=fid.read()
            features=NGrams(PreProcesser(Tokenizer(text),self.lemmatize,self.removeStopwords,self.lowerCase,self.other,self.wordnetDictionary),self.n)
            fid.close()
            yield self.dictionary.doc2bow(features)
                
def DictionaryGenerator(corpusDir,filenames,n=1,lemmatize='no',removeStopwords='no',lowerCase='no',other='no',wordnetDictionary='no'):
    dictionary=corpora.Dictionary([])
    cont=0
    num=0
    lim=len(filenames)/10
    for filename in filenames:
        fid=open(corpusDir+filename,'rU')
        text=fid.read()
        dictionary.add_documents([NGrams(PreProcesser(Tokenizer(text),\
                                                      lemmatize,removeStopwords,lowerCase,other,wordnetDictionary),n)])
        fid.close()
        cont+=1
        if cont==lim:
            num+=1
            print num*10,'% ..... Done!'
            cont=0
    return dictionary
             
def Tokenizer(text):
    sentDetector = nltk.data.load('tokenizers/punkt/english.pickle')
    patternWord=r'''(?x)([A-Z]\.)+|\w+(-\w+)*|\$?\d+(\.\d+)?%?'''
    sents=sentDetector.tokenize(text)
    return [nltk.regexp_tokenize(sent,patternWord) for sent in sents]
             
def PreProcesser(sentsWords,lemmatize='no',removeStopwords='no',lowerCase='no',other='no',wordnetDictionary='no'):
    Res=[]
    wnl=nltk.WordNetLemmatizer()
    stopwords=['the','of','and','a','in','to','is','was','it','for','with', \
           'he','be','on','i','that','by','at','you','\'s','are','not', \
           'his','this','from','but','had','which','she','they','or','an', \
           'were','we','their','been','has','have','will','would','her', \
           '\'t','there','can','all','as','if','who','what','said']
    for words in sentsWords:
        textTemp=words
        if lowerCase=='yes':
            textTemp=[word.lower() for word in textTemp]
        if removeStopwords=='yes':
            textTemp=[word for word in textTemp if word not in stopwords]
        if lemmatize=='yes':
            textTemp=[wnl.lemmatize(word) for word in textTemp]
        if other=='yes':
            textTemp=[word for word in textTemp if re.match(r'[a-zA-Z](.)*',word) and len(word)>2]
        if wordnetDictionary=='yes':
            textTemp=[word for word in textTemp if nltk.corpus.wordnet.synsets(word)]
        Res.append(textTemp)
    return Res
                
def NGrams(text,n,divSent='no'):
    ng=[]
    if divSent=='no':
        for sent in text:
            for i in range(len(sent)-n+1):
                ng.append(tuple(sent[i:i+n]))
    else:
        for sent in text:
            ngTemp=[]
            for i in range(len(sent)-n+1):
                ngTemp.append(tuple(sent[i:i+n]))
            ng.append(ngTemp)
    return ng