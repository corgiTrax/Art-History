import csv
import sys
import numpy
import gensim
from pprint import pprint 
from collections import defaultdict

if len(sys.argv) < 2: 
    print("Usage: python parse.py [data.csv]")
    sys.exit(1)


input_file = open(sys.argv[1],'rt')
reader = csv.reader(input_file)

# store data
data = []
art0_short = []
art0_long = []

for row in reader:
    if row[0] == '0':
        art0_short.append(row[2])
        art0_long.append(row[3])

# remove common words and tokenize
#stoplist = set('for a of the and to in'.split())
stoplist = []
stoplist_file = open("stopword.txt",'r')
for line in stoplist_file:
    stoplist.append((line.strip('\n')))
stoplist_file.close()

texts = [[word for word in art0_long.lower().split() if word not in stoplist]
         for art0_long in art0_long]

## remove words that appear only once
#frequency = defaultdict(int)
#for text in texts:
#    for token in text:
#        frequency[token] += 1
#
#texts = [[token for token in text if frequency[token] > 1]
#         for text in texts]

pprint(texts)

input_file.close()
