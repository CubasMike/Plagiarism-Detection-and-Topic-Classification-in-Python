'''
Created on Apr 15, 2013

@author: MiguelAngel
'''
import os
import re
import xml.sax

class PanHandler( xml.sax.ContentHandler ):
    def __init__(self,lang='en'):
        self.reference = ''
        self.lang=lang
        self.req=[]

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == 'document':
            self.reference=attributes['reference']
        if tag == 'feature':
            if attributes['name']=='about':
                if attributes['lang']==self.lang:
                    self.req.append(self.reference)
                    

class pan2011corpus():
    def __init__(self,corpusDir):
        self.corpusDir=corpusDir

    def fn_per_lang(self,lang='en'):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        Handler=PanHandler(lang)
        parser.setContentHandler(Handler)
        for i in [i for i in os.listdir(self.corpusDir) if re.match('(.)*\.xml', i)]:
            parser.parse(self.corpusDir+i)
        return Handler.req