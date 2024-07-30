from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import openai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import spacy
from keybert import KeyBERT
import json
import random
from summarize import get_entities, summarize_text, add_custom_target_rules
from scrape_articles import fetch_html_content, get_article_links, article_contents

# Load SpaCy english model
nlp = spacy.load("en_core_web_sm")

def extract_named_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def extract_key_phrases(text):
    key_phrases = keyword_model.extract_keywords(text)
    return key_phrases

# load the articles from the json file
with open('article_results/articles.json', 'r') as file:
    articles = json.load(file)

# initialize keybert model
keyword_model = KeyBERT()
def extract_key_phrases(text):
    key_phrases = keyword_model.extract_keywords(text)
    return key_phrases

app = FastAPI()

class Article(BaseModel):
    text: str

@app.post("/analyze")
def analyze_article(article: Article):
    entities = extract_named_entities(article.text)
    key_phrases = extract_key_phrases(article.text)
    return {"entities": entities, "key_phrases": key_phrases}

@app.get("/articles")
def analyze_all_articles():
    results = []
    for article in articles:
        entities = extract_named_entities(article['content'])
        key_phrases = extract_key_phrases(article['content'])
        results.append({"entities": entities, "key_phrases": key_phrases})
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)