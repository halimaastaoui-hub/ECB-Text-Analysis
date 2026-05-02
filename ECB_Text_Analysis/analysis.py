import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
import os

# Ensure NLTK data is downloaded
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# 1. Scraping the ECB Monetary Policy Statement
url = "https://www.ecb.europa.eu/press/press_conference/monetary-policy-statement/2026/html/ecb.is260205~50858cb986.en.html"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the main content area (robust selection)
# ECB pages often keep the main text in 'main', 'article', or a div with class 'section'
content_area = soup.find('main') or soup.find('article') or soup.find('div', class_='section')

if content_area:
    paragraphs = [p.get_text(strip=True) for p in content_area.find_all('p') if len(p.get_text(strip=True)) > 50]
else:
    # Fallback to searching the whole body if specific containers are missing
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 50]

# Save cleaned text
with open('cleaned_press_conference.txt', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(paragraphs))

# 2. Paragraph-level Sentiment Analysis
data = []
for i, p in enumerate(paragraphs):
    analysis = TextBlob(p)
    data.append({
        'paragraph_id': i + 1,
        'text': p[:100] + "...", # Truncated for readability
        'sentiment': analysis.sentiment.polarity
    })

df = pd.DataFrame(data)
df.to_csv('press_conference_sentiment.csv', index=False)

# 3. Word Frequency and Word Cloud
stop_words = set(stopwords.words('english'))
all_text = " ".join(paragraphs).lower()
# Clean text: keep only letters
words = re.findall(r'\b[a-z]{4,}\b', all_text) 
filtered_words = [w for w in words if w not in stop_words]

# Save word frequency
word_counts = Counter(filtered_words)
freq_df = pd.DataFrame(word_counts.most_common(20), columns=['word', 'count'])
freq_df.to_csv('press_conference_word_freq.csv', index=False)

# Generate Word Cloud
wc = WordCloud(width=800, height=400, background_color='white').generate(" ".join(filtered_words))
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
wc.to_file('press_conference_wordcloud.png')

print("Success! Created: cleaned_press_conference.txt, press_conference_sentiment.csv, press_conference_word_freq.csv, press_conference_wordcloud.png")