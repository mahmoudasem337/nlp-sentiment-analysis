import streamlit as st
import pandas as pd
from textblob import TextBlob

# Function to analyze sentiment
def analyze(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive Sentence"
    elif polarity == 0:
        return "Neutral Sentence"
    else:
        return "Negative Sentence"

st.markdown("""
    <style>
    /* Base styles for dark mode */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* Title style */
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    /* Remove any extra white boxes */
    .main > div:nth-child(1) > div {
        background: none !important;
        box-shadow: none !important;
    }

    /* Upload section box */
    .upload-section {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333333;
        margin-bottom: 30px;
    }

    /* Section headers like 'Sentiment Counts' */
    .section-header {
        font-size: 28px;
        color: #4A90E2;
        margin-top: 40px;
        margin-bottom: 10px;
        border-bottom: 2px solid #4A90E2;
        padding-bottom: 5px;
    }

    /* Sentiment counts in light grey */
    .sentiment-counts {
        font-size: 18px;
        color: #AAAAAA;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>

    <div class='main-title'>Sentiment Analysis</div>
""", unsafe_allow_html=True)



# File upload box
st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your file", type=["txt", "csv"])
st.markdown("</div>", unsafe_allow_html=True)

# Main analysis logic
if uploaded_file is not None:
    if uploaded_file.name.endswith(".txt"):
        text_data = uploaded_file.read().decode("utf-8")
        lines = text_data.splitlines()
    elif uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        lines = df.iloc[:, 0].dropna().tolist()
    else:
        st.error("Unsupported format")
        lines = []

    if lines:
        results = {"Positive Sentence": [], "Neutral Sentence": [], "Negative Sentence": []}
        for line in lines:
            sentiment = analyze(line)
            results[sentiment].append(line)

        # Prepare final result table
        all_results = []
        for sentiment, sentence_list in results.items():
            for sentence in sentence_list:
                all_results.append({"Text": sentence, "Sentiment": sentiment})

        # Display sentiment counts
        st.markdown("<div class='section-header'>Sentiment Counts</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sentiment-counts'>Number of the positive sentences: {len(results['Positive Sentence'])}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sentiment-counts'>Number of the neutral sentences: {len(results['Neutral Sentence'])}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sentiment-counts'>Number of the negative sentences: {len(results['Negative Sentence'])}</div>", unsafe_allow_html=True)



        # Show table
        st.markdown("<div class='section-header'> Results</div>", unsafe_allow_html=True)
        st.dataframe(all_results)

