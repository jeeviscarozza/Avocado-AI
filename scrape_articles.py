import os
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import time

def fetch_html_content(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = Service('/usr/local/bin/chromedriver') 
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(10)
    html_content = driver.page_source
    driver.quit()
    return html_content

def get_article_links(website):
    html_content = fetch_html_content(website)
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    for a in soup.find_all('h3', class_='flo-categories__article-title'):
        parent_link = a.find_parent('a', href=True) 
        if parent_link:
            href = parent_link['href']
            if href and href.startswith('/menstrual-cycle/'):
                links.append(f"https://flo.health{href}")
    return links[:5]

def article_contents(article_url):
    
    html_content = fetch_html_content(article_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract the title
    title_tag = soup.find('h1')  # Adjust the tag based on actual HTML
    title = title_tag.get_text(strip=True) if title_tag else 'No title'
    
    # Extract the publication date
    date_container = soup.find('div', class_='flo-article-banner-bottom__info-panel-date--item')  
    date_tag = date_container.find('span')  # Adjust the tag based on actual HTML
    date = date_tag.get_text(strip=True) if date_tag else 'No date'

    content = []

    # Define classes to search for content
    classes_to_search = [
        'flo-content__main', 
        'flo-article-text', 
        'flo-article-text__inner'
    ]

    # Extract content from the specified classes
    for class_name in classes_to_search:
        content_tags = soup.find_all(class_=class_name)
        for tag in content_tags:
            for element in tag.find_all(['p', 'h1', 'h2', 'h3']):
                content.append(element.get_text(strip=True))
        
        # Extract content under subheadings and their paragraphs
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            content.append(heading.get_text(strip=True))
            sibling = heading.find_next_sibling()
            while sibling and sibling.name == 'p':
                content.append(sibling.get_text(strip=True))
                sibling = sibling.find_next_sibling()
        
    content = " ".join(content) if content else 'No content'
        
    print(f"Title: {title}")
    print(f"URL: {article_url}")
    print(f"Date: {date}")
    print(f"Content Preview: {content}...")  

    return {
        'title': title,
        'url': article_url,
        'date': date,
        'content': content
    }

if __name__ == "__main__":

    website = 'https://flo.health/menstrual-cycle' # adjust as required

    # Get the article links from the website
    article_links = get_article_links(website)
    print(f"Article links: {article_links}")

    # Loop through the article links and extract the content
    articles = []
    for link in article_links:
        article_info = article_contents(link)
        articles.append(article_info)
        print(f"Article fetched: {article_info}")

    # Create a folder to save the results
    output_folder = 'article_results'
    os.makedirs(output_folder, exist_ok=True)

    # Save the data to a JSON file
    json_path = os.path.join(output_folder, 'articles.json')
    with open(json_path, 'w') as file:
        json.dump(articles, file, indent=2)

    # Save the data to a CSV file
    df = pd.DataFrame(articles)
    csv_path = os.path.join(output_folder, 'articles.csv')
    df.to_csv(csv_path, index=False)
