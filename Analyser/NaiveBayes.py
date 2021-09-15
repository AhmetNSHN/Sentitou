import json
import re
import openpyxl
import pandas as pd
from nltk.corpus import stopwords


def safe_div(x, y):
    if y == 0:
        return 0
    return x / y


class Predict:
    def __init__(self, parent, document_adress, data):
        self.data = data
        self.parent = parent
        self.document_adress = document_adress

        with open('positive_negative_data/logprior.json', "r") as f:
            self.logprior_sentiment = json.load(f)

        with open('positive_negative_data/Vocabulary.json', "r") as f:
            self.V_sentiment = json.load(f)

        with open("positive_negative_data/Database.json", "r") as f:
            self.loglikelihood_sentiment = json.load(f)

        with open('aspect_based_data/logprior.json', "r") as f:
            self.logprior_category = json.load(f)

        with open('aspect_based_data/Vocabulary.json', "r") as f:
            self.V_category = json.load(f)

        with open("aspect_based_data/Database.json", "r") as f:
            self.loglikelihood_category = json.load(f)

    def extractData(self):
        df = pd.read_excel(self.document_adress, names=["Review"], header=None)
        review_list = df.Review.to_list()

        for x in range(len(review_list)):
            review_list[x] = str(review_list[x]).split(". ")

        for row_number in range(0, len(review_list)):
            for sentence in range(0, len(review_list[row_number])):
                review_list[row_number][sentence] = re.sub(r'[^a-zA-Z ]', '',
                                                           review_list[row_number][sentence].lower()).strip()
                review_list[row_number][sentence] = review_list[row_number][sentence].split()

        # [word for word in review_list[row_number][sentence].split() if len(word) > 5]
        print("non-ascii characters removed and characters changed to lowercase")

        all_stopwords = stopwords.words('english')
        all_stopwords.append("ms")
        all_stopwords.append("us")

        s_word_cloud = ""

        for row_number in range(0, len(review_list)):
            for sentence in range(0, len(review_list[row_number])):
                review_list[row_number][sentence] = [word for word in review_list[row_number][sentence] if
                                                     word not in all_stopwords and len(word) > 2]

        for row_number in range(0, len(review_list)):
            review_list[row_number] = list(filter(None, review_list[row_number]))
            for sentence in review_list[row_number]:
                s_word_cloud = s_word_cloud + " ".join(sentence)
        print("stopwords removed")

        return s_word_cloud, review_list

    def Calculate(self):

        s_word_cloud, data = self.extractData()
        sentence_counter = [0 for _ in range(6)]
        positive_counter = [0 for _ in range(6)]
        category_check = [False] * 5
        category_counter = [0 for _ in range(6)]
        total_size = len(data)
        category_counter[5] = total_size
        progression = 0

        for review in data:
            progression += 1
            self.parent.progress_bar["value"] = progression / total_size
            category_check = [False] * 5

            for sentence in review:
                sentence_counter[5] += 1  # overall
                sentiment, category = self.Naive_Bayes(sentence)

                if category == 0:  # Room
                    sentence_counter[0] += 1
                    category_check[0] = True
                    if sentiment == 1:
                        positive_counter[0] += 1
                        positive_counter[5] += 1

                elif category == 1:  # food
                    sentence_counter[1] += 1
                    category_check[1] = True
                    if sentiment == 1:
                        positive_counter[1] += 1
                        positive_counter[5] += 1

                elif category == 2:  # staff
                    sentence_counter[2] += 1
                    category_check[2] = True
                    if sentiment == 1:
                        positive_counter[2] += 1
                        positive_counter[5] += 1

                elif category == 3:  # pool/sea
                    sentence_counter[3] += 1
                    category_check[3] = True
                    if sentiment == 1:
                        positive_counter[3] += 1
                        positive_counter[5] += 1

                elif category == 4:  # price
                    sentence_counter[4] += 1
                    category_check[4] = True
                    if sentiment == 1:
                        positive_counter[4] += 1
                        positive_counter[5] += 1

            for x in range(0, 5):
                if category_check[x]:
                    category_counter[x] += 1

        return s_word_cloud, [int(safe_div(positive_counter[0], sentence_counter[0]) * 100),
                              int(safe_div(positive_counter[1], sentence_counter[1]) * 100),
                              int(safe_div(positive_counter[3], sentence_counter[3]) * 100),
                              int(safe_div(positive_counter[4], sentence_counter[4]) * 100),
                              int(safe_div(positive_counter[2], sentence_counter[2]) * 100),
                              int(safe_div(positive_counter[5], sentence_counter[5]) * 100)], category_counter

    def Naive_Bayes(self, data):

        # Initialize logpost[ci]: stores the posterior probability for class ci
        classes = [0, 1]
        logpost_sentiment = [None] * len(classes)

        print(data)

        for ci in classes:
            sumloglikelihoods = 0

            for word in data:
                if word in self.V_sentiment:
                    # This is sum represents log(P(w|c)) = log(P(w1|c)) + log(P(wn|c))
                    sumloglikelihoods += self.loglikelihood_sentiment[word][ci]

            # Computes P(c|d)
            logpost_sentiment[ci] = self.logprior_sentiment[ci] + sumloglikelihoods
            # print(logpost_sentiment[ci])

        classes = [0, 1, 2, 3, 4]
        logpost_category = [None] * len(classes)

        for ci in classes:
            sumloglikelihoods2 = 0

            for word in data:
                if word in self.V_category:
                    # This is sum represents log(P(w|c)) = log(P(w1|c)) + log(P(wn|c))
                    sumloglikelihoods2 += self.loglikelihood_category[word][ci]

            # Computes P(c|d)
            logpost_category[ci] = self.logprior_category[ci] + sumloglikelihoods2
            # print(logpost_category[ci])

        # Return the class that generated max ĉ
        sentiment = logpost_sentiment.index(max(logpost_sentiment))
        category = logpost_category.index(max(logpost_category))
        print(f" class -> {sentiment} \n category -> {category}")
        return sentiment, category
