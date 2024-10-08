import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords


# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()


tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))



st.title("SMS Spam Classifier")

# Input SMS from user
input_sms = st.text_area("Enter the message")

# Preprocess the input text
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

# Predict the label for the input text
if st.button('Predict'):
    transformed_text = transform_text(input_sms)
    vec_input = tfidf.transform([transformed_text])
    res = model.predict(vec_input)[0]
    if res == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
