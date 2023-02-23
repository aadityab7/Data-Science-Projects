## Content Based Movie Recommendation System

### Overview

Welcome to my very Movie Recommender machine learning project! 🎉

In recent years, the movie industry has experienced tremendous growth with the creation of various platforms like Netflix, Hulu, and Amazon Prime. These platforms are used to watch movies, and the most significant advantage is the ability to watch whatever one wants to watch at any time. However, with the availability of thousands of movies on these platforms, it can be difficult to decide on what to watch. This problem is what a movie recommender system aims to solve.

In this project I created a content-based movie recommender system using the TMDB 5000 dataset available on Kaggle. The TMDB 5000 dataset contains information about movies, including the title, overview / plot, genres, keywords, cast and crew.

We will suggest movies based on similarity between movies.

#### **Step 1: Data Collection / Extraction**

The first step in building a content-based movie recommender system is to collect the data. We can download the TMDB 5000 dataset from Kaggle - https://www.kaggle.com/tmdb/tmdb-movie-metadata . The dataset contains two files: a credits file and a movies file. The credits file contains information about the cast and crew, while the movies file contains information about the movies.

#### **Step 2: Data Preprocessing**

After downloading the dataset, the next step is to preprocess the data. We will merge the credits and movies files into one file, which we will use to build our recommender system. We will also remove duplicates and missing values and convert the text data into lowercase.

#### **Step 3: Feature Extraction**

The next step is to extract features from the text data.
First, we will perform Stemming to extract the base words from our data.

Then, we will use the TF-IDF vectorizer and a Count Vectorizer from sklearn to extract features from the movie plot, genres, keywords, cast and crew. 

Count vectorizer is a simple method to create a bag-of-words representation of information. 
TF-IDF stands for Term Frequency-Inverse Document Frequency. It is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus.

#### **Step 4: Similarity Calculation**
After feature extraction, we will calculate the similarity between movies based on the features extracted. 

We will use the cosine similarity metric to calculate the similarity between movies. The cosine similarity metric measures the cosine of the angle between two vectors in a multidimensional space. It ranges from -1 to 1, with 1 being the most similar.

#### **Step 5: Building the Recommender System**
The final step is to build the recommender system. We will use the cosine similarity scores to recommend movies that are similar to the input movie. 

When a user inputs a movie, the system will retrieve the top 5 similar movies based on the cosine similarity scores.
