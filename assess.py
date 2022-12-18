import util
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

data=[
        ['mat ionim som var gels'.split(' '), 'mation ims om var gels'.split(' '), 'mation imsom vargels'.split(' '), 'mation ims om vargels'.split(' ')],
        ['cended mationit'.split(' '), 'ce nded mationit'.split(' '), 'cended mat ionit'.split(' '), 'ce nded mat ion it'.split(' ')],
        ['ims omed elislang eld lang elis'.split(' '), 'imsomed elis lang eld lang elis'.split(), 'imsomed elislang eld lang elis'.split(), 'im somed elis lang eld lang elis'.split()],
        ['cest yx vionit ionit'.split(), 'cestyx vionit ionit'.split(), 'cestyx vion it ion it'.split(), 'cest yx vion it ionit'.split()],
        ['noxumat ion itpros'.split(), 'noxumat ion it pros'.split(), 'noxu mation it pros'.split(), 'noxumat ionit pros'.split()],
        ['sevit ims omed var'.split(), 'sev it imsomed var'.split(), 'sev it ims omed var'.split(), 'sevit im somedvar'.split()],
        ['cestce styx mation pro seld'.split(), 'cest ce styx mation proseld'.split(), 'cest cest yx mation proseld'.split(), 'cest cestyx mation pro seld'.split()],
        ]



Parameters=pd.read_csv("Param.csv")

l=Parameters['l'][0]

cond_df=pd.read_csv("Conditional.csv")
mar_df=pd.read_csv("Marginials.csv")

#print(mar_df)
#print(cond_df)
#print(list(cond_df.columns.values))

#print(cond_df['Unnamed: 0'])





fig, ax= plt.subplots(len(data))


for p in range(len(data)):
    #print()

    log_probs=[]
    labels=[]
    for s in data[p]:
        #print(data[p])
        labels.append(" ".join(s))
        log_probs.append(util.get_total_prob(s, cond_df, mar_df, l))

    #print(list(range(len(data[p]))), log_probs)
    ax[p].bar(labels, log_probs)
    #print(labels)
    #print(log_probs)
    #print(p,list(range(len(data[p]))), labels)


plt.tight_layout()
plt.show()
        #print(s, ": \n", util.get_total_prob(s, cond_df, mar_df, l))


