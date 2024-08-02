# Avocado-AI

Setup:
1. Create new environment
2. Configue input and output file paths in summarize.py
    input_file_path = 'article_results/articles.json' # adjust here 
    output_file_path = 'article_results/analyzed_articles.json' # adjust here

3. Run the following commands in terminal
pip install "fastapi[all]"
pip install -r requirements.txt

4. To run app:
uvicorn main:app

make sure to run the following command in terminal:
python -m spacy download en_core_web_sm

5. Install Docker Desktop:
https://www.docker.com/products/docker-desktop/

to start executing api, run the following:
uvicorn main:app --reload


Part 1.
beautiful soup for webscraping: standard
challenges: not too many. needed to process javascript

for nlp task:
spaCy selected as its regarded as the fastest NLP framework in Python
selecting keybert for summarization. in future work would use openai


key phrases: main topic and claim

Will try medspaCy as its speifically designed for medical terminology

1. adding custom target patterns to regognize conditions, treatments, etc
custom entities: symptom
condition
treatment
difficulty is they are case sensitive
2. determined medspacy is sufficient for this task with custom targets. however process is a bit manual in this case, but since its specific to womens health, not too difficult of a task. Other pretrained models are will not extract the relevant information

Idea for the future:
would like to generate training data in the future. develop a mini dataset by handpicking articles related to womens health. use xgboost to generate a larger, labeled dataset

3. using keyBERT for extracting relevant keywords
4. Summarizing using 
T5 (Text-To-Text Transfer Transformer): A versatile model by Google

issue: token count only accepts maximum sequency of 1024

Future: training custom NER using spacy en core web sm
1. PRETRAINED MODEL spacy
entities supported might be too generic. adding custom target entities work for now. in the future we can train on labeled data
2. For summarization: training transformers. fine tuning using tensorflow or keras. I prefer tensorflow

Rule-Based Matching:

Pros:
Quick to set up.
No need for large labeled datasets.
Effective if your entities are well-defined and consistent.
Cons:
Less flexible for variations in language or unexpected terms.
Limited to the rules you define.

Project structure should look like this:
avocado_project/
│
├── main.py  # FastAPI entry point
├── processing/
│   ├── scraping
│   ├── entity_extraction
│   └── summarization
└── requirements.txt

notebooks were used for my own personal debugging
Merge branch 'main' of https://github.com/jeeviscarozza/Avocado-AI into main
Sources:

https://www.newscatcherapi.com/blog/train-custom-named-entity-recognition-ner-model-with-spacy-v3
https://github.com/vishwajeet-hogale/Webscrape-and-summarize
https://www.freecodecamp.org/news/fastapi-quickstart/#how-to-design-the-fastapi-endpoints
https://aparnamishra144.medium.com/automated-text-summarization-using-spacy-in-nlp-8750b1b6e404

Medspacy:

https://github.com/medspacy/medspacy

H. Eyre, A.B. Chapman, K.S. Peterson, J. Shi, P.R. Alba, M.M. Jones, T.L. Box, S.L. DuVall, O. V Patterson,
Launching into clinical space with medspaCy: a new clinical text processing toolkit in Python,
AMIA Annu. Symp. Proc. 2021 (in Press. (n.d.). 
http://arxiv.org/abs/2106.07799.

https://huggingface.co/docs/transformers/en/tasks/summarization