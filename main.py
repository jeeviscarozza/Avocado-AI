from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import medspacy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import spacy
from keybert import KeyBERT
import json
import random
from transformers import pipeline
from summarize import get_entities, summarize_text, add_custom_target_rules
from scrape_articles import fetch_html_content, get_article_links, article_contents
import uvicorn
from fastapi import BackgroundTasks

# main.py

nlp = medspacy.load()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


class ArticleInput(BaseModel):
    title: str
    date: str
    url: str
    content: str

app = FastAPI()

# function to extract entities
def get_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# function to summarize text
def summarize_text(text):
    summary = summarizer(text, max_length=200, min_length=100, do_sample=False)
    return summary[0]['summary_text']

@app.post("/process_article/")
def process_article(article: ArticleInput):
    entities = get_entities(article.content)
    summary = summarize_text(article.content)
    return {
        "title": article.title,
        "date": article.date,
        "url": article.url,
        "entities": entities,
        "summary": summary
    }
