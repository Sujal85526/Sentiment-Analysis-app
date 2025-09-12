import streamlit as st
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="💬 Sentiment Analysis App",
    page_icon="💬",
    layout="centered"
)

# Title and description
st.title("💬 Sentiment Analysis App")
st.markdown("**Analyze the sentiment of any text using multiple methods!**")
st.divider()

# Sidebar for method selection
st.sidebar.header("Analysis Settings")
method = st.sidebar.selectbox(
    "Choose Analysis Method:",
    ["TextBlob", "VADER", "Both"]
)

# Main input
st.subheader("Enter Text to Analyze")
text_input = st.text_area(
    "Type your text here...",
    placeholder="Example: I love this new technology! It's amazing.",
    height=120
)

# Analysis button
if st.button("🔍 Analyze Sentiment", type="primary"):
    if text_input:
        col1, col2 = st.columns(2)
        
        if method in ["TextBlob", "Both"]:
            with col1:
                st.subheader("📊 TextBlob Analysis")
                blob = TextBlob(text_input)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
                
                # Determine sentiment
                if polarity > 0.1:
                    sentiment = "Positive 😊"
                    color = "green"
                elif polarity < -0.1:
                    sentiment = "Negative 😢"
                    color = "red"
                else:
                    sentiment = "Neutral 😐"
                    color = "gray"
                
                st.markdown(f"**Sentiment:** :{color}[{sentiment}]")
                st.metric("Polarity Score", f"{polarity:.3f}")
                st.metric("Subjectivity Score", f"{subjectivity:.3f}")
                
        if method in ["VADER", "Both"]:
            with col2:
                st.subheader("🎯 VADER Analysis")
                analyzer = SentimentIntensityAnalyzer()
                scores = analyzer.polarity_scores(text_input)
                
                # Determine sentiment
                if scores['compound'] > 0.05:
                    sentiment = "Positive 😊"
                    color = "green"
                elif scores['compound'] < -0.05:
                    sentiment = "Negative 😢"
                    color = "red"
                else:
                    sentiment = "Neutral 😐"
                    color = "gray"
                
                st.markdown(f"**Sentiment:** :{color}[{sentiment}]")
                st.metric("Compound Score", f"{scores['compound']:.3f}")
                
                # Show detailed scores
                with st.expander("View Detailed Scores"):
                    st.write(f"Positive: {scores['pos']:.3f}")
                    st.write(f"Negative: {scores['neg']:.3f}")
                    st.write(f"Neutral: {scores['neu']:.3f}")
        
        # Show interpretation
        st.divider()
        st.subheader("📖 How to Interpret Results")
        with st.expander("Click to learn more"):
            st.write("""
            **TextBlob:**
            - Polarity: -1 (negative) to +1 (positive)
            - Subjectivity: 0 (objective) to 1 (subjective)
            
            **VADER:**
            - Compound: -1 (negative) to +1 (positive)
            - Individual scores: 0 to 1 for pos/neg/neu
            """)
    else:
        st.warning("Please enter some text to analyze!")

# Sample texts
st.divider()
st.subheader("🧪 Try Sample Texts")

# Define sample texts
sample_texts = {
    "positive": "I absolutely love this amazing product! It exceeds all my expectations and brings me so much joy. Highly recommended!",
    "negative": "This is terrible and frustrating. I hate how complicated and confusing everything is. Completely disappointed.",
    "neutral": "The weather today is partly cloudy with a temperature of 22 degrees. Traffic conditions are normal on most routes."
}

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😊 Positive Example", use_container_width=True):
        st.session_state['sample_text'] = sample_texts["positive"]

with col2:
    if st.button("😢 Negative Example", use_container_width=True):
        st.session_state['sample_text'] = sample_texts["negative"]
        
with col3:
    if st.button("😐 Neutral Example", use_container_width=True):
        st.session_state['sample_text'] = sample_texts["neutral"]

# Display the selected sample text
if 'sample_text' in st.session_state:
    st.markdown("### 📝 Sample Text Selected")
    st.text_area("Selected sample:", st.session_state['sample_text'], height=100, disabled=True)

# Footer
st.divider()
st.markdown("Built with ❤️ using Streamlit and Python")
