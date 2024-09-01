# Sentitou: Hotel Review Analysis using Naive Bayes Classifier

Sentitou is a machine learning project that analyzes hotel reviews using a Multinomial Naive Bayes classifier. The project is designed to classify reviews as either positive or negative, and also to perform aspect-based sentiment analysis across different categories such as Food, Staff, Price, Pool/Sea, and Room.

## Overview

### Naive Bayes Classifier

The core of this project is the **Multinomial Naive Bayes** classifier, a probabilistic model that estimates the likelihood of various outcomes based on observed data. This classifier is used to:
- **Classify reviews** as positive or negative.
- **Make aspect-based analysis** to categorize reviews into specific aspects (Food, Staff, Price, Pool/Sea, and Room).

### Training Data

- **Positive/Negative Classifier**: Trained on 10,000 hotel reviews.
- **Aspect-Based Classifier**: Trained with 200 reviews for each five specific aspects total of 1000 reviews.

### Data Preprocessing

The training data undergoes a three-stage cleaning process:
1. **Removal of non-ASCII characters**: Handled using regular expressions.
2. **Conversion to lowercase**: All text is standardized to lowercase.
3. **Stopword removal**: Commonly used words that don't contribute to sentiment analysis are removed.

### Training Process

During the training phase:
- Data is shuffled, with 75% used for training and 25% reserved for testing.
- The model calculates prior probabilities \( p(c) \) for each class and the likelihood \( p(d|c) \) of observing a given feature set.
- The processed data is stored in JSON files, including Vocabulary, Prior Likelihood, and Likelihood. These files are later utilized by the "Test_classifier" function and the "predict.py" class for analysis.

### Performance

The model was tested 10 times, yielding an average accuracy of:
- **95%** for the Positive/Negative classifier.
- **92%** for the Aspect-Based classifier.

## Analyzer Class

The **Analyzer** class fetches review data from the database and processes it in the following steps:
- **Data Extraction**: Program fetch data from given .xlsx and proccess it. Other extensions are prevented. Each line is a review.
- **Sentence Splitting**: Reviews are divided into individual sentences for granular analysis.
- **Data Cleaning**: Same cleaning steps used in the training process are applied.
- **Sentiment and Aspect Classification**: The Naive Bayes algorithm first determines the sentiment, then categorizes the sentence into one of the five aspects based on the highest likelihood.

### Rating Calculation

The Analyzer class dynamically determines the rating based on the frequency and sentiment of aspects mentioned within a review. If an aspect is mentioned multiple times with conflicting sentiments, they neutralize each other.

## Project Structure

The project follows Object-Oriented Programming (OOP) principles and is structured into:
- A **Main Window** class to manage user interface.
- Two classes for managing frames embedded within the window.
- The **Analyzer** class for processing and analyzing reviews.

## User Interface

![User Interface](https://github.com/AhmetNSHN/sentitou/blob/master/UI.jpeg)
*Figure 1: User Interface*

## Flowcharts

The following flowcharts outline the training and analysis processes:

<p align="center">
  <img src="https://github.com/AhmetNSHN/sentitou/blob/master/flowchart%20Training.jpeg" alt="Training Flowchart" height="1000px">
  <img src="https://github.com/AhmetNSHN/sentitou/blob/master/flowchart%20analysing.jpeg" alt="Analyzing Flowchart" height="1000px">
</p>

<p align="center">Figure 2: Training Flowchart | Figure 3: Analyzing Flowchart</p>



## Data Collection

Training data was crawled from TripAdvisor using a custom bot:
- **Selenium-TripAdvisorReviewScraper**: [GitHub Repository](https://github.com/AhmetNSHN/Selenium-TripAdvisorReviewScraper)

## Conclusion

Sentitou provides a robust framework for analyzing hotel reviews, offering insights into both general sentiment and specific aspects of the customer experience. The use of the Naive Bayes classifier ensures accurate and reliable predictions, making it a valuable tool for businesses in the hospitality industry.

