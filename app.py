import streamlit as st
from google import genai

st.set_page_config(page_title="AI Shorts Script Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Viral Shorts & Reels Generator")
st.caption("Generate high-retention hooks and 30-second scripts in seconds.")

# API Key Secrets la irunthu edukkum
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

topic = st.text_input("Enter your video topic:", placeholder="e.g., Top 3 AI tools to save time")
language = st.selectbox("Language / Style:", ["English", "Tamil", "Tanglish (Tamil + English)", "Hindi"])
tone = st.selectbox("Tone:", ["Energetic & Viral", "Educational", "Storytelling", "Motivational"])

if st.button("Generate Script 🚀"):
    if not api_key:
        st.error("Please provide an API key in secrets or sidebar.")
    elif not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an expert short-form video creator.
            Topic: {topic}
            Language: {language}
            Tone: {tone}

            Provide:
            1. 3 Catchy Visual Hooks (First 3 seconds)
            2. Full 30-Second Script with [Visual/Action] cues
            3. Call To Action (CTA)
            4. 5 Relevant Hashtags
            """

            with st.spinner("Generating your script..."):
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                st.subheader("Your Viral Script:")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar UPI Monetization
st.sidebar.title("💰 Support / Unlimited Access")
st.sidebar.markdown("**Price: ₹49 only**")
st.sidebar.info("GPay / PhonePe UPI: `yourname@upi`")
