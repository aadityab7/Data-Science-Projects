## Overview

The goal of this project is to detect fraudulent credit card transactions with high accuracy using anomaly detection algorithms.

**✔ 1. Data Extraction and Cleaning**
* Loading Data 
* dealing with Null values and duplicates

**✔ 2. EDA (Exploratory Data Analysis)**
* overview of data and understanding data using statistics 
* visualizing distributions using scatter plots and histograms 

**✔ 3. Data Preprocessing and Feature Engineering**
* Normalization of 'Amount' using Standard Scaler and MinMax Scaler
* Creating a new 'Hour' feature from 'Time'
* Remove non-useful features

**✔ 4. Model Building**
* Seperate input features and targets
* Split data into Train and Test sets
* Handling Imbalanced Class Distribution using SMOTE
* Creating Models 
    * Isolation Forest
    * Logistic Regression    
* Evaluation using Precision, Recall, F1 Score and Confusion Matrix
* Model Selection

**✔ 5. Exporting Final Model for Deployment**
* Training the final selected Model on complete dataset for better performance
* Save the Model Object as Byte file for making predictions later
