import logging
import gensim
import sys
from pprint import pprint 
import csv
import copy as cp
from gensim.summarization import summarize, keywords
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if len(sys.argv) < 2: 
    print("Usage: python parse.py [data.csv]")
    sys.exit(1)


# store data
art0_short = []
art0_long = ""

input_file = open(sys.argv[1],'rt')
reader = csv.reader(input_file)

for row in reader:
    if row[0] == '0':
        short_res = row[2]
        long_res = row[3]
        long_res = long_res.replace('\n', '')
#        art0_long.append(cp.deepcopy(long_res))
        art0_long += long_res
input_file.close()

pprint(art0_long)
print(summarize(art0_long, ratio = 0.01))

print(keywords(art0_long, ratio = 0.05))
