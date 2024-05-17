import requests
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to validate website response
def validate_response(response):
    if response.status_code == 200:
        return True
    else:
        logging.error(f"Error: Failed to retrieve webpage. Status code: {response.status_code}")
        return False

# Function to scrape question-answer pairs from a webpage
def scrape_data(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            if validate_response(response):
                soup = BeautifulSoup(response.content, 'html.parser')

                # Target specific elements containing question-answer pairs


                # (Customize this part based on the website's structure)
                pairs = soup.find_all("div", class_="faq-item")  # Example targeting a hypothetical "faq-item" class

                questions = []
                answers = []

                for pair in pairs:
                    question = pair.find("h4").text.strip()
                    answer = pair.find("p").text.strip()
                    questions.append(question)
                    answers.append(answer)

                return questions, answers
            else:
                retries += 1
                logging.warning(f"Retrying scraping for {url} (Attempt {retries}/{max_retries})")
                time.sleep(random.uniform(1, 5))  # Introduce a random delay before retrying
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
            retries += 1
            logging.warning(f"Retrying scraping for {url} (Attempt {retries}/{max_retries})")
            time.sleep(random.uniform(1, 5))  # Introduce a random delay before retrying

    logging.error(f"Failed to scrape data from {url} after {max_retries} attempts.")
    return [], []

# Preprocess the data
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = ' '.join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])  # Perform lemmatization
    return text

# Load data from scraping (replace URLs with relevant gprMax website pages)
faq_url = "https://www.gprmax.com/faq"
tutorials_url = "https://www.gprmax.com/tutorials"

questions, answers = scrape_data(faq_url)
logging.info(f"Scraped {len(questions)} question-answer pairs from {faq_url}")

tutorial_questions, tutorial_answers = scrape_data(tutorials_url)
questions += tutorial_questions
answers += tutorial_answers
logging.info(f"Scraped {len(tutorial_questions)} question-answer pairs from {tutorials_url}")

# Remove duplicates
unique_qa_pairs = list(set(zip(questions, answers)))
questions, answers = zip(*unique_qa_pairs)``
logging.info(f"Removed {len(questions) - len(unique_qa_pairs)} duplicate question-answer pairs.")

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
    user_query = preprocess(user_query)
    user_query_embedding = sentence_transformer.encode([user_query])[0]

    similarities = cosine_similarity([user_query_embedding], question_embeddings).flatten()
    top_indices = similarities.argsort()[::-1]

    responses = []
    for i in top_indices:
        if similarities[i] >= threshold:
            response = f"Question: {preprocessed_questions[i]}\nAnswer: {preprocessed_answers[i]}"
            responses.append(response)
        else:
            break

    if responses:
        return '\n\n'.join(responses)
    else:
        return "I'm sorry, I couldn't find a relevant answer for your query. Please rephrase your question or provide more details."

# Example usage
user_query = "What are the system requirements for gprMax?"
response = get_response(user_query, question_embeddings, preprocessed_questions, answer_embeddings, preprocessed_answers)
print("Response:\n", response)