# -*- coding: utf-8 -*-
"""chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1v5vUVoxDQmMNX5KyMOdMHKDmSx--Cgw-
"""

import numpy as np
import nltk
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Open and read the file
with open('/content/chatbot.txt', 'r', errors='ignore') as f:
    raw_doc = f.read().lower()  # Converts text to lowercase

# Download required NLTK data
nltk.download('punkt')  # Using the Punkt tokenizer
nltk.download('wordnet')  # Using the WordNet dictionary

# Tokenize the document into sentences and words
sent_tokens = nltk.sent_tokenize(raw_doc)  # Converts doc to list of sentences
word_tokens = nltk.word_tokenize(raw_doc)  # Converts doc to list of words

# Initialize the WordNet Lemmatizer
lemmer = nltk.stem.WordNetLemmatizer()

# Lemmatize tokens
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

# Remove punctuation and normalize text
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greetings
GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREET_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)

# Generate response using TF-IDF and cosine similarity
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]

    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        robo_response = "I am sorry! I don't understand you."
    else:
        robo_response = sent_tokens[idx]

    sent_tokens.remove(user_response)
    return robo_response

# Start the chatbot
def chatbot():
    print("BOT: My name is Tharun. Let's have a conversation! Also, if you want to exit any time, just type Bye!")


    flag = True

    while flag:
        user_response = input().lower()
        if user_response != 'bye':
            if user_response in ('thanks', 'thank you'):
                flag = False
                print("BOT: You are welcome.")
            else:
                if greet(user_response) is not None:
                    print("BOT: " + greet(user_response))
                else:
                    print("BOT: ", end="")
                    print(response(user_response))
        else:
            flag = False
            print("BOT: Goodbye! Take care <3")

if __name__ == "__main__":
    chatbot()





