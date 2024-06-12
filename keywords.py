import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import nltk
import random
# Make sure you have the NLTK stopwords downloaded
# nltk.download('stopwords')
# nltk.download('punkt')

def get_useragent():
    return random.choice(_useragent_list)


_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]


def download_nltk_data():
    nltk.download('stopwords')
    nltk.download('punkt')

def check_nltk_data():
    try:
        stopwords.words('english')
        word_tokenize("This is a test sentence.")
    except LookupError:
        print("NLTK data not found, downloading...")
        download_nltk_data()

def fetch_webpage(url):
    response = requests.get(url, 
        headers={
            "User-Agent": get_useragent()
        },
        timeout=1,
    )
    response.raise_for_status()
    return response.text

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()  # Remove JavaScript and CSS
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text

def is_valid(word):
    stop_words = set(stopwords.words('english')) 
    stop_words.add('lakhview')
    return word not in stop_words and len(word) > 2 and word.isalpha()

def clean_text(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if is_valid(word.lower())]
    return words

def get_ngrams(words, n):
    return list(ngrams(words, n))

def get_keywords_from_url(url):
    html_content = fetch_webpage(url)
    text = extract_text_from_html(html_content)
    cleaned_words = clean_text(text)
    # Single words
    word_freq = Counter(cleaned_words)
    
    # Bigrams
    bigrams = get_ngrams(cleaned_words, 2)
    bigram_freq = Counter(bigrams)
    
    # Trigrams
    trigrams = get_ngrams(cleaned_words, 3)
    trigram_freq = Counter(trigrams)

    return word_freq, bigram_freq, trigram_freq

def format_ngrams(counter):
    return [(' '.join(gram), freq) for gram, freq in counter.most_common()]

