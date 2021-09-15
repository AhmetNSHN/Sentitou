import re
import json
import numpy as np
import pandas as pd
from nltk.corpus import stopwords

df = pd.read_csv("training_data/Training_Dataset.csv", sep='\t', names=["id", "review", "value"], usecols=["review", "value"])
review_list = df.review.to_list()
class_list = df.value.to_list()

data = [[re.sub(r'[^a-zA-Z ]', '', review_list[i].lower()).split(), class_list[i]] for i in range(1, len(review_list))]
print("non-ascii characters removed and characters changed to lowecase")

all_stopwords = stopwords.words('english')
for row_number in range(0, len(data)):
    data[row_number][0] = [word for word in data[row_number][0] if word not in all_stopwords]
print("stopwords removed")

np.random.shuffle(data)
training = data
# testing = data[7000:]
classes = [0, 1]

def train_naive_bayes(training, classes):
    """Given a training dataset and the classes that categorize
    each observation, return V: a vocabulary of unique words,
    prior_p: a list of P(c), and likelihood_p: a list of P(fi|c)s
    for each word
    """

    # Initialize class_document[ci]: a list of all documents of class i
    # E.g. class_document[1] is a list of [reviews, ratings] of class 1
    class_document = [[]] * len(classes)

    # Initialize num_doc[ci]: number of documents of class i
    num_doc = [None] * len(classes)

    # Initialize prior_p[ci]: stores the prior probability for class i
    prior_p = [None] * len(classes)

    # Initialize likelihood_p: likelihood_p[ci][wi] stores the likelihood probability for wi given class i
    likelihood_p = [None] * len(classes)

    # Partition documents into classes. class_document[0]: negative docs, class_document[1]: positive docs
    for pair in training:  # pair: a [review, rating] pair
        if pair[1] == "1":
            class_document[1] = class_document[1] + [pair]
            # Can also write as class_document[1] = class_doocument[1].append(pair)
        elif pair[1] == "0":
            class_document[0] = class_document[0] + [pair]

    # print(document_class[0])
    # Creates a vocabulary list. For large datasets

    V = []
    for pair in training:
        for word in pair[0]:
            if word in V:
                continue
            else:
                V.append(word)
    print("Vocabulary List created")

    V_size = len(V)
    # n_docs: total number of documents in training set
    n_docs = len(training)

    total_iteration = V_size*2
    current_iteration = 0

    for ci in range(len(classes)):

        current_iteration += 1
        print(current_iteration / total_iteration, end="\r")

        # Store n_class value for each class
        num_doc[ci] = len(class_document[ci])

        # Compute P(c)
        prior_p[ci] = np.log((num_doc[ci] + 1) / n_docs)

        # Counts total number of words in class c
        total_number_of_words = 0
        for sentence in class_document[ci]:
            total_number_of_words = total_number_of_words + len(sentence[0])
        denom = total_number_of_words + V_size # size of V

        dic = {}
        # Compute P(w|c)
        for word_i in V:
            current_iteration += 1
            print(current_iteration/total_iteration, end="\r")

            # Count number of times word_i appears in class_document[ci]
            count_wi_in_D_c = 0
            for sentence in class_document[ci]:
                for word in sentence[0]:
                    if word == word_i:
                        count_wi_in_D_c = count_wi_in_D_c + 1

            numer = count_wi_in_D_c + 1
            dic[word_i] = np.log((numer) / (denom)) # likelihood for words

        likelihood_p[ci] = dic

    return (V, prior_p, likelihood_p)

V, logprior, loglikelihood = train_naive_bayes(training, classes)

# print(V)
# print(logprior)
# print(loglikelihood[0])
# print(loglikelihood[1])

ds = [loglikelihood[0], loglikelihood[1]]
d = {}
for k in loglikelihood[0].keys():
  d[k] = tuple(d[k] for d in ds)
with open("positive_negative_data/Database.json", "w") as database:
    json.dump(d, database)

with open("positive_negative_data/logprior.json", "w") as f:
    json.dump(logprior, f)

with open("positive_negative_data/Vocabulary.json", "w") as f:
    json.dump(V, f)

# naive_bayes_test(testing)





