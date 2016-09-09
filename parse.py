import csv
import sys
import numpy
from pprint import pprint 
from collections import defaultdict
import re
import copy as cp
from gensim.utils import smart_open, simple_preprocess
from gensim.corpora.wikicorpus import _extract_pages, filter_wiki
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora
import logging, gensim, bz2
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if len(sys.argv) < 2: 
    print("Usage: python parse.py [data.csv]")
    sys.exit(1)

def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]

# store data
data = []
art0_short = []
art0_long = []

input_file = open(sys.argv[1],'rt')
reader = csv.reader(input_file)

for row in reader:
    if row[0] == '0':
        short_res = row[2]
        long_res = row[3]
        shorts = re.split('\,|\.|\n|;|\?|!',short_res)
        longs = re.split('\,|\.|\n|;|\?|!',long_res)
        art0_short += [sent for sent in shorts]
        art0_long += [sent for sent in longs]

input_file.close()

## remove common words and tokenize
##stoplist = set('for a of the and to in'.split())
#stoplist = []
#stoplist_file = open("stopword.txt",'r')
#for line in stoplist_file:
#    stoplist.append((line.strip('\n')))
#stoplist_file.close()
#texts = [[word for word in art0_long.lower().split() if word not in stoplist]
#         for art0_long in art0_long]

texts = []
for sent in art0_long:
    texts.append(tokenize(sent))
#pprint(texts)

## remove words that appear only once
#frequency = defaultdict(int)
#for text in texts:
#    for token in text:
#        frequency[token] += 1
#
#texts = [[token for token in text if frequency[token] > 1]
#         for text in texts]

dict0 = corpora.Dictionary(texts)
# ignore words that appear in less than 20 documents or more than 10% documents
#dict0.filter_extremes(no_below=2, no_above=0.1)

dict0.save('art0.dict')  # store the dictionary, for future reference
#print(dictionary.token2id)

corpus0 = [dict0.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('art0.mm', corpus0)  # store to disk, for later use

dict0 = corpora.Dictionary.load('art0.dict')

corpus0 = corpora.MmCorpus('art0.mm')
#lsi = gensim.models.lsimodel.LsiModel(corpus=corpus0, id2word=dict0, num_topics=1)
#lsi.print_topics(1)
print(corpus0)

most_index, most_count = max(corpus0[1], key=lambda (word_index, count): count)
print(dict0[most_index], most_count)
#lda = gensim.models.ldamodel.LdaModel(corpus=corpus0, id2word=dict0, num_topics=3, update_every=1, chunksize=100, passes=10)
#lda.print_topics(3)
