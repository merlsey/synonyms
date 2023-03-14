'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2022.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

'''Returns the similarity between two words based on their semantic descriptors'''
def cosine_similarity(vec1, vec2):
    v1 = 0
    v2 = 0
    num = 0

    for key, value in vec1.items():
        for key1, value1 in vec2.items():
            if key == key1:
                num += value*value1

    for key, value in vec1.items():
        v1 += value**2
    for key1, value1 in vec2.items():
        v2 += value1**2

    denom = math.sqrt(v1*v2)
    return (num/denom)

'''Counts in each sentence and word to build semantic descriptor.'''
def build_semantic_descriptors(sentences):
    worddict = {}

    for line in sentences:
        for word in line:
            worddict[word] = {}

    for line in sentences:
        for word in line:
            for x in range(len(line)):
                if word != line[x]:
                    if worddict[word].get(line[x]) == None:
                        worddict[word][line[x]] = 1
                    else:
                        worddict[word][line[x]] += 1

    return worddict

'''Adds files to one text, separating by sentence and word via the removal of punctuation.'''
def build_semantic_descriptors_from_files(filenames):
    punc_remove = [",", "-", "--", ":", ";", "(", ")", '"', "/", '”', '“']
    punc_sep = [".", "!", "?"]
    file = ""
    filelist = []
    ind1 = [-1]

    for i in range(len(filenames)):
        file += open(filenames[i], encoding="utf-8").read()
    file = file.lower()

    for val in punc_remove:
        file = file.replace(val, " ")
    for val in punc_sep:
        for i in range(len(file)):
            if file[i] == val:
                ind1.append(i)
    ind1.sort()
    for i in range(len(ind1)-1):
        filelist.append(file[ind1[i]+1:ind1[i+1]])

    splitfl = []
    for sentence in filelist:
        sentence = sentence.split()
        splitfl.append(sentence)

    final = build_semantic_descriptors(splitfl)
    return final

'''Returns the most similar word out of specifed choices based on their similarity.'''
def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    wordvec = semantic_descriptors.get(word)
    similaritylist = []

    if semantic_descriptors.get(word) != None:
        semantic_descriptors.pop(word)

    for val in choices:
        if semantic_descriptors.get(val) != None:
            compvec = semantic_descriptors.get(val)
            comparison = similarity_fn(wordvec, compvec)
            similaritylist.append((comparison, val))
        else:
            similaritylist.append((-1, val))

    similaritysort = sorted(similaritylist, reverse=True)
    return similaritysort[0][1]

'''Takes in texts to build the semantic descriptor and then uses the dictionary to determine accuracy in guesses.'''
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    qcount = len(open(filename, encoding="utf-8").readlines())
    sentences = open(filename, encoding="utf-8").read().split("\n")

    wordsplit = []

    for val in sentences:
        val = val.split()
        wordsplit.append(val)

    for i in range(len(wordsplit)):
        sd_copy = semantic_descriptors.copy()
        guess = most_similar_word(wordsplit[i][0], wordsplit[i][2:], sd_copy, similarity_fn)
        if guess == wordsplit[i][1]:
            correct += 1

    return (correct/qcount)*100

