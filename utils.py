from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import smart_open, simple_preprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
import sys

REMOVE = ["feel", "feels", "feeling", 
"image",
"makes", 
"look", "looks", "looking",
"think",
"shows",
"appear", "appears",
"convey",
"represents",
"reminds",
"gives",
]

#REMOVE = []

def tokenize(text):
    return [token for token in simple_preprocess(text) if ((token not in STOPWORDS) and (token not in REMOVE))]

ARTS = [0,1,2,10,11]
COLORS = ["red", "green", "blue", "purple", "orange", "gray"]
LETTERS = ['x', 'o', '+']

def plot_embedding(font, X, sent_ids, art_ids, sources, whichArt, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    #ax = plt.subplot(111)
    for i in range(X.shape[0]):
        # plot all sentences, for all arts
        if whichArt == "crowd":
            if sources[i] == 0 and art_ids[i] in ARTS: # only show crowd 
                #plt.text(X[i, 0], X[i, 1], str(art_ids[i]), color=plt.cm.Set1(int(art_ids[i]) / 21.0), fontdict={'weight': 'bold', 'size': font})
                plt.text(X[i, 0], X[i, 1], 'x', color=COLORS[ARTS.index(art_ids[i])], fontdict={'weight': 'bold', 'size': font})
        elif whichArt == "wiki":
            if sources[i] == 1: # only show crowd 
                plt.text(X[i, 0], X[i, 1], str(art_ids[i]), color=plt.cm.Set1(int(art_ids[i]) / 21.0), fontdict={'weight': 'bold', 'size': font})
        elif whichArt == "book":
            if sources[i] == 2: # only show crowd 
                plt.text(X[i, 0], X[i, 1], str(art_ids[i]), color=plt.cm.Set1(int(art_ids[i]) / 21.0), fontdict={'weight': 'bold', 'size': font})
        # plot art individually
        elif art_ids[i] == int(whichArt):
            if True: #sent_ids[i] == "363-5":
                #plt.text(X[i, 0], X[i, 1], str(sent_ids[i]), color=COLORS[sources[i]], fontdict={'weight': 'bold', 'size': font})
                plt.text(X[i, 0], X[i, 1], LETTERS[sources[i]], color=COLORS[sources[i]], fontdict={'weight': 'bold', 'size': font})

    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)

if __name__ == '__main__':
    embed = np.load("result/all_embed.npy")
    sent_ids = np.load("result/all_sent_ids.npy")
    art_ids = np.load("result/all_art_ids.npy")
    sources = np.load("result/all_sources.npy")
  
    ct = [0,0,0]
    for i in sources:
        ct[i] += 1
    print(ct)

    SAVE = True
    if SAVE:
        font = 15
        sdpi = 500
#        plot_embedding(font, embed, sent_ids, art_ids, sources, "crowd")
#        plt.savefig("result/all_crowd.png", dpi = sdpi, bbox_inches='tight')
#        plt.show()
#        plot_embedding(font, embed, sent_ids, art_ids, sources, "wiki")
#        plt.savefig("result/all_wiki.png", dpi = sdpi)
#        plt.close()
#        plot_embedding(font, embed, sent_ids, art_ids, sources, "book")
#        plt.savefig("result/all_book.png", dpi = sdpi)
#        plt.close()
    
        for i in range(21):
            plot_embedding(font, embed, sent_ids, art_ids, sources, str(i))
            plt.savefig("result/" + str(i) +  ".png", dpi = sdpi,bbox_inches='tight')
            plt.close()
    else:
        font = 9
        plot_embedding(font, embed, sent_ids, art_ids, sources, str(sys.argv[1]))
        plt.show()

   
