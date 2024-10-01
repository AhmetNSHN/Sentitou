# Sentitou: Hotel Review Sentiment Analysis


Sentitou is a machine learning project designed to analyze hotel reviews. The project utilizes the Multinomial Naive Bayes classifier, a probabilistic model, to classify reviews as positive or negative and to perform aspect-based sentiment analysis across several categories.

## Classifier Details

The **Multinomial Naive Bayes** classifier observes outcomes, selects the best estimation, and returns it based on the highest probability or likelihood. In this project, the classifier is used for:
- **Positive/Negative classification**: Determines whether a review is overall positive or negative.
- **Aspect-based classification**: Analyzes specific aspects such as Food, Staff, Price, Pool/Sea, and Room.

### Training Data

- **Positive/Negative Classifier**: Trained on 10,000 hotel reviews.
- **Aspect-Based Classifier**: Trained on 200 hotel reviews categorized into five aspects:
  - Food
  - Staff
  - Price
  - Pool/Sea
  - Room

### Data Preprocessing

The training data undergoes the following preprocessing steps:
1. **Remove non-ASCII characters**: Handled using regular expressions.
2. **Convert to lowercase**: Standardizes all text to lowercase.
3. **Remove stopwords**: Filters out common words that don't contribute to sentiment analysis.

### Training Process

The training process includes:
- **Data Shuffling**: 75% of the data is used for training, while 25% is reserved for testing. This ratio applies to both the Positive/Negative and Aspect-Based classifiers.
- **Model Training**: The model calculates \( p(c) \) (prior probability) and \( p(d|c) \) (likelihood given class \( c_i \)) for each class. It then forms a vocabulary list based on the training data.
- **Output**: The training output is saved in three JSON files:
  - Vocabulary
  - Prior likelihood
  - Likelihood

These JSON files are used by the `Test_classifier` function and the `Predict` class to analyze new data.

### Performance

The model's accuracy was tested 10 times with resetting between tests:
- **Positive/Negative Classifier**: Achieved an average accuracy of 95%.
- **Aspect-Based Classifier**: Achieved an average accuracy of 92%.

## Analyzer Class

The **Analyzer** class is responsible for:
- **Data Extraction**: Fetches review data from the database. Only `.xlsx` files are processed.
- **Sentence Splitting**: Divides reviews into sentences for detailed analysis.
- **Data Cleaning**: Applies the same cleaning steps as during training.
- **Sentiment and Aspect Classification**: Uses the Naive Bayes algorithm to determine the sentiment and categorize each sentence.

### Rating Calculation

Ratings are dynamically calculated based on the frequency and sentiment of aspects mentioned in a review:
- **Multiple Mentions**: If the same aspect is mentioned multiple times, it has a stronger influence on the rating.
- **Conflicting Sentiments**: If an aspect is mentioned with both positive and negative sentiments, they neutralize each other.

The Analyzer generates data for:
- Word clouds
- Donut charts
- The number of reviews mentioning each aspect

## Project Structure

The project is developed using Object-Oriented Programming (OOP) principles. The main components include:
- **Main Window**: The primary user interface.
- **Frames**: Two classes for managing frames within the window.
- **Analyzer**: The core class responsible for processing and analyzing the reviews.

## User Interface

![User Interface](https://github.com/AhmetNSHN/sentitou/blob/master/UI.jpeg)
*Figure 1: User Interface*

## Process Flowcharts

The following flowcharts illustrate the training and analysis processes:

<p align="center">
  <img src="https://github.com/AhmetNSHN/sentitou/blob/master/flowchart%20Training.jpeg" alt="Training Flowchart" height="1000px">
  <img src="https://github.com/AhmetNSHN/sentitou/blob/master/flowchart%20analysing.jpeg" alt="Analyzing Flowchart" height="1000px">
</p>

<p align="center">Figure 2: Training Flowchart | Figure 3: Analyzing Flowchart</p>


## Data Collection

A custom bot was developed to crawl data for training our model. The source code can be found below, but please note that TripAdvisor updates platform frequently, which will affect the bot's functionality:
- **Selenium-TripAdvisorReviewScraper**: [GitHub Repository](https://github.com/AhmetNSHN/Selenium-TripAdvisorReviewScraper)

## Conclusion

Sentitou offers a robust solution for analyzing hotel reviews, providing insights into both overall sentiment and specific aspects of the customer experience. The use of a Naive Bayes classifier ensures accurate predictions, making it a valuable tool for understanding guest feedback in the tourism industry.
