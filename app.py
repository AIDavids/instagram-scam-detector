
import os
import sys
import subprocess

# Try to import joblib, otherwise install it
try:
    import joblib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "joblib"])
    import joblib



import streamlit as st
import joblib
import pandas as pd
from scipy.sparse import hstack, csr_matrix

# === Load model and vectorizer ===
model = joblib.load("logreg_calibrated_model.joblib")
vectorizer = joblib.load("tfidf_vectorizer.joblib")

# === Helper functions for numeric features ===
def count_emojis(text):
    return sum(char in "😀😃😄😁😆😅😂🤣😊😍😘😎👍🔥💯✅📲💵🎁🎉" for char in text)

def punctuation_ratio(text):
    if len(text) == 0:
        return 0
    puncts = sum(char in "!?.," for char in text)
    return puncts / len(text)

def has_link(text):
    return int("http" in text or "www" in text)

def prepare_features(texts):
    df = pd.DataFrame({"text": texts})
    df["length"] = df["text"].str.len()
    df["word_count"] = df["text"].str.split().apply(len)
    df["emoji_count"] = df["text"].apply(count_emojis)
    df["punct_ratio"] = df["text"].apply(punctuation_ratio)
    df["has_link"] = df["text"].apply(has_link)

    X_tfidf = vectorizer.transform(df["text"])
    numeric_feats = csr_matrix(df[["length","word_count","emoji_count","punct_ratio","has_link"]].values)
    return hstack([X_tfidf, numeric_feats])

# === Streamlit UI ===
st.title("📱 Instagram Scam Detector")
st.write("Paste an Instagram caption or message to check if it's a scam or legit.")

user_input = st.text_area("Enter caption here:")

if st.button("Predict"):
    if user_input.strip():
        X_new = prepare_features([user_input])
        pred = model.predict(X_new)[0]
        prob = model.predict_proba(X_new)[0][1]  # probability of scam

        if pred == 1:
            st.error(f"⚠️ Scam detected! (Confidence: {prob:.2%})")
        else:
            st.success(f"✅ Looks safe. (Scam probability: {prob:.2%})")
