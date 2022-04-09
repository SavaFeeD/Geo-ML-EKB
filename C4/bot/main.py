import re
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords

from sklearn import preprocessing
from sklearn import feature_extraction

import tensorflow
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

from intents import intents

nltk.download('all')


X_train = []
y_train = []

for intent in intents:
    tag = intent['tag']
    for pattern in intent['patterns']:
        X_train.append(pattern)
        y_train.append(tag)


class StemmedCountVectorizer(feature_extraction.text.CountVectorizer):
    def build_analyzer(self):
        stemmer = nltk.stem.PorterStemmer()
        analyzer = super().build_analyzer()

        def stemming_step(doc):
            stemmed = [stemmer.stem(w) for w in analyzer(doc)]
            stemmed = [token for token in stemmed if re.match(r'\w+', token)]
            return stemmed

        return stemming_step


vectorizer = StemmedCountVectorizer(lowercase=True, tokenizer=nltk.word_tokenize, stop_words=stopwords.words('english'))
vectorizer.fit(X_train)

labelEncoder = preprocessing.LabelEncoder()
labelEncoder.fit(list(set(y_train)))

X_train = vectorizer.transform(X_train)
y_train = labelEncoder.transform(y_train)

numOfClasses = len(labelEncoder.classes_)
numOfPatterns = (len(vectorizer.get_feature_names()),)

X_train = X_train.toarray()
y_train = to_categorical(y_train)

model = Sequential()
model.add(Dense(15, input_shape=numOfPatterns, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(numOfClasses, activation='softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

history = model.fit(X_train, y_train, epochs=500, batch_size=16)

while True:
    request = input('> ')

    tag = labelEncoder.inverse_transform(
        [model.predict(vectorizer.transform([request])).argmax()]
    )[0]

    intent = [intent for intent in intents if intent['tag'] == tag][0]
    possible_responses = intent['responses']
    print(random.choice(possible_responses))

    if 'operation' in intent.keys():
        intent['operation']()

    if tag == 'goodbye':
        break
