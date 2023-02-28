## Overview

The goal of this project is to detect fraudulent credit card transactions with high accuracy using anomaly detection algorithms.

**✔ 1. Data Extraction and Cleaning**
* Loading Data 
* dealing with Null values and duplicates

**✔ 2. EDA (Exploratory Data Analysis)**
* overview of data and understanding data using statistics 
* visualizing distributions using scatter plots and histograms 

**✔ 3. Data Preprocessing and Feature Engineering**
* Creating a new 'Hour' feature from 'Time'
* Normalization of features using:
    * Standard Scaler
    * MinMax Scaler
    * Robust Scaler
* Remove non-useful features

**✔ 4. Model Building**
* Data Preparation
    * Seperate input features and targets
    * Split data into Train and Test sets
    * Handling Imbalanced Class Distribution using SMOTE
* Defining Function to perform Model Evaluation using:
    * Precision
    * Recall
    * F1 Score
    * Confusion Matrix
* Using Cross Validation to compare different Model Performances
* Creating indivual Models to get better performance
    * Isolation Forest
    * Logistic Regression
    * KNeighbors Classifier
    * Decision Tree Classifier
* Model Selection

**✔ 5. Exporting Final Model for Deployment**
* Training the final selected Model on complete dataset for better performance
* Save the Model Object as Byte file for making predictions later
