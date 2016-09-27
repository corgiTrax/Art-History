import csv
import xlrd
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
import utils
from sklearn.manifold import TSNE
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
numpy.set_printoptions(suppress=True)

class Sentence:
    def __init__(self, orig_text, text, art_id, subj_id, sent_id, source):
        self.art_id = art_id
        self.subj_id = subj_id
        self.sent_id = sent_id
        self.source = source # 0: crowd; 1: wiki; 2: textbook
        self.words = text
        self.nw = len(self.words)
        self.orig_text = orig_text

    def display(self):
        print("UID: " + "{}-{}-{}-{}".format(self.art_id, self.source, self.subj_id, self.sent_id))
        print("art id: " + str(self.art_id))
        print("source: " + str(self.source))
        print("subj-sent id: " + str(self.subj_id) + '-' + str(self.sent_id))
        print("original text: " + self.orig_text)
        print(self.words)
        print("number of words: " + str(self.nw))

    def word2vec(self, model):
        '''convert all words in this sentence to be a vector, using a pretrained word2vec embedding'''
        self.wordvecs = []
        for word in self.words:
            vec = model[word]
            self.wordvecs.append(cp.deepcopy(vec))

        '''sum all word vectors'''
        for ct, vec in enumerate(self.wordvecs):
            if ct == 0:
                self.sumvec = cp.deepcopy(vec)
            else:
                self.sumvec = numpy.sum([self.sumvec, vec], axis = 0)
        self.sumvec = self.sumvec / float(self.nw)

        '''save obtained sum vector to file'''
        # save summed vector
        filename = "vec/sum_" + str(self.art_id) + "_" + str(self.source) + "_" + str(self.subj_id) + "_" + str(self.sent_id) +".npy"
        numpy.save(filename, self.sumvec)
        print("Saving to " + filename)
        print("-"*100)
#        # also save word vectors
#        for ct, vec in enumerate(self.wordvecs):
#            filename = "vec/word_" + str(self.art_id) + "_" + str(self.source) + "_" + str(self.subj_id) + "_" + str(self.sent_id) + "_" + str(ct) + ".npy"
#            numpy.save(filename, vec)

    def loadVec(self):
        '''load word and sum vectors according to default names, this saves the labor of loading word2Vec model again'''
        filename = "vec/sum_" + str(self.art_id) + "_" + str(self.source) + "_" + str(self.subj_id) + "_" + str(self.sent_id) +".npy"
        self.sumvec = numpy.load(filename)
# not using wordvecs for now
#        self.wordvecs = []
#        for ct in range(self.nw):
#            filename = "vec/word_" + str(self.art_id) + "_" + str(self.source) + "_" + str(self.subj_id) + "_" + str(self.sent_id) + "_" + str(ct) + ".npy"
#            self.wordvecs.append(cp.deepcopy(numpy.load(filename)))

