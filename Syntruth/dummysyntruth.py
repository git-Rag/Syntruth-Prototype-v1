# syntruth_mvp_hackathon.py
import streamlit as st
import re
import random
import os

st.set_page_config(page_title="Syntruth - AI Authenticity Detector", layout="wide")
st.title("🔍 Syntruth - AI Authenticity Detector")
st.markdown("Detect phishing emails and deepfake media in real-time!")

# ---------------------------
# Phishing detection (lightweight rule-based)
# ---------------------------
st.sidebar.header("Email Analysis")
st.sidebar.markdown("Paste your email text below:")
email_input = st.sidebar.text_area("Email Text", height=150)

def analyze_email(text):
    if not text.strip():
        return None

    suspicious_words = ["verify","login","password","urgent","bank","account","update"]
    phishing_score = 0
    flagged_links = []

    # Count suspicious words
    for word in suspicious_words:
        if word in text.lower():
            phishing_score += 15  # each word adds weight

    # Extract suspicious links
    links = re.findall(r'https?://[^\s]+', text)
    for l in links:
        if any(x in l.lower() for x in ["login","verify","secure","account"]):
            flagged_links.append(l)
            phishing_score += 20  # weight for links

    phishing_score = min(phishing_score, 100)
    return {"phishing_score": phishing_score, "flagged_links": flagged_links}

# ---------------------------
# Deepfake detection (placeholder)
# ---------------------------
st.sidebar.header("Media Analysis")
media_file = st.sidebar.file_uploader("Upload Image or Video", type=["png","jpg","jpeg","mp4"])

def analyze_media(file):
    if file is None:
        return None
    # Save temporarily
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    # Fake deepfake score for demo
    deepfake_score = round(random.uniform(20, 80), 2)
    return {"deepfake_score": deepfake_score}

# ---------------------------
# Trust score calculation
# ---------------------------
def calculate_trust(phishing=None, deepfake=None):
    scores = []
    if phishing is not None:
        scores.append(phishing)
    if deepfake is not None:
        scores.append(deepfake)
    if not scores:
        return 100
    trust = 100 - sum(scores)/len(scores)
    return round(trust,2)

# ---------------------------
# Run analysis on button click
# ---------------------------
if st.button("Analyze Input"):

    phishing_result = analyze_email(email_input)
    media_result = analyze_media(media_file)

    phishing_score = phishing_result["phishing_score"] if phishing_result else None
    deepfake_score = media_result["deepfake_score"] if media_result else None

    trust_score = calculate_trust(phishing_score, deepfake_score)

    # ---------------------------
    # Display results
    # ---------------------------
    st.subheader("🔹 Analysis Results")
    
    st.metric("Trust Score", f"{trust_score}%")
    
    if phishing_score is not None:
        st.write(f"**Phishing Risk:** {phishing_score}%")
        if phishing_result["flagged_links"]:
            st.write("⚠️ Suspicious Links Detected:")
            for link in phishing_result["flagged_links"]:
                st.write(f"- {link}")
        else:
            st.write("No suspicious links detected.")

    if deepfake_score is not None:
        st.write(f"**Deepfake Risk:** {deepfake_score}%")
        st.write("⚠️ Note: Facial/media inconsistencies detected (demo placeholder)")

    if phishing_score is None and deepfake_score is None:
        st.write("No input detected. Please provide email text or media file.")
