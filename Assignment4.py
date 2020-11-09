#!/usr/bin/env python3
import collections 
import sys
from Porter_Stemmer_Python import PorterStemmer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def read_file(filename):
    f = open(filename)
    return f.readlines()

#removes special characters frm words
def remove_chars(line):
    special_chars = [',',';','.','"',')',"'",'(','0','1','2','3','4','5','6','7','8','9', '[', ']','â', '€', '?','¦', ':', '\n'] 
    blank = ''
    words = line.split()
    fixed_word = ""
    new_words = []
    for w in words: #remove special characters
        new_word = w
        for c in special_chars:
            new_word = new_word.replace(c, blank)
        new_words.append(new_word)
    new_words2 = []
    for w in new_words: # remove blank words and make all words lower case
        if not w == "":
            new_words2.append(w.lower())
    return new_words2

# removes the words from the list that are in stop_words.txt
def remove_stop_words(words):
    stop_f = open("stop_words.txt")
    sw = stop_f.read().replace('\n',' ')
    sw = sw.split()
    words2 = []
    is_sw = False
    for w in words:
        for s in sw:
            if w==s:
                is_sw = True
                break  # move to next word
        if not is_sw:
            words2.append(w)
        else:
            is_sw = False
    return words2

def remove_hyphens(words):
    for i,w in enumerate(words):
        if '-' in w:
            broken = w.split('-')
            del words[i]
            for b in broken:
                words.append(b)
    return words

def FCAN(df):
    alpha = 1 #learning rate
    threshold = 8
    w = [] # center of gravity for each cluster
    clusters = [] # record the paragraphs contained in each cluster
    w.append(alpha*np.array(df.iloc[0])) # initialize first cluster cog
    clusters.append([0])
    i = 1
    while i < df.shape[0]: # for every entry in the tdm
        min_ed = 10**10
        x = np.array(df.iloc[i])
        for j,cluster in enumerate(w): # determine the ed from each cluster to x
            ed = euc_dist(cluster,x)
            if ed < min_ed:
                min_ed = ed
                min_index = j # record which cluster was closest to x
        if min_ed < threshold: # adjust center of gravity for closest cluster if less than threshold
            w[min_index] = (w[min_index] + alpha*x)/(len(w) + 1)
            clusters[min_index].append(i)
        else:
            w.append(alpha*x) #create new cluster if ed was greater than threshold
            clusters.append([i])
        i +=1
    return clusters # return the clusters

def euc_dist(v1,v2):
    return np.linalg.norm(v1-v2) #return the euclidean distance between two vectors


def main():
    lines = read_file("paragraphs.txt")
    mined_file = "edit.txt"             # file that contains the text after steps A-E are performed
    tdms = []
    p = PorterStemmer()
    for l in lines:
        edit_f = open(mined_file,'w')
        edit = remove_stop_words(remove_hyphens(remove_chars(l))) # remove special characters,split hyphenated words, and remove stop words
        for w in edit:
            edit_f.write(w + " ") # write edited text to file so porter stemmer can be used
        edit_f.close()
        stemmed = p.run("edit.txt")  # stemmed text
        open(mined_file,'w').close() # clear the file for the next paragraph
        tdms.append(stemmed.split()) # add mined text to a list

        with open('stemmed_file.txt', 'w') as f:
            for item in tdms:
                if item:
                    f.write("%s\n" % item)

    tdms = list(filter(None,tdms)) #remove empty lines

    # create tdm from feature vectors
    docs = open("stemmed_file.txt")
    vec = CountVectorizer()
    X = vec.fit_transform(docs)
    total_features = len(vec.vocabulary_)
    df= pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    total = df.T.sort_values(by=0, ascending=False).head(100)
    final=total.transpose()
    final.to_csv('TEST_TDM.csv', index=False, header=True)

    # run algorithm on tdm and print the results
    subjects = FCAN(final)
    for i,f in enumerate(subjects):
        print("Subject "+ str(i)+ " included paragraphs" + str(f))


if __name__=='__main__':
    main()
