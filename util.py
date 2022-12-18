import pandas as pd
import numpy as np

class Smoothed_Distribution():
    a=[1]
    def __init__(self):
        self.counts={}
        self.n=0
        #self.a=1

    #def __setitem__(self, item, value):
    #    self.counts[item]+=1
    #    self.n+=1

    def setalpha(self, a):
        if a>0:
            self.a[0]=a

    def count(self, key):
        if key in self.counts:
            self.counts[key]+=1
        else:
            self.counts[key]=1
        self.n+=1

    def __getitem__(self, item):
        if self.n==0:
            return 0
        elif item in self.counts:
            return (self.counts[item]+self.a[0])/(self.n*(1+self.a[0]))
        else:
            return (self.a[0])/(self.n*(1+self.a[0]))

    #def to_dict(self):
    #    return {key:self[key] for key in self.counts}

    def __iter___(self):
        for key in self.counts:
            yield key

        yield "<UNKNOWN>"

    def get_min_prob(self):
        return (self.a[0])/(self.n*(1+self.a[0]))

    def tolist(self):
        return list(self.counts.keys())+["<UNKNOWN>"]

class DefaultDict(dict):
    def __init__(self, default):
        self.default=default

    def __missing__(self):
        return default



def create_conddf(dist_dict):
    """
    dist_dict: dictionary of Smoothed_Distribution objects

    returns: dataframe corresponding to values, where each intersection is
        p(row word | column word)
    """

    words=list(dist_dict.keys())+["<END>"]+["<UNKNOWN>"]
    df=pd.DataFrame(columns=words, index=words)

    for key in dist_dict:
        for word in words:
            df.loc[word, key]=dist_dict[key][word]
            #print(dist_dict[key][word])
            #rint(df)

    return df

def create_mardf(dist):
    """
    """
    df=pd.DataFrame(index=[0])
    for key in dist.tolist():
        df[key]=dist[key]

    return df



def get_prob(conddf, mar_df, word1, word2, l=1):
    """
    conddf: 2d pandas dataframe with same format as one created in create_conddf
    mar_df: 1d pandas dataframe containing marginials for all words
    word1: first word in bigram
    word2: second word in bigram
    l=lambda parameter, weighting for conditional vs marginial probability
    """


    if word1 not in mar_df:
        word1="<UNKNOWN>"
    if word2 not in mar_df:
        word2="<UNKNOWN>"
    elif word1!="<UNKNOWN>" and word2 not in conddf[word1]:
        word2="<UNKNOWN>"

    if word1=="<UNKNOWN>":

        #print('mar', type(mar_df[word2][0]), type(mar_df[word1][0]))
        return l*mar_df[word1][0]*mar_df[word2][0]+(1-l)*mar_df[word2][0]
    #print(word1, word2)

    #print(conddf)
    #print(list(conddf.columns.values), list(conddf.index.values))


    word2_i=list(conddf['Unnamed: 0']).index(word2)

    #print('cond',type(conddf[word1][word2_i]))
    #print('mar', type(mar_df[word2][0]))
    #print('cond', type(conddf[word1][word2_i]))
    return l*conddf[word1][word2_i] + (1-l)*mar_df[word2][0]

def get_total_prob(phrase, conddf, mar_df, l):
    """
    Returns log probability
    """
    prob=0
    for i in range(len(phrase)-1):
        prob+=np.log(get_prob(conddf, mar_df, phrase[i], phrase[i+1], l))
        #print(type(np.log(get_prob(conddf, mar_df, phrase[i], phrase[i+1], l))))

    #print(list(prob))
    #print(type(prob))
    return prob







