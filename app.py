import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from phishing_detector import analyze_email
from deepfake_detector import analyze_image
from trust_engine import calculate_trust

st.set_page_config(page_title="SynTruth", page_icon="⚙️", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at 20% 30%, #0a0a0f 0%, #121225 100%);
        color: #f2f2f2;
        font-family: 'Inter', sans-serif;
    }
    .main {
        padding-top: 4rem;
    }
    .title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 1px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #b0b0ff;
        margin-top: -0.5rem;
        margin-bottom: 3rem;
    }
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 70vh;
        flex-direction: column;
    }
    .try-btn {
        background: linear-gradient(135deg, #5a00ff, #1de9b6);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem 3rem;
        border: none;
        border-radius: 2rem;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
    }
    .try-btn:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #1de9b6, #5a00ff);
    }
    </style>
""", unsafe_allow_html=True)

# --- Page Router ---
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    with st.container():
        st.markdown('<div class="center">', unsafe_allow_html=True)
        st.markdown('<h1 class="title">🧠 SynTruth</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">AI That Separates the Synthetic from the Real</p>', unsafe_allow_html=True)
        if st.button("🚀 Try SynTruth", key="try", help="Begin analyzing emails or media files"):
            st.session_state.page = "analyzer"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "analyzer":
    st.title("🔍 SynTruth Analyzer")
    st.markdown("Analyze emails or media for phishing and deepfake risk in real-time.")

    mode = st.radio("Choose Analysis Type:", ["Phishing Email", "Deepfake Image"], horizontal=True)

    if mode == "Phishing Email":
        text = st.text_area("📧 Paste Email Content Below", height=200)
        if st.button("Analyze Email"):
            if text.strip() == "":
                st.warning("Please enter some text to analyze.")
            else:
                with st.spinner("Analyzing for phishing..."):
                    result = analyze_email(text)
                    phishing_score = result["phishing_score"]
                    trust = calculate_trust(phishing=phishing_score)
                    st.subheader(f"Trust Score: {trust}%")
                    st.progress(trust / 100)
                    st.info(f"Phishing Risk: {phishing_score}%")
                    if result["links_flagged"]:
                        st.error("Suspicious Links Detected:")
                        for link in result["links_flagged"]:
                            st.write(f"- {link}")

    elif mode == "Deepfake Image":
        uploaded_file = st.file_uploader("🖼️ Upload an image for deepfake analysis", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            if st.button("Analyze Image"):
                with st.spinner("Analyzing for deepfake content..."):
                    with open("temp.jpg", "wb") as f:
                        f.write(uploaded_file.read())
                    result = analyze_image("temp.jpg")
                    deepfake_score = result["deepfake_score"]
                    trust = calculate_trust(deepfake=deepfake_score)
                    st.subheader(f"Trust Score: {trust}%")
                    st.progress(trust / 100)
                    st.info(f"Deepfake Probability: {deepfake_score}%")

    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()
