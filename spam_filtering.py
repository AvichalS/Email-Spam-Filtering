# -*- coding: utf-8 -*-
"""Spam filtering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A9JfR1deUg3b1bNdU2_sREc7sfzfr22x
"""

import pandas as pd
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# Load the CSV file
file_path = input("Please enter the path of your CSV file: ")
df = pd.read_csv(file_path)

# Check the number of emails in the dataset
num_emails = len(df)
print(f"\nLoaded {num_emails} emails from the dataset.")

# Separate the input features (email text) and the target variable (spam/ham)
X = df['email_text']
y = df['spam']

# Remove stop words from the input features using NLTK
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
X = X.apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))

# Vectorize the input features using the CountVectorizer
vectorizer = CountVectorizer()
X_vect = vectorizer.fit_transform(X)

# Split the data into training and testing sets
test_size = float(input("\nPlease enter the test size (between 0 and 1): "))
random_state = int(input("Please enter a random seed: "))
X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=test_size, random_state=random_state)

# Train the Multinomial Naive Bayes model
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

# Evaluate the model on the testing set
y_pred = nb_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label='spam')
recall = recall_score(y_test, y_pred, pos_label='spam')
f1 = f1_score(y_test, y_pred, pos_label='spam')

print("\n------------------- Results -------------------")
print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1 Score:", round(f1, 4))
print("------------------------------------------------")

# Prompt the user to input text to classify as spam or ham
while True:
    input_text = input("\nPlease enter some text to classify as spam or ham (or 'quit' to exit): ")
    if input_text.lower() == 'quit':
        break
    else:
        # Preprocess the input text
        input_text = ' '.join([word for word in input_text.split() if word.lower() not in stop_words])
        input_vect = vectorizer.transform([input_text])

        # Predict the class of the input text
        prediction = nb_model.predict(input_vect)[0]

        # Print the prediction
        if prediction == 'spam':
            print("\nThe input text is classified as spam.")
        else:
            print("\nThe input text is classified as ham.")

# Load the data
df = pd.read_csv('spam.csv', usecols=['spam', 'email_text'])

# Convert the labels to binary values
df['spam'] = df['spam'].apply(lambda x: 1 if x == 'spam' else 0)

# Create the count vectorizer
vectorizer = CountVectorizer(stop_words='english')

# Fit and transform the text data
X_vect = vectorizer.fit_transform(df['email_text'])

# Create a DataFrame with the feature names and their corresponding word counts for spam and ham emails
feature_names = list(vectorizer.vocabulary_.keys())
spam_word_counts = X_vect[df['spam'] == 1].sum(axis=0).A1
ham_word_counts = X_vect[df['spam'] == 0].sum(axis=0).A1
word_counts_df = pd.DataFrame({'word': feature_names, 'spam_count': spam_word_counts, 'ham_count': ham_word_counts})

# Get the top 10 most frequent words in spam and ham messages
top_10_spam_words = word_counts_df.sort_values('spam_count', ascending=False).head(10)
top_10_ham_words = word_counts_df.sort_values('ham_count', ascending=False).head(10)

# Plot the bar charts for the top 10 most frequent words in spam and ham messages
fig, axs = plt.subplots(2, figsize=(10, 10))
axs[0].bar(top_10_spam_words['word'], top_10_spam_words['spam_count'])
axs[0].set_title('Most Frequent Words in Spam Messages')
axs[1].bar(top_10_ham_words['word'], top_10_ham_words['ham_count'])
axs[1].set_title('Most Frequent Words in Ham Messages')
plt.show()

