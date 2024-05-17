from flask import Flask, request, jsonify
import requests
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# Preprocess the data
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = ' '.join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])  # Perform lemmatization
    return text

# Function to scrape question-answer pairs from a webpage
def scrape_data(url, max_retries=3):
    # ... (scrape_data function code)

# Load data from scraping (replace URLs with relevant gprMax website pages)
faq_url = "https://www.gprmax.com/faq"
tutorials_url = "https://www.gprmax.com/tutorials"

questions, answers = scrape_data(faq_url)
tutorial_questions, tutorial_answers = scrape_data(tutorials_url)
questions += tutorial_questions
answers += tutorial_answers

# Remove duplicates
unique_qa_pairs = list(set(zip(questions, answers)))
questions, answers = zip(*unique_qa_pairs)

# Preprocess the scraped data
preprocessed_questions = [preprocess(q) for q in questions]
preprocessed_answers = [preprocess(a) for a in answers]

# Create Sentence Transformer vectorizer
sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

# Encode preprocessed questions and answers
question_embeddings = sentence_transformer.encode(preprocessed_questions)
answer_embeddings = sentence_transformer.encode(preprocessed_answers)

# Function to retrieve answers based on user query
def get_response(user_query, question_embeddings, preprocessed_questions, answer_embeddings, preprocessed_answers, threshold=0.5):
    # ... (get_response function code)

@app.route('/chatbot', methods=['POST'])
def handle_chatbot():
    user_query = request.json['query']
    response = get_response(user_query, question_embeddings, preprocessed_questions, answer_embeddings, preprocessed_answers)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()