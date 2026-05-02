# ECB-Text-Analysis
Python-based text analysis of ECB Monetary Policy Statement from 18 December 2025
# 1. ECB page selected
For this analysis, I selected the monetary policy statement of 18 December 2025 published by the European Central Bank. This document was chosen because it represents the end-of-year assessment by the Governing Council and provides a comprehensive overview of inflation developments, economic growth, and monetary policy projections for the years ahead.
# 2. Sentiment analysis tool
I used the TextBlob library to conduct the sentiment analysis.
Why TextBlob? TextBlob is well suited for introductory-level sentiment analysis of formal and objective texts, in contrast to tools such as VADER, which are primarily designed for social media and informal language. TextBlob provides a simple polarity score ranging from −1.0 to +1.0 based on standard linguistic lexicons. This approach allowed me to assess sentiment at the paragraph level and avoid the “saturation effect” that can occur when a long document is analysed as a single block of text.
# 3. Interpretation of paragraph-level results
By splitting the text into individual paragraphs, the analysis reveals a clear narrative structure in the ECB’s communication.

Tone:

Sentiment scores remain largely neutral in the opening paragraphs, which focus on factual decisions by the Governing Council regarding interest rates and the end-of-year economic assessment. The tone becomes increasingly cautious, with lower polarity scores, in the middle and later paragraphs. This shift corresponds to sections where the Governing Council discusses risks to the economic outlook and heightened uncertainty associated with the macroeconomic transition into 2026.

Topic Focus:

Using word frequency analysis combined with customised stop-word filtering (removing terms such as “inflation”, “monetary”, and “policy” to highlight underlying themes), the results show a strong and consistent emphasis on balancing economic growth, price stability, and expectations. Paragraph-level segmentation demonstrates that the ECB deliberately moves from a declarative and factual tone when presenting monetary policy decisions to a more analytical and cautious tone when addressing potential economic headwinds for the year ahead.
## Repository Structure
* `ecb_press_conference.txt`: The cleaned text file from the 18 December 2025 statement.
* `paragraph_sentiment.csv`: Sentiment scores calculated at the paragraph level.
* `top_words.csv`: The most frequent words found in the document.
* `wordcloud.png`: A visualization of the document's key themes.
* `analysis.py`: The main script used to perform the scraping, sentiment analysis, and visualization.