class Document:
    '''a document store a list of sentence classes'''
    def __init__(self, crowd_csvfile, school_csvfile):
        self.sentences = []
        self.model = gensim.models.Word2Vec.load_word2vec_format("../GoogleNews.bin", binary = True)

        crowd_file = open(crowd_csvfile,'rt')
        crowd_reader = csv.reader(crowd_file)
        source = 0 # crowd
        for ct,row in enumerate(crowd_reader):
            if ct != 0:
                art_id = int(row[0])
                subj_id = ct - 1 # ignore the first line
                short_res = row[2]
                long_res = row[3]
                longs = re.split('\n|\.|;|\?|!',long_res) # do not split using ',' now
                for ct_sent, sent in enumerate(longs):
                    new_sent = sent.translate(None, string.punctuation)
                    new_sent = utils.tokenize(new_sent)
                    # we remove tokens that are not in model vocabulary
                    for word in new_sent[:]:
                        if not(word in self.model.vocab): new_sent.remove(word)
                    if len(new_sent) > 1:
                        sent_class = Sentence(cp.deepcopy(sent), cp.deepcopy(new_sent), art_id, subj_id, ct_sent, source)
                        self.sentences.append(cp.deepcopy(sent_class))
        crowd_file.close()
        
        school_file = xlrd.open_workbook(school_csvfile)
        sh = school_file.sheet_by_index(0)
        for ct in range(sh.nrows):
            if ct != 0:
                row = sh.row(ct)
                art_id = int(row[0].value)
                subj_id = ct - 1 # ignore the first line

                wiki_res = row[5].value.encode('ascii','ignore')
                wikis = re.split('\n|\.|;|\?|!',wiki_res) 
                source = 1
                for ct_sent, sent in enumerate(wikis):
                    new_sent = sent.translate(None, string.punctuation)
                    new_sent = utils.tokenize(new_sent)
                    # we remove tokens that are not in model vocabulary
                    for word in new_sent[:]:
                        if not(word in self.model.vocab): new_sent.remove(word)
                    if len(new_sent) > 1:
                        sent_class = Sentence(cp.deepcopy(sent), cp.deepcopy(new_sent), art_id, subj_id, ct_sent, source)
                        self.sentences.append(cp.deepcopy(sent_class))

                book_res = row[6].value.encode('ascii','ignore')
                books = re.split('\n|\.|;|\?|!',book_res) 
                source = 2
                for ct_sent, sent in enumerate(books):
                    new_sent = sent.translate(None, string.punctuation)
                    new_sent = utils.tokenize(new_sent)
                    # we remove tokens that are not in model vocabulary
                    for word in new_sent[:]:
                        if not(word in self.model.vocab): new_sent.remove(word)
                    if len(new_sent) > 1:
                        sent_class = Sentence(cp.deepcopy(sent), cp.deepcopy(new_sent), art_id, subj_id, ct_sent, source)
                        self.sentences.append(cp.deepcopy(sent_class))

    def buildSaveVec(self):
        '''for each sentence in document, do word2vec and save'''
        for ct, sent in enumerate(doc.sentences):
            sent.display()
            sent.word2vec(self.model)

    def loadVec(self):
        '''must be called after buildSaveVec(), load sum and word vectors'''
        for ct, sent in enumerate(doc.sentences):
            sent.loadVec()

    def frequency(self):
        '''note: this frequency is after removing oovs (word2Vec model), stop words and tfidfs (if REMOVE != [])'''
        words = [[]]
        for sent in self.sentences:
            words[0] += cp.deepcopy(sent.words)
        dict0 = corpora.Dictionary(words)
        corpus0 = [dict0.doc2bow(word) for word in words]
        # frequency analysis
        most_index, most_count = max(corpus0[0], key=lambda (word_index, count): count)
        sorted_dict0 = sorted(corpus0[0], key = operator.itemgetter(1), reverse = True)
        for i in range(100): # show top 100 words
            print(dict0[sorted_dict0[i][0]], sorted_dict0[i][1])
           
if __name__ == '__main__':
    doc = Document("data/parsed_data.csv", "data/wiki.xlsx")
#    doc.frequency()
    # only need to call this once when constructing vectors
    doc.buildSaveVec()
    doc.loadVec()
    
    vecs = []
    sent_ids = []
    art_ids = []
    sources = []
    for sent in doc.sentences:
        vecs.append(sent.sumvec)
        sent_ids.append(str(sent.subj_id) + '-' + str(sent.sent_id))
        art_ids.append(sent.art_id)
        sources.append(sent.source)
    
    print("Now running TSNE.......")
    tsne = TSNE(n_components=2, init = 'pca', random_state=0)
    #tsne = TSNE(n_components=2, random_state=0)
    embed = tsne.fit_transform(vecs)
    numpy.save("result/all_embed.npy", embed)
    numpy.save("result/all_sent_ids.npy", sent_ids)
    numpy.save("result/all_art_ids.npy", art_ids)
    numpy.save("result/all_sources.npy", sources)
