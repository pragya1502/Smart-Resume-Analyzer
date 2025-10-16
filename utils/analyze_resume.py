import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Load default keywords
with open('models/keyword_list.txt', 'r') as f:
    default_keywords = [line.strip().lower() for line in f.readlines()]

def analyze_resume(resume_text, custom_keywords=None):
    words = [word.lower() for word in resume_text.split() if word.lower() not in stop_words]

    # Use custom job keywords if provided
    keywords = [kw.lower() for kw in custom_keywords] if custom_keywords else default_keywords

    matched = [word for word in keywords if word in words]
    missing = [word for word in keywords if word not in words]

    score = round((len(matched) / len(keywords)) * 100, 2) if keywords else 0
    return score, missing
