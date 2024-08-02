import json
import spacy
from keybert import KeyBERT
import medspacy
from medspacy.preprocess import PreprocessingRule, Preprocessor
from medspacy.ner import TargetRule
from medspacy.context import ConTextRule
from medspacy.section_detection import Sectionizer
from medspacy.postprocess import PostprocessingRule, PostprocessingPattern, Postprocessor
from medspacy.postprocess import postprocessing_functions
from medspacy.visualization import visualize_ent, visualize_dep
from medspacy.ner import TargetMatcher
from transformers import pipeline

def add_custom_target_rules(nlp, target_rules):
    target_matcher = nlp.get_pipe("medspacy_target_matcher")
    target_matcher.add(target_rules)

# function to get entities
def get_entities(text, nlp):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities

# for getting the keywords using keybert
def keywords_text(text,model):
    model = KeyBERT('distilbert-base-nli-mean-tokens')
    keywords = model.extract_keywords(text)
    return keywords

# to summarize the text
def summarize_text(text):
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")
    #max_input_length = 1024  # Maximum length for the model
    #truncated_text = text[:max_input_length]  # Truncate the text
    summary = summarizer(text, max_length=200, min_length=30, do_sample=False)
    return summary[0]['summary_text']


def load_articles(file_path):
    with open(file_path, 'r') as file:
        articles = json.load(file)
    return articles

