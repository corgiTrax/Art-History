import csv
import sys
import numpy
from pprint import pprint 
from collections import defaultdict
import re
import string
import copy as cp
from gensim.utils import smart_open, simple_preprocess
from gensim.corpora.wikicorpus import _extract_pages, filter_wiki
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora
from gensim.summarization import summarize
import logging, gensim, bz2
import operator

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if len(sys.argv) < 2: 
    print("Usage: python parse.py [data.csv]")
    sys.exit(1)

def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]

# store data
data = []
art0_short = []
art0_long = [""]

input_file = open(sys.argv[1],'rt')
reader = csv.reader(input_file)

for ct,row in enumerate(reader):
    if ct > 0:
        short_res = row[2]
        long_res = row[3]
#        shorts = re.split('\,|\.|\n|;|\?|!',short_res)
#        longs = re.split('\,|\.|\n|;|\?|!',long_res)
#       art0_short += [sent for sent in shorts]
#        art0_long += [sent for sent in longs]
        longs = long_res.translate(None, string.punctuation)
#        art0_long.append(cp.deepcopy(longs))
        art0_long[0] += longs
input_file.close()

texts = []
for sent in art0_long:
    texts.append(tokenize(sent))
pprint(texts)

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
#dict0.filter_n_most_frequent(1)

dict0.save('art0.dict')  # store the dictionary, for future reference
#print(dictionary.token2id)

corpus0 = [dict0.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('art0.mm', corpus0)  # store to disk, for later use
# print(corpus0)

dict0 = corpora.Dictionary.load('art0.dict')

corpus0 = corpora.MmCorpus('art0.mm')
#print(corpus0)

# frequency analysis
most_index, most_count = max(corpus0[0], key=lambda (word_index, count): count)
#print(dict0[most_index], most_count)
sorted_dict0 = sorted(corpus0[0], key = operator.itemgetter(1), reverse = True)
for i in range(100):
    print(dict0[sorted_dict0[i][0]], sorted_dict0[i][1])

# lsa and lda
#lsi = gensim.models.lsimodel.LsiModel(corpus=corpus0, id2word=dict0, num_topics=1)
#lsi.print_topics(1)

#lda = gensim.models.ldamodel.LdaModel(corpus=corpus0, id2word=dict0, num_topics=1, update_every=1, chunksize=100, passes=10)
#lda.print_topics(1)
