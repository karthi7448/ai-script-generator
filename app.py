import urllib.parse
import streamlit as st
from google import genai
import json
import os

# ----------------- SEO & Page Configuration -----------------
st.set_page_config(
    page_title="TaskPilot AI — Viral Script & Content Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- SEO Meta Tags & Gemini-Style CSS -----------------
st.markdown("""
<head>
    <meta name="description" content="TaskPilot AI is the #1 worldwide AI viral script and hook generator for YouTube Shorts, Instagram Reels, and TikTok. Powered by Google Gemini.">
    <meta name="keywords" content="AI script generator, viral reels hook, youtube shorts AI, tiktok script maker, taskpilot ai, content creator AI, viral marketing">
    <meta name="author" content="TaskPilot AI">
    <meta property="og:title" content="TaskPilot AI - Gemini Viral Content Studio">
    <meta property="og:description" content="Create viral scripts in 30 seconds across all social media platforms in any language.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Gemini Dynamic Gradient Header */
    .gemini-gradient {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 30%, #a18cd1 70%, #fbc2eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* Gemini-Style Glass Cards */
    .gemini-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    .gemini-card:hover {
        transform: translateY(-4px);
        border-color: rgba(79, 172, 254, 0.5);
        box-shadow: 0 16px 40px 0 rgba(79, 172, 254, 0.2);
    }

    /* Anime Sensei Guide Container */
    .anime-guide-container {
        display: flex;
        align-items: center;
        gap: 20px;
        background: linear-gradient(135deg, rgba(161, 140, 209, 0.1), rgba(251, 194, 235, 0.05));
        border: 1px solid rgba(161, 140, 209, 0.3);
        border-radius: 24px;
        padding: 20px 24px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    .anime-avatar {
        font-size: 55px;
        background: radial-gradient(circle, #7f00ff, #e100ff);
        border-radius: 50%;
        width: 75px;
        height: 75px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(225, 0, 255, 0.6);
        animation: pulseAvatar 3s infinite alternate;
        flex-shrink: 0;
    }
    @keyframes pulseAvatar {
        0% { transform: scale(1); box-shadow: 0 0 20px rgba(225, 0, 255, 0.5); }
        100% { transform: scale(1.05); box-shadow: 0 0 35px rgba(79, 172, 254, 0.8); }
    }
    .anime-bubble {
        color: #E2E8F0;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Tier Pricing Cards */
    .pricing-card {
        border-radius: 24px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.02);
        transition: 0.3s ease;
        height: 100%;
    }
    .pricing-card-popular {
        border: 1px solid #4facfe;
        background: linear-gradient(180deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 0, 0, 0) 100%);
        box-shadow: 0 0 30px rgba(79, 172, 254, 0.25);
    }
    .pricing-card:hover {
        transform: translateY(-5px);
    }

    @media (max-width: 768px) {
        .anime-guide-container {
            flex-direction: column;
            text-align: center;
            padding: 16px;
        }
        .anime-avatar {
            width: 60px;
            height: 60px;
            font-size: 40px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Persistent Storage -----------------
DB_FILE = "user_database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        default_data = {
            "users": {},
            "vip_codes": ["VIP2026", "PROCREATOR", "TASKPILOT99", "KARTHI7448"],
            "payment_logs": []
        }
        with open(DB_FILE, "w") as f:
            json.dump(default_data, f)
        return default_data
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"users": {}, "vip_codes": ["VIP2026", "PROCREATOR", "TASKPILOT99"], "payment_logs": []}

def save_db(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

db = load_db()

# ----------------- Config & Secrets -----------------
api_key = st.secrets.get("GEMINI_API_KEY", None)
DEFAULT_UPI_ID = st.secrets.get("UPI_ID", "yourname@upi")  # Ungaloda UPI ID inga podunga
UPI_NAME = "TaskPilot AI"

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ----------------- Sidebar (Clean User Profile) -----------------
with st.sidebar:
    st.markdown('<h2 style="margin-bottom:0px;">✨ TaskPilot AI</h2>', unsafe_allow_html=True)
    st.caption("Next-Gen Viral Content Engine")
    st.markdown("---")
    
    if not st.session_state.user_email:
        st.markdown("### 🎁 Claim Free Trial")
        st.write("Join 10,000+ creators worldwide.")
        user_input_email = st.text_input("Enter Email to claim 3 Free Credits:", placeholder="creator@gmail.com")
        if st.button("Unlock 3 Credits 🚀", use_container_width=True):
            if "@" in user_input_email and "." in user_input_email:
                clean_email = user_input_email.strip().lower()
                st.session_state.user_email = clean_email
                if clean_email not in db["users"]:
                    db["users"][clean_email] = {"credits": 3, "is_vip": False, "plan": "Free"}
                    save_db(db)
                st.rerun()
            else:
                st.error("Please enter a valid email address.")
    else:
        user_data = db["users"].get(st.session_state.user_email, {"credits": 0, "is_vip": False, "plan": "Free"})
        st.success(f"👤 **{st.session_state.user_email}**")
        
        if user_data.get("is_vip", False):
            st.markdown('<div style="background:linear-gradient(90deg, #FF6EA7, #B56BFF); padding:8px 14px; border-radius:12px; font-weight:700; text-align:center; color:white; margin:10px 0;">👑 PREMIUM VIP MEMBER</div>', unsafe_allow_html=True)
            st.caption("⚡ Unlimited Generations & Custom Page Audits Unlocked!")
        else:
            c_left = user_data.get("credits", 0)
            st.markdown(f"**Credits Balance:** `{c_left} / 3 Free`")
            st.progress(max(0.0, min(1.0, c_left / 3.0)))
            
            st.markdown("---")
            st.markdown("#### 🔑 Have a VIP Passcode?")
            v_code = st.text_input("Enter Passcode:", type="password", placeholder="e.g. VIP2026")
            if st.button("Activate Passcode 🔓", use_container_width=True):
                if v_code.strip() in db.get("vip_codes", []):
                    db["users"][st.session_state.user_email]["is_vip"] = True
                    db["users"][st.session_state.user_email]["plan"] = "Premium VIP"
                    save_db(db)
                    st.success("🎉 Welcome to Premium! Unlimited access granted.")
                    st.rerun()
                else:
                    st.error("Invalid passcode. Get yours in the Subscriptions tab.")
        
        st.markdown("---")
        if st.button("Sign Out", use_container_width=True):
            st.session_state.user_email = ""
            st.rerun()

# ----------------- AI Engine Call Function -----------------
def generate_viral_content(prompt_text):
    if not st.session_state.user_email:
        st.warning("👉 Please enter your email in the sidebar first to use your 3 free credits!")
        return None

    user_info = db["users"].get(st.session_state.user_email, {"credits": 0, "is_vip": False})
    if not user_info.get("is_vip", False) and user_info.get("credits", 0) <= 0:
        st.error("❌ You have reached your free credit limit! Upgrade to Basic, Standard, or Premium to continue.")
        return None

    if not api_key:
        st.error("API Key is missing. Configure GEMINI_API_KEY in Streamlit Secrets.")
        return None

    try:
        client = genai.Client(api_key=api_key)
        with st.spinner("✨ Gemini is engineering your high-retention viral content..."):
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt_text
            )
            # Deduct credit if free
            if not user_info.get("is_vip", False):
                db["users"][st.session_state.user_email]["credits"] -= 1
                save_db(db)
            return response.text
    except Exception as e:
        st.error(f"Generation error: {e}")
        return None

# ----------------- HERO HEADER (Gemini Style) -----------------
st.markdown("""
<div style="text-align: center; padding: 25px 0 10px 0;">
    <h1 style="font-size: 3.2rem; margin-bottom: 8px;">
        <span class="gemini-gradient">TaskPilot AI Studio</span>
    </h1>
    <p style="font-size: 1.15rem; color: #A0AEC0; max-width: 650px; margin: 0 auto 20px auto;">
        Supercharge your social presence with AI-crafted viral scripts, scroll-stopping hooks & algorithmic growth blueprints.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------- ANIME SENSEI INTRO & GUIDANCE -----------------
st.markdown("""
<div class="anime-guide-container">
    <div class="anime-avatar">🥷</div>
    <div class="anime-bubble">
        <h4 style="margin: 0 0 5px 0; color: #FFF; font-weight: 700;">Kon'nichiwa Creator! I am Kira, your AI Viral Sensei ✨</h4>
        <p style="margin: 0; color: #CBD5E0; font-size: 0.93rem;">
            Want your next video to hit 100K+ views? <b>Step 1:</b> Enter your topic below. <b>Step 2:</b> Pick your platform & language. 
            <b>Step 3:</b> Hit Generate! I use Google Gemini's multimodal reasoning to craft hooks that stop the scroll in the first 3 seconds! 🚀
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- MAIN STUDIO TABS -----------------
tab_yt, tab_ig, tab_fb, tab_times, tab_audit, tab_sub = st.tabs([
    "📺 YouTube Studio",
    "📸 Instagram Reels",
    "📘 Facebook Viral",
    "⏰ Best Upload Times",
    "🔥 Viral Page Blueprint (VIP)",
    "💎 Subscriptions & UPI Pay"
])

GLOBAL_LANGUAGES = [
    "English", "Tamil", "Tanglish (Tamil + English)", "Hindi", "Telugu", 
    "Malayalam", "Kannada", "Bengali", "Spanish", "French", "German", 
    "Arabic", "Japanese", "Korean", "Portuguese", "Russian", "Indonesian"
]

# 1. YouTube
with tab_yt:
    st.markdown('<div class="gemini-card">', unsafe_allow_html=True)
    st.markdown("### 📺 YouTube Viral Script & Shorts Engine")
    st.caption("Engineered for High Click-Through Rate (CTR) and 80%+ Average View Duration (AVD).")
    
    col_p1, col_p2, col_p3 = st.columns()
    with col_p1:
        yt_topic = st.text_input("Video Topic or Title Idea:", placeholder="e.g. 5 AI Websites That Feel Illegal to Know", key="yt_top")
    with col_p2:
        yt_format = st.selectbox("Content Format:", ["YouTube Shorts (< 60s)", "Long Video Outline & Hook (8-10m)", "Viral Title & Thumbnail Concept"], key="yt_fmt")
    with col_p3:
        yt_lang = st.selectbox("Language:", GLOBAL_LANGUAGES, index=0, key="yt_lng")
        
    yt_tone = st.select_slider("Content Energy / Tone:", options=["Calm & Insightful", "Educational & Authoritative", "High-Energy & Viral", "Shocking & Mysterious"], value="High-Energy & Viral", key="yt_tne")
    
    if st.button("Generate YouTube Package 🚀", key="btn_yt", use_container_width=True):
        if yt_topic.strip():
            p = f"""
            You are an elite YouTube algorithm strategist and scriptwriter.
            Topic: {yt_topic}
            Format: {yt_format}
            Language: {yt_lang}
            Tone: {yt_tone}

            Generate a comprehensive viral production package:
            1. 3 High-CTR Click-Worthy Title Options (Using curiosity gaps)
            2. 3 First-3-Seconds Visual & Verbal Hook Variations (Pattern interrupts)
            3. Complete Script with [Visual Cues], [Sound Effects], and [On-Screen Text]
            4. High-Retention Call To Action (CTA) encouraging comments
            5. 10 High-Ranking SEO Search Tags & Keywords
            """
            result = generate_viral_content(p)
            if result:
                st.markdown("---")
                st.markdown(result)
        else:
            st.warning("Please enter a video topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# 2. Instagram
with tab_ig:
    st.markdown('<div class="gemini-card">', unsafe_allow_html=True)
    st.markdown("### 📸 Instagram Reels & Hook Studio")
    st.caption("Crafted to trigger the Instagram Explore algorithm and generate viral saves/shares.")
    
    col_i1, col_i2, col_i3 = st.columns()
    with col_i1:
        ig_topic = st.text_input("Reel Topic / Concept:", placeholder="e.g. 3 Mobile Video Editing Hacks that look like Hollywood", key="ig_top")
    with col_i2:
        ig_format = st.selectbox("Format:", ["Viral Reel (15-30s)", "Carousel Post Script (7 Slides)", "Story Series Funnel"], key="ig_fmt")
    with col_i3:
        ig_lang = st.selectbox("Language:", GLOBAL_LANGUAGES, index=0, key="ig_lng")
        
    ig_style = st.selectbox("Aesthetic & Vibe:", ["Fast-Paced & Relatable", "Cinematic & Minimalist", "Controversial Myth-Buster", "Step-by-Step Educational"], key="ig_sty")
    
    if st.button("Generate Instagram Script ⚡", key="btn_ig", use_container_width=True):
        if ig_topic.strip():
            p = f"""
            You are a viral Instagram creator and growth strategist.
            Topic: {ig_topic}
            Format: {ig_format}
            Language: {ig_lang}
            Vibe: {ig_style}

            Generate:
            1. 3 Visual Hook Cues (Gestures, on-screen text, audio cue)
            2. Voiceover / Dialogue Script (Timed precisely for 15-30 seconds)
            3. High-Converting Caption with a clear 'Comment [KEYWORD] for DM link' trigger
            4. 15 Categorized Viral Hashtags (5 Low-competition, 5 Niche, 5 Trending)
            """
            result = generate_viral_content(p)
            if result:
                st.markdown("---")
                st.markdown(result)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. Facebook
with tab_fb:
    st.markdown('<div class="gemini-card">', unsafe_allow_html=True)
    st.markdown("### 📘 Facebook Viral Video & Discussion Engine")
    st.caption("Tailored for mass social sharing, emotional resonance, and high comment velocity.")
    
    col_f1, col_f2 = st.columns()
    with col_f1:
        fb_topic =
