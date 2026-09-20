import urllib.parse
import streamlit as st
from google import genai
import json
import os

# 1. Page Configuration
st.set_page_config(
    page_title="TaskPilot AI — 3D Viral Content Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Ultra 3D Animated CSS (Glowing Neon Borders, Floating Anime, 3D Logos)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Outfit:wght@600;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* 3D Glowing Title */
    .title-3d {
        font-family: 'Outfit', sans-serif;
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 35%, #fbc2eb 70%, #ff4b8b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        text-shadow: 0 10px 30px rgba(0, 242, 254, 0.3);
        margin-bottom: 5px;
    }

    /* 3D Glassmorphic Cards with Glowing Borders */
    .card-3d-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1.5px solid rgba(255, 255, 255, 0.1);
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 22px;
        position: relative;
    }
    .card-3d-box:hover {
        transform: translateY(-6px) scale(1.01);
        border-color: #00f2fe;
        box-shadow: 0 18px 45px rgba(0, 242, 254, 0.35), inset 0 1px 2px rgba(255, 255, 255, 0.3);
    }

    /* Active Glowing Neon 3D Border for Selected Cards */
    .neon-active-box {
        border: 2px solid #00f2fe !important;
        box-shadow: 0 0 35px rgba(0, 242, 254, 0.6), inset 0 1px 2px rgba(0, 242, 254, 0.4) !important;
        transform: translateY(-8px) scale(1.03) !important;
        background: linear-gradient(180deg, rgba(0, 242, 254, 0.12) 0%, rgba(14, 17, 23, 0.9) 100%) !important;
    }

    /* 3D Floating Logos */
    .logo-3d {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 58px;
        height: 58px;
        border-radius: 18px;
        font-size: 32px;
        margin-bottom: 12px;
        animation: floatLogo 3s ease-in-out infinite;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    }
    @keyframes floatLogo {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(3deg); }
    }
    .yt-3d { background: linear-gradient(135deg, #ff0000, #b30000); box-shadow: 0 8px 25px rgba(255, 0, 0, 0.5); }
    .ig-3d { background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045); box-shadow: 0 8px 25px rgba(253, 29, 29, 0.5); }
    .fb-3d { background: linear-gradient(135deg, #1877f2, #0d5bbd); box-shadow: 0 8px 25px rgba(24, 119, 242, 0.5); }
    .clock-3d { background: linear-gradient(135deg, #00f2fe, #4facfe); box-shadow: 0 8px 25px rgba(0, 242, 254, 0.5); }
    .vip-3d { background: linear-gradient(135deg, #f093fb, #f5576c); box-shadow: 0 8px 25px rgba(245, 87, 108, 0.5); }

    /* Anime Human-AI Guide Container */
    .anime-guide-container {
        display: flex;
        align-items: center;
        gap: 22px;
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.1), rgba(255, 75, 139, 0.08));
        border: 1.5px solid rgba(0, 242, 254, 0.4);
        border-radius: 26px;
        padding: 20px 26px;
        margin-bottom: 28px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);
    }
    
    /* Anime Full-Body Character Animations */
    .anime-character {
        flex-shrink: 0;
        animation: floatAnime 3.5s ease-in-out infinite;
    }
    @keyframes floatAnime {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-7px); }
    }
    .waving-hand {
        transform-origin: 82px 72px;
        animation: waveGesture 2.2s infinite ease-in-out;
    }
    @keyframes waveGesture {
        0%, 100% { transform: rotate(0deg); }
        35% { transform: rotate(-18deg); }
        70% { transform: rotate(14deg); }
    }

    .anime-speech {
        color: #E2E8F0;
    }
    .anime-tag {
        display: inline-block;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        color: #000;
        font-weight: 800;
        font-size: 11px;
        padding: 3px 12px;
        border-radius: 20px;
        margin-bottom: 6px;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.6);
    }

    /* Input Box Focus Glowing Neon 3D Border */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within {
        border-color: #00f2fe !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.4) !important;
    }

    /* 3D Action Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00f2fe, #4facfe) !important;
        color: #000 !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 10px 30px rgba(0, 242, 254, 0.7) !important;
    }

    @media (max-width: 768px) {
        .anime-guide-container {
            flex-direction: column;
            text-align: center;
            padding: 16px;
        }
        .title-3d { font-size: 2.2rem; }
    }
</style>
""", unsafe_allow_html=True)

# 3. Database
DB_FILE = "user_database.json"
def load_db():
    if not os.path.exists(DB_FILE):
        d = {"users": {}, "vip_codes": ["VIP2026", "PROCREATOR", "TASKPILOT99", "KARTHI7448"], "payment_logs": []}
        with open(DB_FILE, "w") as f: json.dump(d, f)
        return d
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except Exception:
        return {"users": {}, "vip_codes": ["VIP2026", "PROCREATOR"], "payment_logs": []}

def save_db(data):
    try:
        with open(DB_FILE, "w") as f: json.dump(data, f, indent=2)
    except Exception: pass

db = load_db()
api_key = st.secrets.get("GEMINI_API_KEY", None)
DEFAULT_UPI_ID = st.secrets.get("UPI_ID", "yourname@upi")  # Ungaloda UPI ID inga podalam

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# 4. Clean Sidebar
with st.sidebar:
    st.markdown("## ✨ TaskPilot AI")
    st.caption("Next-Gen 3D Viral Content Studio")
    st.markdown("---")
    
    if not st.session_state.user_email:
        st.markdown("### 🎁 3 Free Trial Credits")
        u_email = st.text_input("Enter your Email to start:", placeholder="creator@gmail.com")
        if st.button("Claim 3 Credits 🚀", use_container_width=True):
            if "@" in u_email and "." in u_email:
                st.session_state.user_email = u_email.strip().lower()
                if st.session_state.user_email not in db["users"]:
                    db["users"][st.session_state.user_email] = {"credits": 3, "is_vip": False}
                    save_db(db)
                st.rerun()
            else:
                st.error("Enter a valid email address.")
    else:
        u_data = db["users"].get(st.session_state.user_email, {"credits": 0, "is_vip": False})
        st.success(f"👤 {st.session_state.user_email}")
        if u_data.get("is_vip", False):
            st.markdown("### 👑 **PREMIUM VIP PASS**")
            st.caption("⚡ Unlimited Generations & Viral Audits Active!")
        else:
            credits_left = u_data.get("credits", 0)
            st.markdown(f"**Credits Remaining:** `{credits_left} / 3 Free`")
            st.progress(max(0.0, min(1.0, credits_left / 3.0)))
            st.markdown("---")
            code_in = st.text_input("Have a VIP Passcode?", type="password", placeholder="e.g. VIP2026")
            if st.button("Unlock Unlimited 🔓", use_container_width=True):
                if code_in.strip() in db.get("vip_codes", []):
                    db["users"][st.session_state.user_email]["is_vip"] = True
                    save_db(db)
                    st.success("VIP Activated! Unlimited Access Granted.")
                    st.rerun()
                else:
                    st.error("Invalid VIP Code. Get yours in Subscriptions tab.")
        
        st.markdown("---")
        if st.button("Sign Out", use_container_width=True):
            st.session_state.user_email = ""
            st.rerun()

# 5. Gemini AI Generation Engine
def generate_viral(prompt_text):
    if not st.session_state.user_email:
        st.warning("👉 Please enter your email in the sidebar first to use your 3 free credits!")
        return None
    u_info = db["users"].get(st.session_state.user_email, {"credits": 0, "is_vip": False})
    if not u_info.get("is_vip", False) and u_info.get("credits", 0) <= 0:
        st.error("❌ Free credits finished! Upgrade in the '💎 Subscriptions & UPI Pay' tab to continue.")
        return None
    if not api_key:
        st.error("Gemini API Key missing in Streamlit Secrets.")
        return None
    try:
        client = genai.Client(api_key=api_key)
        with st.spinner("✨ Gemini Multimodal is generating your viral content..."):
            res = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt_text
            )
            if not u_info.get("is_vip", False):
                db["users"][st.session_state.user_email]["credits"] -= 1
                save_db(db)
            return res.text
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# 6. Hero Section
st.markdown("""
<div style="text-align: center; padding: 10px 0 15px 0;">
    <h1 class="title-3d">TaskPilot AI Studio</h1>
    <p style="color: #A0AEC0; font-size: 1.15rem; max-width: 650px; margin: 0 auto 10px auto;">
        3D Next-Gen AI Content Studio for <b>YouTube, Instagram & Facebook</b>. Every box glows with 3D energy!
    </p>
</div>
""", unsafe_allow_html=True)

# 7. Full-Body Animated Anime Guide ("Kira AI Sensei") with Waving Hand
st.markdown("""
<div class="anime-guide-container">
    <div class="anime-character">
        <svg width="110" height="140" viewBox="0 0 120 150" fill="none" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="60" cy="75" rx="50" ry="60" fill="url(#aura_glow)" opacity="0.35" />
            <defs>
                <radialGradient id="aura_glow" cx="0.5" cy="0.5" r="0.5">
                    <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.9"/>
                    <stop offset="100%" stop-color="#4facfe" stop-opacity="0"/>
                </radialGradient>
                <linearGradient id="suit_grad" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#141824"/>
                    <stop offset="100%" stop-color="#23293d"/>
                </linearGradient>
            </defs>
            <ellipse cx="60" cy="142" rx="26" ry="5" fill="#000" opacity="0.4"/>
            <rect x="46" y="112" width="10" height="28" rx="5" fill="#131722"/>
            <rect x="64" y="112" width="10" height="28" rx="5" fill="#131722"/>
            <path d="M44 135H57V142H44C42 142 42 135 44 135Z" fill="#00f2fe"/>
            <path d="M64 135H77V142H64C62 142 62 135 64 135Z" fill="#00f2fe"/>
            <path d="M40 76C38 88 42 114 60 114C78 114 82 88 80 76C75 66 65 65 60 65C55 65 45 66 40 76Z" fill="url(#suit_grad)" stroke="#00f2fe" stroke-width="1.5"/>
            <polygon points="60,74 65,82 60,90 55,82" fill="#00f2fe"/>
            <path d="M38 74C30 84 28 98 34 104" stroke="#ffdfba" stroke-width="6" stroke-linecap="round"/>
            <path d="M38 72C32 80 30 88 32 94" stroke="#131722" stroke-width="8" stroke-linecap="round"/>
            <g class="waving-hand">
                <path d="M82 72C92 68 100 56 102 46" stroke="#131722" stroke-width="8" stroke-linecap="round"/>
                <path d="M102 46C104 40 102 36 98 34" stroke="#ffdfba" stroke-width="6" stroke-linecap="round"/>
                <circle cx="98" cy="34" r="4" fill="#ffdfba"/>
                <circle cx="102" cy="31" r="2" fill="#ffdfba"/>
                <circle cx="95" cy="30" r="2" fill="#ffdfba"/>
                <polygon points="108,30 110,34 114,35 110,36 108,40 106,36 102,35 106,34" fill="#ffd700"/>
            </g>
            <rect x="56" y="58" width="8" height="10" fill="#ffdfba"/>
            <ellipse cx="60" cy="46" rx="18" ry="17" fill="#ffdfba"/>
            <path d="M38 42C36 24 45 14 60 14C75 14 84 24 82 42C80 58 76 68 76 74C72 70 68 62 68 58C60 62 52 62 48 58C46 64 42 70 38 74C38 68 36 58 38 42Z" fill="#ff4b8b"/>
            <ellipse cx="52" cy="45" rx="4" ry="5.5" fill="#111"/>
            <ellipse cx="68" cy="45" rx="4" ry="5.5" fill="#111"/>
            <ellipse cx="52" cy="46" rx="3" ry="4" fill="#00f2fe"/>
            <ellipse cx="68" cy="46" rx="3" ry="4" fill="#00f2fe"/>
            <circle cx="51" cy="44" r="1.5" fill="#fff"/>
            <circle cx="67" cy="44" r="1.5" fill="#fff"/>
            <ellipse cx="47" cy="51" rx="3" ry="1.5" fill="#ff7675" opacity="0.7"/>
            <ellipse cx="73" cy="51" rx="3" ry="1.5" fill="#ff7675" opacity="0.7"/>
            <path d="M57 53C58 55 62 55 63 53" stroke="#d63031" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M38 32L46 16L52 26" fill="#00f2fe" stroke="#fff" stroke-width="1.5"/>
            <path d="M82 32L74 16L68 26" fill="#00f2fe" stroke="#fff" stroke-width="1.5"/>
            <path d="M42 32C42 22 78 22 78 32" stroke="#4facfe" stroke-width="3" fill="none"/>
        </svg>
    </div>
    <div class="anime-speech">
        <span class="anime-tag">✨ KIRA AI SENSEI (HUMAN AI GUIDE)</span>
        <h3 style="margin: 3px 0 6px 0; color: #FFF; font-weight: 800;">Kon'nichiwa! I am Kira, your 3D Anime AI Guide 🚀</h3>
        <p style="margin: 0; color: #CBD5E0; font-size: 0.95rem; line-height: 1.5;">
            Welcome to the 3D studio! Every box lights up with glowing 3D neon energy. 
            <b>1.</b> Pick your platform tab. <b>2.</b> Enter your topic. <b>3.</b> Hit Generate! I will craft hooks that hold viewers for the first 3 crucial seconds! 🌟
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# 8. Main 3D Studio Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📺 YouTube 3D",
    "📸 Instagram Reels 3D",
    "📘 Facebook Viral 3D",
    "⏰ Best Upload Times",
    "🔥 Viral Page Blueprint (VIP)",
    "💎 Subscriptions & 3D UPI Pay"
])

ALL_LANGS = [
    "English", "Tamil", "Tanglish (Tamil + English)", "Hindi", "Telugu", 
    "Malayalam", "Kannada", "Spanish", "French", "German", "Arabic", "Japanese", "Russian"
]

# Tab 1: YouTube 3D
with tab1:
    st.markdown('''
    <div class="card-3d-box">
        <div class="logo-3d yt-3d">▶️</div>
        <h3 style="display:inline-block; margin-left: 12px; vertical-align: middle;">YouTube 3D Viral Engine</h3>
        <p style="color: #A0AEC0; font-size: 0.9rem;">Engineered for 80%+ View Duration and Maximum CTR.</p>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns()
    with col1:
        yt_t = st.text_input("YouTube Topic or Title:", placeholder="e.g. 5 AI Tools to Automate Online Business", key="y_t")
    with col2:
        yt_f = st.selectbox("Format:", ["YouTube Shorts (< 60s)", "Long Video Outline (8-10m)", "High-CTR Titles & Thumbnails"], key="y_f")
    with col3:
        yt_l = st.selectbox("Language:", ALL_LANGS, key="y_l")
        
    if st.button("Generate YouTube Package 🚀", key="y_btn", use_container_width=True):
        if yt_t.strip():
            p = f"Act as elite YouTube strategist. Topic: {yt_t}, Format: {yt_f}, Language: {yt_l}. Provide 3 Clickable Titles, 3 First-3-Seconds Visual Hooks, Full Script with [Visual Cues], ending CTA, and 10 SEO Tags."
            res = generate_viral(p)
            if res:
                st.markdown("---")
                st.markdown(res)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Instagram 3D
with tab2:
    st.markdown('''
    <div class="card-3d-box">
        <div class="logo-3d ig-3d">📸</div>
        <h3 style="display:inline-block; margin-left: 12px; vertical-align: middle;">Instagram Reels 3D Studio</h3>
        <p style="color: #A0AEC0; font-size: 0.9rem;">Triggers Explore Feed recommendation and high save/share ratio.</p>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns()
    with col1:
        ig_t = st.text_input("Reel Topic / Hook:", placeholder="e.g. 3 Mobile Video Editing Hacks in CapCut", key="i_t")
    with col2:
        ig_f = st.selectbox("Format:", ["Viral Reel (15-30s)", "Carousel Post Script", "Story Series"], key="i_f")
    with col3:
        ig_l = st.selectbox("Language:", ALL_LANGS, key="i_l")
        
    if st.button("Generate Instagram Script ⚡", key="i_btn", use_container_width=True):
        if ig_t.strip():
            p = f"Act as Instagram algorithm specialist. Topic: {ig_t}, Format: {ig_f}, Language: {ig_l}. Provide 3 Visual Hooks, 15-30s Spoken Script, High-Converting Caption with 'Comment [KEYWORD]', and 15 Viral Hashtags."
            res = generate_viral(p)
            if res:
                st.markdown("---")
                st.markdown(res)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Facebook 3D
with tab3:
    st.markdown('''
    <div class="card-3d-box">
        <div class="logo-3d fb-3d">📘</div>
        <h3 style="display:inline-block; margin-left: 12px; vertical-align: middle;">Facebook Viral 3D Engine</h3>
        <p style="color: #A0AEC0; font-size: 0.9rem;">Emotional storytelling and viral community engagement.</p>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns()
    with col1:
        fb_t = st.text_input("Facebook Story / Topic:", placeholder="e.g. An inspiring story of building a drone delivery startup", key="f_t")
    with col2:
        fb_l = st.selectbox("Language:", ALL_LANGS, key="f_l")
        
    if st.button("Generate Facebook Content 🚀", key="f_btn", use_container_width=True):
        if fb_t.strip():
            p = f"Write an emotionally engaging Facebook video script and viral post about: {fb_t} in {fb_l}. Include 1 engaging question to generate 100+ comments."
            res = generate_viral(p)
            if res:
                st.markdown("---")
                st.markdown(res)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Best Upload Times
with tab4:
    st.markdown('''
    <div class="card-3d-box">
        <div class="logo-3d clock-3d">⏰</div>
        <h3 style="display:inline-block; margin-left: 12px; vertical-align: middle;">Peak Uploading Times (3D Traffic Map)</h3>
        <p style="color: #A0AEC0; font-size: 0.9rem;">Maximum initial algorithmic velocity for India (IST) & Worldwide.</p>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        #### 📺 YouTube Windows
        * **India (IST):** 12:00 PM – 2:00 PM & 6:00 PM – 9:00 PM
        * **Best Days:** Thursday, Friday, Saturday
        * *Tip: Upload as Unlisted 1 hr early for full 4K processing.*
        """)
    with col2:
        st.markdown("""
        #### 📸 Instagram Reels Windows
        * **India (IST):** 8:30 AM – 9:30 AM & 7:30 PM – 10:00 PM
        * **Best Days:** Wednesday, Thursday, Sunday
        * *Tip: Pair with trending audio within the first 48 hours.*
        """)
    with col3:
        st.markdown("""
        #### 📘 Facebook Windows
        * **India (IST):** 1:00 PM – 3:30 PM & 7:00 PM – 9:30 PM
        * **Best Days:** Tuesday, Thursday, Friday
        * *Tip: 1-3 minute vertical video clips get 3x more shares.*
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Viral Page Blueprint (VIP)
with tab5:
    st.markdown('''
    <div class="card-3d-box">
        <div class="logo-3d vip-3d">👑</div>
        <h3 style="display:inline-block; margin-left: 12px; vertical-align: middle;">360° Viral Page Growth Blueprint (VIP)</h3>
        <p style="color: #A0AEC0; font-size: 0.9rem;">Step-by-step personalized channel optimization to convert views into followers & income.</p>
    ''', unsafe_allow_html=True)
    
    u_info = db["users"].get(st.session_state.user_email, {"is_vip": False})
    if not u_info.get("is_vip", False):
        st.warning("🔒 This advanced growth suite is reserved for Basic, Standard & Premium Subscribers.")
        st.markdown("""
        * ✅ Complete Channel/Profile Bio Overhaul (10x Follower Conversion)
        * ✅ 30-Day Step-by-Step Content Calendar (Exact topics to post Mon–Sun)
        * ✅ Algorithmic Retention Hacks to hit Explore feeds
        * 👉 **Upgrade in the Subscriptions tab to unlock instantly!**
        """)
    else:
        st.success("🔓 VIP Active! Enter your channel details:")
        v_niche = st.text_input("Your Channel Niche:", placeholder="e.g. Video Editing, Drones, Tech Reviews, Fitness")
        col1, col2 = st.columns(2)
        with col1:
            v_plat = st.selectbox("Platform:", ["YouTube Channel", "Instagram Page", "Cross-Platform (YouTube + Instagram)"])
        with col2:
            v_goal = st.selectbox("Goal:", ["First 10,000 Organic Followers", "Monetization & AdSense", "Sell Courses / Products"])
            
        if st.button("Generate My 30-Day Viral Blueprint 🚀", use_container_width=True):
            p = f"Act as viral growth consultant. Niche: {v_niche}, Platform: {v_plat}, Goal: {v_goal}. Produce high-converting bio, 30-day weekly content calendar, retention triggers, and monetization funnel."
            out = generate_viral(p)
            if out:
                st.markdown("---")
                st.markdown(res)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 6: Subscriptions & Dynamic 3D Neon Selection
with tab6:
    st.markdown('<div class="card-3d-box"><h2 style="text-align:center;">💎 Choose Your Growth Plan</h2>', unsafe_allow_html=True)
    st.caption("Click any plan below—the selected box lights up with glowing 3D neon borders!")
    
    # Selection control
    selected_plan = st.radio(
        "Select Your Plan (Watch the 3D card light up):",
        ["Basic Plan (₹49)", "Standard Plan (₹149) 🔥", "Premium VIP (₹299) 👑"],
        horizontal=True
    )
    
    is_basic = "49" in selected_plan
    is_standard = "149" in selected_plan
    is_vip_plan = "299" in selected_plan
    
    amount = "49" if is_basic else ("149" if is_standard else "299")
    tier_name = "Basic" if is_basic else ("Standard" if is_standard else "Premium")
    
    # Class highlights: selected box gets glowing neon line
    b_class = "neon-active-box" if is_basic else ""
    s_class = "neon-active-box" if is_standard else ""
    v_class = "neon-active-box" if is_vip_plan else ""
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
        <div class="card-3d-box {b_class}" style="text-align:center;">
            <h3>🥉 Basic Plan</h3>
            <h1 style="color:#00f2fe;">₹49</h1>
            <p style="color:#AAA; font-size:14px;">50 AI Script Generations<br>YouTube Shorts & Reels<br>High-CTR Titles & Hooks</p>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="card-3d-box {s_class}" style="text-align:center;">
            <span style="background:#00f2fe; color:#000; font-size:11px; font-weight:800; padding:2px 10px; border-radius:12px;">MOST POPULAR 🔥</span>
            <h3 style="margin-top:6px;">🥈 Standard Plan</h3>
            <h1 style="color:#00f2fe;">₹149</h1>
            <p style="color:#AAA; font-size:14px;">300 AI Script Generations<br>All Platforms (YT, IG, FB)<br>Full Viral Page Blueprint</p>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="card-3d-box {v_class}" style="text-align:center;">
            <span style="background:linear-gradient(90deg, #ff4b8b, #f093fb); color:#fff; font-size:11px; font-weight:800; padding:2px 10px; border-radius:12px;">LIFETIME PASS 👑</span>
            <h3 style="margin-top:6px;">🥇 Premium VIP</h3>
            <h1 style="color:#ff4b8b;">₹299</h1>
            <p style="color:#AAA; font-size:14px;">UNLIMITED Generations Forever<br>All Future Features<br>1-on-1 VIP Creator Support</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")
    
    upi_string = f"upi://pay?pa={DEFAULT_UPI_ID}&pn=TaskPilotAI&am={amount}&cu=INR&tn=TaskPilot{tier_name}"
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(upi_string)}"
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f"#### 📱 Scan to Pay **₹{amount}** via GPay / PhonePe")
        st.image(qr_code_url, width=220, caption=f"Scan with Google Pay / PhonePe / Paytm / BHIM")
        st.markdown(f"**UPI ID:** `{DEFAULT_UPI_ID}`")
        st.markdown(f'<a href="{upi_string}" target="_blank" style="display:inline-block; background:linear-gradient(90deg, #00f2fe, #4facfe); color:#000; padding:10px 22px; border-radius:12px; text-decoration:none; font-weight:800; box-shadow:0 6px 20px rgba(0,242,254,0.4);">📲 Click to Pay via UPI App (Mobile)</a>', unsafe_allow_html=True)
        
    with col_p2:
        st.markdown("#### ⚡ Instant Activation")
        u_email_input = st.text_input("Your Registered Email:", value=st.session_state.user_email, placeholder="yourname@gmail.com")
        utr_num = st.text_input("12-Digit UPI Transaction ID / UTR:", placeholder="e.g. 425678912345")
        if st.button("Submit Payment & Get Code 🚀", use_container_width=True):
            if len(utr_num.strip()) >= 6 and "@" in u_email_input:
                db["payment_logs"].append({"email": u_email_input.strip().lower(), "utr": utr_num.strip(), "amount": amount})
                save_db(db)
                st.success("🎉 Payment Received! Your Activation Passcode is: **`VIP2026`**")
                st.info("Enter this passcode in the left sidebar to unlock unlimited access!")
            else:
                st.error("Please enter a valid email and 12-digit UTR from your payment receipt.")
    st.markdown('</div>', unsafe_allow_html=True)
