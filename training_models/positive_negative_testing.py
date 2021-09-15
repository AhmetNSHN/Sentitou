import re
import pandas as pd
from nltk.corpus import stopwords
from Analyser.NaiveBayes import Predict

df = pd.read_csv("../csv_test_document.csv", sep="\t", names=["Review"])
review_list = df.Review.to_list()
data = []
for x in range(len(review_list)):
    review_list[x] = review_list[x].split(". ")

for row_number in range(0, len(review_list)):
    for sentence in range(0, len(review_list[row_number])):
        review_list[row_number][sentence] = re.sub(r'[^a-zA-Z ]', '', review_list[row_number][sentence].lower()).strip()
        review_list[row_number][sentence] = review_list[row_number][sentence].split()

# [word for word in review_list[row_number][sentence].split() if len(word) > 5]
print("non-ascii characters removed and characters changed to lowercase")

all_stopwords = stopwords.words('english')
all_stopwords.append("ms")
all_stopwords.append("us")

indexes_tobe_removed = []

for row_number in range(0, len(review_list)):
    for sentence in range(0, len(review_list[row_number])):
        review_list[row_number][sentence] = [word for word in review_list[row_number][sentence] if word not in all_stopwords and len(word) > 2]

for row_number in range(0, len(review_list)):
    review_list[row_number] = list(filter(None, review_list[row_number]))

print("stopwords removed")

negative_counter = 0
positive_counter = 0

for row in review_list:
    for sentence in row:
        if Predict(sentence) == 1:
            positive_counter += 1
        else:
            negative_counter += 1

print(f"Overall document analysis %{(positive_counter/(positive_counter+negative_counter))*100}")



