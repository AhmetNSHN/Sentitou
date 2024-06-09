# Sentitou

The training model used is the Multinomial Naive Bayes classifier. The Naive Bayes classifier is a probabilistic classifier that observes outcomes, selects the best estimation, and returns it. The outcome might be the highest probability, the highest likelihood, or one of them at the required level. This classifier is used for both classifying positive and negative classes and aspect-based classes in this project. The training data includes 10,000 comments for the positive and negative classifier and 200 reviews for the aspect-based classifier (Food, Staff, Price, Pool/Sea, and Room).

The algorithm starts by clearing the training data, which consists of three stages: removing non-ASCII characters, converting lowercase characters to uppercase characters, and removing stopwords. The algorithm uses regular expressions to clear non-ASCII characters.

Training data includes 10,000 comments for the positive and negative classifier. There are five classes for the Aspect-based classifier: Food, Staff, Price, Pool/Sea, and Room. During the training phase, data is shuffled, and 75% of the training data is used to train our model, and the remaining is used to test our model. Ratios are the same for both models, the model that analyzes sentences as positive and negative, and the other model that makes aspect-based analysis. After clearing the data, the algorithm starts to train the model.

The model calculates \( p(c) \) (prior probability), then counts the total number of words for each class. It then computes \( p(d|c) \) (the probability we return class \( c_i \) given that our observation is \( d \)) and forms a vocabulary list that consists of words our model will use during execution. The algorithm divides those classes into documents, counts the number of times Word "x" appears in class document, and then calculates the likelihood for each word. At the end, the training algorithm writes its output to JSON files. The output consists of three JSON files: Vocabulary, prior likelihood, and likelihood. JSON files are later used by the "Test_classifier" function to test the model and "Predict" class created to analyze given data by the user. The same process is applied to our model making aspect-based analysis.

After training for both models, instead of using cross-validation, we tested the model 10 times by resetting it, and the averages were 95% for the positive-negative classifier and 92% for the aspect-based classifier.

![User Interface](https://github.com/AhmetNSHN/sentitou/blob/master/UI.jpeg)
Figure 1: User Interface

Our Analyzer class starts with fetching data from the database for both classifiers. It extracts data from the location given by the user. The selection of documents with extensions other than .xlsx is prevented. Reviews are divided into sentences, and analysis is done sentence by sentence. The data clearing process is done by the analyzer too. The clearing data process is the same as the training phase and can be seen in figure 2. After the clearing process, the Analyzer keeps every word to form a word cloud.

The cleared data is then passed to the Analyzer. The Analyzer keeps some counters to calculate the number of reviews for each mentioned aspect and calculate rating. Dynamics to determine the rating is as follows: if the same aspect is mentioned in several sentences in the review, then it has more power to determine the rating than other reviews. If a review has two sentences about the same aspect but one of them is positive and the other is negative, they neutralize each other. The Analyzer returns data created to draw word clouds, stats to draw donut charts and write to the text box, and the number of reviews for each aspect mentioned. Analyzer Naive Bayes algorithm, first calculates the sentiment of the sentence, then the category of it by selecting the highest likelihood between classes, and then returns both sentiment and category.

The project is written according to the Object-Oriented Programming (OOP) concept. The structure of the code is as follows: a class for the main window, two classes for frames embedded inside the window, and there is an Analyzer class.

![Training Flowchart](https://github.com/AhmetNSHN/sentitou/blob/master/flowchart%20Training.jpeg) ![Analyzing Flowchart](https://github.com/AhmetNSHN/sentitou/blob/master/flowchart%20analysing.jpeg)

Figure 2: Training Flowchart | Figure 3: Analyzing Flowchart

Bot that used to crawl training data from TripAdvisor: [Selenium-TripAdvisorReviewScraper](https://github.com/AhmetNSHN/Selenium-TripAdvisorReviewScraper)
