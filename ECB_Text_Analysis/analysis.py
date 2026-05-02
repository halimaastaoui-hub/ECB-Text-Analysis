import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
from collections import Counter
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. SETUP & FETCH
url = "https://www.ecb.europa.eu/press/projections/html/ecb.projections202603_ecbstaff~ebe291cd3d.en.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
content = soup.find('main')
paragraphs = [p.get_text().strip() for p in content.find_all('p') if len(p.get_text().strip()) > 50]

# 2. SAVE CLEANED TEXT
with open('cleaned_text.txt', 'w', encoding='utf-8') as f:
    for p in paragraphs:
        f.write(p + "\n\n")

# 3. SENTIMENT ANALYSIS & WORD COUNTING
data = []
all_words = []
stop_words = {"the", "and", "a", "of", "to", "in", "is", "for", "that", "on", "with", "as", "by", "are", "be", "an", "at", "was", "from", "this", "which", "would"}

for i, p in enumerate(paragraphs):
    analysis = TextBlob(p)
    data.append({'paragraph_id': i + 1, 'text': p, 'sentiment': analysis.sentiment.polarity})
    
    # Process words for word cloud/frequency
    words = p.lower().translate(str.maketrans('', '', string.punctuation)).split()
    all_words.extend([w for w in words if w not in stop_words and len(w) > 3])

# 4. SAVE CSVs
pd.DataFrame(data).to_csv('ecb_projections_analysis.csv', index=False)
word_freq = Counter(all_words).most_common(20)
pd.DataFrame(word_freq, columns=['word', 'count']).to_csv('word_frequency.csv', index=False)

# 5. GENERATE WORD CLOUD
text_for_cloud = " ".join(all_words)
wc = WordCloud(width=800, height=400, background_color='white').generate(text_for_cloud)
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.savefig('wordcloud.png')

print("All tasks complete! Check your folder for: cleaned_text.txt, ecb_projections_analysis.csv, word_frequency.csv, and wordcloud.png.")