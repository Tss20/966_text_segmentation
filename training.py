import numpy as np
import pandas as pd
import util
from util import Smoothed_Distribution
import regex as re

def parse(file_name):
    f=open(file_name, "r")
    lines=f.read().split('\n')

    parsed=[]
    for line in lines:

        parsed_line=line.lower()
        #parsed_line=re.sub("-", " ", line).lower()
        #parsed_line=re.sub("[^\w\s\d]", "", parsed_line)#.lower()
        #parsed_line=re.sub("\n", " ", parsed_line)

        #parsed_line=re.sub("<|>|;\:|", '', line).lower()
        #p=[]
        #for i in range(len(parsed_line)-1, -1, -1):
        #    if
        parsed.append(parsed_line.split(' '))
    return parsed

def get_distributions(parsed_lines):
    cond={
            "<START>":Smoothed_Distribution(),
            "<END>":Smoothed_Distribution()
            #"<UNKNOWN>":Smoothed_Distribution()

            }
    mar=Smoothed_Distribution()
    for line in parsed_lines:
        mar.count("<START>")
        for i, word in enumerate(line):
            if word not in cond:
                cond[word]=Smoothed_Distribution()
            if i==0:
                cond["<START>"].count(word)
            else:
                cond[line[i-1]].count(word)

            mar.count(word)
        if line[-1] not in cond:
            cond[line[-1]]=Smoothed_Distribution()
        cond[line[-1]].count("<END>")
        mar.count("<END>")

    return cond, mar


def get_prob_instance(word1, word2, cond, mar, l, debug=False):
    #print(word1, word2, cond[word1][word2], mar[word2])

    #if cond[word1][word2]==0 and mar[word2]==0:
    #    #print(word1, word2)



    if word1 not in cond:
        cond_prob=mar["<UNKNOWN>"]*mar[word2]
    else:
        cond_prob=cond[word1][word2]

    if debug:
        print(word1, word2, cond[word1][word2], mar[word2], l)
    #if l*cond[word1][word2]+(1-l)*mar[word2]==0:
    #    print(word1, word2, l, cond[word1][word2], mar[word2])
    return l*cond_prob+(1-l)*mar[word2]

def get_logprob_all(parsed_lines, cond, mar, l):
    total_prob=0

    for line in parsed_lines:
        for i in range(len(line)+1):
            prev=total_prob
            if i==0:
                prob=get_prob_instance("<START>", line[i], cond, mar, l)
                total_prob+=np.log(prob)#get_prob_instance("<START>", line[i], cond, mar, l)
            elif i==len(line):
                prob=get_prob_instance(line[i-1], "<END>", cond, mar, l)
                total_prob+=np.log(prob)#get_prob_instance(line[i-1], "<END>", cond, mar, l)
            else:
                prob=get_prob_instance(line[i-1], line[i], cond, mar, l)
                total_prob+=np.log(prob)#get_prob_instance(line[i-1], line[i], cond, mar, l)

            #if total_prob==0 and prev!=0:

                #if i==0:
                #    word1="<START>"
                #else:
                #    word1=line[i-1]
                #if i==len(line):
                #    word2="<END>"
                #else:
                #    word2=line[i]
                #print(l, mar.a, word1, word2, cond[word1][word2], mar[word2], prev, prob)

    return total_prob




def optimize_hyperparameters(parsed_lines, cond, mar):
    a_options=np.arange(0.1,1.1,0.1)
    l_options=np.arange(0.1,1.1,0.1)



    max_prob=get_logprob_all(parsed_lines, cond, mar, 1)
    max_al=mar.a[0], 1
    for a in a_options:
        mar.setalpha(a)

        for l in l_options:
            prob=get_logprob_all(parsed_lines, cond, mar, l)
            #print(prob, max_prob)
            if prob>max_prob:
                max_prob=prob
                max_al=a,l

    return max_al


if __name__=="__main__":
    parsed_lines=parse("training_data.txt")


    training, validation = parsed_lines[:-2],  parsed_lines[-2:]
    print("Generating distributions from training data")
    cond,mar=get_distributions(training)

    print("Optimizing hyperparameters")
    a,l=optimize_hyperparameters(validation, cond, mar)
    mar.setalpha(a)

    print("Loading dataframes...")
    print(len(cond), "features")

    print("Loading conditionals")
    cond_df=util.create_conddf(cond)

    print("Loading marginials")
    mar_df=util.create_mardf(mar)

    print("Loading parameters")
    parameters=pd.DataFrame(index=[0])

    parameters['a']=a
    parameters['l']=l


    print("Writing conditional csv")
    cond_df.to_csv("Conditional.csv")

    print("Writing marginial csv")
    mar_df.to_csv("Marginials.csv")

    print("Writing parameters csv")
    parameters.to_csv("Param.csv")

