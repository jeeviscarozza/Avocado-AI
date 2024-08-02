from summarize import summarize_text, get_entities

def process_article(article_text):
    entities = get_entities(article_text)
    summary = summarize_text(article_text)
    return entities, summary