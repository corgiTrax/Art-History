from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import smart_open, simple_preprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox

REMOVE = []
#
#["feel", "feels", "feeling", 
#"image",
#"makes", 
#"look", "looks", "looking",
#"think",
#"shows",
#"appear", "appears",
#"convey",
#"represents",
#"reminds",
#"gives",
#]
#
def tokenize(text):
    return [token for token in simple_preprocess(text) if ((token not in STOPWORDS) and (token not in REMOVE))]


def plot_embedding(X, ids, art_ids, whichArt, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    ax = plt.subplot(111)
    for i in range(X.shape[0]):
        if False:             
            plt.text(X[i, 0], X[i, 1], str(art_ids[i]), color=plt.cm.Set1(int(art_ids[i]) / 21.0), fontdict={'weight': 'bold', 'size': 8})
        elif art_ids[i] == whichArt:
            plt.text(X[i, 0], X[i, 1], str(ids[i]), color=plt.cm.Set1(int(art_ids[i]) / 21.0), fontdict={'weight': 'bold', 'size': 8})

    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)

if __name__ == '__main__':
    embed = np.load("result/all_cloud.npy")
    ids = np.load("result/all_ids.npy")
    art_ids = np.load("result/all_art_ids.npy")
    plot_embedding(embed, ids, art_ids, 20)
    plt.show()


