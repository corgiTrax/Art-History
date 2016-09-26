import logging
import gensim
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if len(sys.argv) < 2:
    print("Usage: python word2vec.py [model.bin]")
    sys.exit(1)

model = gensim.models.Word2Vec.load_word2vec_format(sys.argv[1], binary = True)

test = ["main", "man", "jacksons", "corgi"]

print("man" in model.vocab)
print("jacksons" in model.vocab)
