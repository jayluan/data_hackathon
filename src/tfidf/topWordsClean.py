import numpy as np
import pandas as pd

word2wid = dict()
wid2word = dict()

wid = 0
with open("redditSubmissions.csv") as subfile:
    subid = 0
    for post in subfile:
        if subid == 0:
            subid += 1
            continue
        if len(post.split(",")) < 4:
            continue
        titlelist = post.split(",")[3].split(" ")
        for wo in titlelist:
            intword = str(wo).lower()
            word = ''.join(ch for ch in intword if ch.isalnum())
            if word not in word2wid:
                word2wid[word] = wid
                wid2word[wid] = word
                wid += 1

print "loaded dictionary. We have " + str(len(wid2word)) + " unique words."
wordcounts = np.zeros(wid+1,dtype=int)
with open("redditSubmissions.csv") as subfile:
    subid = 0
    for post in subfile:
        if subid == 0:
            subid += 1
            continue
        if len(post.split(",")) < 4:
            continue
        titlelist = post.split(",")[3].split(" ")
        for wo in titlelist:
            intword = str(wo).lower()
            word = ''.join(ch for ch in intword if ch.isalnum())
            wordcounts[word2wid[word]] += 1

# load data frame
d = pd.read_csv('redditSubmissions.csv', sep=',', error_bad_lines=False, dtype={'unixtime': np.float64})

sid2sub = dict()
sub2sid = dict()
sid = 0
for sub in d.subreddit:
    if sub not in sub2sid:
        sub2sid[str(sub).lower()] = sid
        sid2sub[sid] = str(sub).lower()
        sid += 1

class SubDicts:
    def __init__(self):
        self.ind2wid = dict()
        self.wid2ind = dict()
        self.nwords = 0

sub2dicts = dict()
for subr, title in zip(d.subreddit, d.title):
    sub = str(subr).lower()
    if sub not in sub2dicts:
        # current wid, wid2word, and word2wid in that order
        sub2dicts[sub] = SubDicts()
    for wo in str(title).split(" "):
        intword = str(wo).lower()
        word = ''.join(ch for ch in intword if ch.isalnum())
        if word not in word2wid:
            continue
        wid = word2wid[word]
        if wid not in sub2dicts[sub].wid2ind:
            ind = sub2dicts[sub].nwords
            sub2dicts[sub].wid2ind[wid] = ind
            sub2dicts[sub].ind2wid[ind] = wid
            sub2dicts[sub].nwords += 1

sub2counts = dict()
for subr, title in zip(d.subreddit, d.title):
    sub = str(subr).lower()
    if sub not in sub2counts:
        # current wid, wid2word, and word2wid in that order
        sub2counts[sub] = np.zeros(sub2dicts[sub].nwords + 1)
    for wo in str(title).split(" "):
        intword = str(wo).lower()
        word = ''.join(ch for ch in intword if ch.isalnum())
        if word not in word2wid:
            continue
        wid = word2wid[word]
        sub2counts[sub][sub2dicts[sub].wid2ind[wid]] += 1


# Now, get top 10 TF-IDF posts per subreddit
while(1):
    print "Enter a subreddit name: "
    subr = raw_input()
    if subr == "break":
        break
    sub = str(subr).lower()
    if sub not in sub2dicts:
        print "Subreddit doesn't exist"
        continue
    # Get the TF-IDF for each word in the sub
    nwords = sub2dicts[sub].nwords
    tfidfs = np.zeros(nwords,dtype=float)
    for ind in range(sub2dicts[sub].nwords):
        wid = sub2dicts[sub].ind2wid[ind]
        tf = sub2counts[sub][ind]
        idf = wordcounts[wid]
        tfidfs[ind] = tf / idf
    topwords = tfidfs.argsort()[::-1]
    print sub + "'s top words: "
    for i in xrange(min(10,sub2dicts[sub].nwords)):
        print wid2word[sub2dicts[sub].ind2wid[topwords[i]]] 
