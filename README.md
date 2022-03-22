# sentitou
Our training model, statistical model that we used is Multinomial Naive Bayes classifier. Naive Bayes classifier is a probabilistic classifier, they observe outcomes and select and return the best estimation. The outcome might be the highest probability, the highest likelihood, or one of them at the required level. This classifier is used for both classifying positive and negative classes and aspect-based classes in our project.Training data includes 10.000 comments for positive, negative classifier and 200 review for aspect based classifier (Food, Staff, Price, Pool/Sea, and room)

The algorithm starts with clearing our training data. Clearing process consists of three stages; Removing non-ascii character, converts lower characters to uppercase characters, remove stopwords. Algorithm is using regular expressions to clear non-ascii characters.
Training data includes 10.000 comments for positive, negative classifier. aspect-based classifier on the 5 aspects. Classes for aspect-based analysis are Food, Staff, Price, Pool/Sea, and room. During Training phase data is shuffled and   ¾  of training data is used to train our model and ¼ is used to test our model. Ratios are same in our both model, models that analyzing sentence as positive and negative and other model is making aspect based analysis. After clearing data, algorithm start to train model. We have two training functions within tool for both models and it is always possible to improve the model by better training datasets. 
Our model calculates p(c) (prior probability) then count the total number of words for each class. Then we compute p(d|c) (the probability we return class ci given that our observation is d) and form a vocabulary list that consists of words our model will use during execution.  The algorithm divides those classes into documents, count number of times Word “x” appears in class document then Algorithm calculates the likelihood for each word.  At the end, Training algorithm writes its output to Json files.  Output consists of three Json files, Vocabulary, prior likelihood and likelihood. Json files later used by “Test_classifier” function to test model and Predict class created to analyse given data by user. Same process is applied to our model making aspect based analysis.
After training for both model, Instead of using cross validation, we tested model 10 times by resetting it and averages were %95 for positive, negative classifier and 92% for Aspect based classifier.





![alt text](https://github.com/AhmetNSHN/sentitou/blob/master/UI.jpeg)





Our Analyser class starts with fetching data from database for both classifiers. It extracts data from the location given by the user. Selection of other document rather that having .xlsx extension is prevented. Reviews divided into sentences and analysis done sentence by sentence. Clearing data process is done by analyzer too. Clearing data process same with training phase and can be seen in figure 1. After clearing process Analyser keep every word to form a word cloud. 
Cleared data passed to “calculate function of Analyzer. This function is managing and using “Naïve_Bayes” function of analyser and get results from there then make needed calculations. Calculate function keeps some counters to calculate the number of reviews for each mentioned aspect and calculate rating. Dynamics to determine the rating is as; if same aspect mentioned in several sentences in the review then it has more power to determine rating than other reviews. If review own two sentences about the same aspect but one of them is positive and other is negative they neutralize each other. “Calculate function returns data created to draw word cloud, stats to draw donut charts and write to the text box and the number of reviews for each aspect mentioned.
“Naïve_bayes” algorithm used by “Calculate” function is first calculates the sentiment of the sentence, then category of it by selecting the highest likelihood between classes then returns both sentiment and category to “Calculate” function of the analyser.
The project is written according to Object oriented programming (OOP) concept. Structure of the code is as; Class for main window, two classes for frames embedded inside the window and there is Analyser class. During execution of the analyser, new thread is created to prevent the UI from freezing and lost its capability. Progress bar is added and updated from Analyser executing on another thread.

![alt text](https://github.com/AhmetNSHN/sentitou/blob/master/flowchart%20Training.jpeg) ![alt text](https://github.com/AhmetNSHN/sentitou/blob/master/flowchart%20analysing.jpeg)







