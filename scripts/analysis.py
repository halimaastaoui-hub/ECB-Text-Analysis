import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud
import os

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

url = "https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2025/html/ecb.is251218~3a10402adb.en.html"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')
# Targeted selector for ECB article content
content_area = soup.select_one('main div.section') or soup.find('main')
paragraphs = [p.get_text(strip=True) for p in content_area.find_all('p') if len(p.get_text(strip=True)) > 50]

os.makedirs('data', exist_ok=True)
file_path = 'data/ecb_press_conference.txt'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write("\n\n".join(paragraphs))

data = []
for i, p in enumerate(paragraphs):
    blob = TextBlob(p)
    data.append({
        'paragraph_number': i + 1,
        'paragraph_text': p[:100] + "...", 
        'sentiment_score': blob.sentiment.polarity
    })

os.makedirs('outputs', exist_ok=True)
pd.DataFrame(data).to_csv('outputs/paragraph_sentiment.csv', index=False)

stop_words = set(stopwords.words('english'))
custom_stops = {'ecb', 'euro', 'area', 'monetary', 'policy', 'inflation', 'per', 'cent', 'today'}
all_text = " ".join(paragraphs).lower()
words = [w for w in nltk.word_tokenize(all_text) if w.isalpha() and w not in stop_words and w not in custom_stops]

word_counts = Counter(words)
pd.DataFrame(word_counts.most_common(20), columns=['word', 'count']).to_csv('outputs/top_words.csv', index=False)

wc = WordCloud(width=800, height=400, background_color='white').generate(" ".join(words))
wc.to_file('outputs/wordcloud.png')

print("Analysis complete. Check 'data/' and 'outputs/' folders.")