target_rules = [
    # Symptoms
    TargetRule("cramping", "SYMPTOM"),
    TargetRule("mood swings", "SYMPTOM"),
    TargetRule("fatigue", "SYMPTOM"),
    TargetRule("headaches", "SYMPTOM"),
    TargetRule("breast tenderness", "SYMPTOM"),
    TargetRule("nausea", "SYMPTOM"),

    # Conditions
    TargetRule("menstrual cramps", "CONDITION"),
    TargetRule("endometriosis", "CONDITION"),
    TargetRule("polycystic ovary syndrome", "CONDITION", pattern=[
        {"LOWER": "pcos"}
    ]),
    TargetRule("uterine fibroids", "CONDITION"),
    TargetRule("irregular periods", "CONDITION"),
    TargetRule("menopause", "CONDITION"),
    TargetRule("premenstrual syndrome", "CONDITION", pattern=[
        {"LOWER": "pms"}
    ]),
    TargetRule("premenstrual dysphoric disorder", "CONDITION", pattern=[
        {"LOWER": "pmdd"}
    ]),
    TargetRule("dysmenorrhea", "CONDITION"),
    TargetRule("amenorrhea", "CONDITION"),
    TargetRule("oligomenorrhea", "CONDITION"),
    TargetRule("menorrhagia", "CONDITION"),
    TargetRule("metrorrhagia", "CONDITION"),
    TargetRule("dyspareunia", "CONDITION"),
    TargetRule("vaginismus", "CONDITION"),
    TargetRule("vulvodynia", "CONDITION"),
    TargetRule("vaginitis", "CONDITION"),
    TargetRule("cervicitis", "CONDITION"),
    TargetRule("pelvic inflammatory disease", "CONDITION", pattern=[
        {"LOWER": "pid"}
    ]), 
    TargetRule("bacterial vaginosis", "CONDITION", pattern=[
        {"LOWER": "bv"}
    ]),
    TargetRule("yeast infection", "CONDITION"),
    TargetRule("cervical dysplasia", "CONDITION"),
    TargetRule("cervical cancer", "CONDITION"),
    TargetRule("ovarian cysts", "CONDITION"),
    TargetRule("ovarian cancer", "CONDITION"),
    TargetRule("breast cancer", "CONDITION"),
    TargetRule("infertility", "CONDITION"),
    TargetRule("ectopic pregnancy", "CONDITION"),
    TargetRule("miscarriage", "CONDITION"),
    TargetRule("stillbirth", "CONDITION"),
    TargetRule("preterm birth", "CONDITION"),
    TargetRule("low birth weight", "CONDITION"),
    TargetRule("preeclampsia", "CONDITION"),
    TargetRule("gestational diabetes", "CONDITION"),
    TargetRule("postpartum depression", "CONDITION"),
    TargetRule("postpartum psychosis", "CONDITION"),
    TargetRule("postpartum thyroiditis", "CONDITION"),
    TargetRule("postpartum hemorrhage", "CONDITION"),
    TargetRule("postpartum preeclampsia", "CONDITION"),
    TargetRule("postpartum eclampsia", "CONDITION"),
    TargetRule("postpartum cardiomyopathy", "CONDITION"),
    TargetRule("postpartum infections", "CONDITION"),
    TargetRule("postpartum psychosis", "CONDITION"),
    TargetRule("postpartum anxiety", "CONDITION"),
    TargetRule("postpartum OCD", "CONDITION"),
    TargetRule("postpartum PTSD", "CONDITION"),
    TargetRule("postpartum bipolar disorder", "CONDITION"),
    TargetRule("postpartum schizophrenia", "CONDITION"),
    TargetRule("postpartum mania", "CONDITION"),
    TargetRule("postpartum hypomania", "CONDITION"),
    TargetRule("postpartum depression", "CONDITION"),
    TargetRule("postpartum anxiety", "CONDITION"),
    TargetRule("postpartum OCD", "CONDITION"),

    # Hormones
    TargetRule("estrogen", "HORMONE"),
    TargetRule("progesterone", "HORMONE"),
    TargetRule("follicle-stimulating hormone", "HORMONE", pattern=[
        {"LOWER": "fsh"}
    ]),
    TargetRule("luteinizing hormone", "HORMONE", pattern=[
        {"LOWER": "lh"}
    ]),

    # Treatments/Medications
    TargetRule("birth control", "TREATMENT"),
    TargetRule("hormone replacement therapy", "TREATMENT"),
    TargetRule("pain relievers", "TREATMENT"),
    TargetRule("antidepressants", "TREATMENT"),

    # General Concepts
    TargetRule("menstruation", "CONCEPT"),
    TargetRule("contraception", "CONCEPT"),
    TargetRule("pregnancy", "CONCEPT"),
    TargetRule("ovulation", "CONCEPT"),
    TargetRule("fertilization", "CONCEPT"),
    TargetRule("implantation", "CONCEPT"),
    TargetRule("labor", "CONCEPT"),
    TargetRule("delivery", "CONCEPT"),
    TargetRule("postpartum", "CONCEPT"),
    TargetRule("menopause", "CONCEPT"),
    TargetRule("hysterectomy", "CONCEPT"),
    TargetRule("mastectomy", "CONCEPT"),
    TargetRule("ovarian removal", "CONCEPT"),
    TargetRule("cervical removal", "CONCEPT"),
    TargetRule("vaginal removal", "CONCEPT"),
    TargetRule("hormone replacement therapy", "CONCEPT"),
    TargetRule("breastfeeding", "CONCEPT"),
    TargetRule("menstrual cycle", "CONCEPT"),

    # Sexual Health
    TargetRule("sexually transmitted infections", "CONDITION", pattern=[
        {"LOWER": "sti"},
        {"LOWER": "std"}
    ]),
    TargetRule("chlamydia", "CONDITION"),
    TargetRule("gonorrhea", "CONDITION"),
    TargetRule("syphilis", "CONDITION"),
    TargetRule("herpes", "CONDITION"),
    TargetRule("human papillomavirus", "CONDITION", pattern=[
        {"LOWER": "hpv"}
    ]),
    TargetRule("HIV", "CONDITION", pattern=[
        {"LOWER": "hiv"}
    ]),
    TargetRule("AIDS", "CONDITION", pattern=[
        {"LOWER": "aids"}
    ]),
    TargetRule("safe sex", "CONCEPT"),
    TargetRule("condom", "TREATMENT"),
    TargetRule("lubricant", "TREATMENT"),
    TargetRule("sexual health", "CONCEPT"),
    TargetRule("sexual activity", "CONCEPT"),
    TargetRule("sexual intercourse", "CONCEPT"),
    TargetRule("sexual dysfunction", "CONDITION"),
    TargetRule("erectile dysfunction", "CONDITION"),
    TargetRule("libido", "CONCEPT"),
    TargetRule("sex drive", "CONCEPT"),
    TargetRule("sexual arousal", "CONCEPT"),
    TargetRule("sexual pleasure", "CONCEPT"),
    TargetRule("orgasm", "CONCEPT"),
    TargetRule("anorgasmia", "CONDITION"),
    TargetRule("dyspareunia", "CONDITION"),
    TargetRule("vaginismus", "CONDITION"),
    TargetRule("erectile disorder", "CONDITION"),
    TargetRule("premature ejaculation", "CONDITION"),
]

def save_results(results, output_file):
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=2)

def main():
    
    input_file_path = 'article_results/articles.json' # adjust here!
    output_file_path = 'article_results/analyzed_articles.json' #adjust here

    articles = load_articles(input_file_path)

    # Load the medSpaCy model
    nlp = medspacy.load()
    add_custom_target_rules(nlp, target_rules)

    # KEYBERT MODEL
    model = KeyBERT('distilbert-base-nli-mean-tokens')

    results = []
    for article in articles:
        # entities
        text = article['content']
        entities = get_entities(text, nlp)
        # keywords
        keywords = keywords_text(text, model)
        # summarize
        summary = summarize_text(text)
        # print the results
        print(f"Title: {article['title']}")
        print("Entities:", entities)
        print("Keywords:", keywords)
        print("Summary:", summary)
        print()
        results.append({
            'title': article['title'],
            'url': article['url'],
            'publication_date': article['date'],
            'entities': entities,
            'keywords': keywords,
            'summary': summary
        })
        save_results(results, output_file_path)

if __name__ == "__main__":
    main()