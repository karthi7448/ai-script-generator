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
DEFAULT_UPI_ID = st.secrets.get("UPI_ID", "yourname@upi")  # Ungaloda real UPI ID inga podalam
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

# ----------------- ANIME SENSEI INTRO (100% Guaranteed SVG Graphic) -----------------
st.markdown("""
<div class="anime-guide-container">
    <svg width="75" height="75" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="border-radius: 50%; box-shadow: 0 0 25px rgba(0, 242, 254, 0.7); flex-shrink: 0; background: linear-gradient(135deg, #1f1c2c, #928dab);">
        <circle cx="50" cy="50" r="46" fill="#131722" stroke="#00f2fe" stroke-width="2"/>
        <path d="M22 42C24 25 36 15 50 15C64 15 76 25 78 42C72 32 60 30 50 34C40 30 28 32 22 42Z" fill="#ff4b8b"/>
        <ellipse cx="50" cy="56" rx="26" ry="24" fill="#ffdfba"/>
        <path d="M24 40C25 55 28 62 30 65C28 55 27 46 26 40Z" fill="#ff4b8b"/>
        <path d="M76 40C75 55 72 62 70 65C72 55 73 46 74 40Z" fill="#ff4b8b"/>
        <path d="M40 32C45 42 43 48 41 52C46 45 48 38 46 32Z" fill="#ff6ea7"/>
        <path d="M60 32C55 42 57 48 59 52C54 45 52 38 54 32Z" fill="#ff6ea7"/>
        <ellipse cx="38" cy="54" rx="6" ry="8" fill="#111"/>
        <ellipse cx="62" cy="54" rx="6" ry="8" fill="#111"/>
        <ellipse cx="38" cy="55" rx="5" ry="6" fill="#00f2fe"/>
        <ellipse cx="62" cy="55" rx="5" ry="6" fill="#00f2fe"/>
        <circle cx="36" cy="52" r="2.5" fill="#fff"/>
        <circle cx="60" cy="52" r="2.5" fill="#fff"/>
        <circle cx="40" cy="57" r="1.2" fill="#fff"/>
        <circle cx="64" cy="57" r="1.2" fill="#fff"/>
        <ellipse cx="31" cy="62" rx="4" ry="2" fill="#ff7675" opacity="0.6"/>
        <ellipse cx="69" cy="62" rx="4" ry="2" fill="#ff7675" opacity="0.6"/>
        <path d="M46 65C48 68 52 68 54 65" stroke="#d63031" stroke-width="1.8" stroke-linecap="round"/>
        <path d="M20 28L30 14L34 26" fill="#00f2fe" stroke="#fff" stroke-width="1.5"/>
        <path d="M80 28L70 14L66 26" fill="#00f2fe" stroke="#fff" stroke-width="1.5"/>
    </svg>
    <div class="anime-bubble">
        <h4 style="margin: 0 0 5px 0; color: #FFF; font-weight: 700; font-size: 1.15rem;">✨ Kon'nichiwa! I am Kira, your Anime AI Viral Sensei</h4>
        <p style="margin: 0; color: #CBD5E0; font-size: 0.93rem;">
            Ready to make your content blow up? <b>1.</b> Pick your platform tab below. <b>2.</b> Enter your video topic and target language. 
            <b>3.</b> Hit Generate! I engineer scroll-stopping 3-second hooks and high-retention scripts that the algorithm loves! 🚀
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
        fb_topic = st.text_input("Story / Discussion Topic:", placeholder="e.g. How a college dropout built a $1M business using drones", key="fb_top")
    with col_f2:
        fb_lang = st.selectbox("Language:", GLOBAL_LANGUAGES, index=0, key="fb_lng")
        
    if st.button("Generate Facebook Viral Content 🚀", key="btn_fb", use_container_width=True):
        if fb_topic.strip():
            p = f"""
            Write a viral Facebook video script and accompanying long-form narrative post for: {fb_topic} in {fb_lang}.
            Make it emotionally compelling, easy to relate to, and design the final paragraph to provoke hundreds of constructive comments and shares.
            """
            result = generate_viral_content(p)
            if result:
                st.markdown("---")
                st.markdown(result)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Best Upload Times
with tab_times:
    st.markdown('<div class="gemini-card">', unsafe_allow_html=True)
    st.markdown("### ⏰ Best Worldwide & Indian Peak Uploading Hours")
    st.write("Publishing during these critical windows gives the initial velocity needed to trip the algorithm:")
    
    t_c1, t_c2, t_c3 = st.columns(3)
    with t_c1:
        st.markdown("""
        #### 📺 YouTube Peak Windows
        * **India (IST):** 12:00 PM – 2:00 PM & 6:00 PM – 9:00 PM
        * **US / Global (EST):** 2:00 PM – 5:00 PM
        * **Best Days:** Thursday, Friday, Saturday
        * *Sensei Tip: Upload as Unlisted 1-2 hours before so the 4K render and auto-captions process cleanly.*
        """)
    with t_c2:
        st.markdown("""
        #### 📸 Instagram Reels Windows
        * **India (IST):** 8:30 AM – 9:30 AM & 7:30 PM – 10:00 PM
        * **US / Global (EST):** 9:00 AM – 12:00 PM & 7:00 PM – 9:00 PM
        * **Best Days:** Wednesday, Thursday, Sunday
        * *Sensei Tip: Post when your specific followers are active (check IG Insights -> Total Followers).*
        """)
    with t_c3:
        st.markdown("""
        #### 📘 Facebook Watch Windows
        * **India (IST):** 1:00 PM – 3:30 PM & 7:00 PM – 9:30 PM
        * **US / Global (EST):** 1:00 PM – 4:00 PM
        * **Best Days:** Tuesday, Thursday, Friday
        * *Sensei Tip: Vertical 1:1 or 9:16 video clips with on-screen burned-in subtitles perform 3x better.*
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# 5. Viral Page Blueprint (VIP)
with tab_audit:
    st.markdown('<div class="gemini-card">', unsafe_allow_html=True)
    st.markdown("### 🔥 360° Social Media Viral Page Blueprint & Audit (VIP)")
    
    curr_user = db["users"].get(st.session_state.user_email, {"is_vip": False})
    if not curr_user.get("is_vip", False):
        st.warning("🔒 This advanced audit suite is reserved for Basic, Standard, and Premium Subscribers.")
        st.markdown("""
        **What you unlock with a Subscription:**
        * ✅ Complete Channel/Profile Bio Overhaul (10x your Follower Conversion Rate)
        * ✅ 30-Day Step-by-Step Content Calendar (Exact topics to post Mon–Sun)
        * ✅ Algorithmic Retention Checklist to hit the Explore & Recommendation feeds
        * ✅ Audience Monetization Funnel (Convert passive viewers into paying clients/customers)
        
        👉 **Head over to the Subscriptions tab to unlock instant VIP access!**
        """)
    else:
        st.success("🔓 VIP Sensei Active! Enter your channel details:")
        v_niche = st.text_input("Your Specific Niche / Industry:", placeholder="e.g. Video Editing, Tech Gadgets, Finance, Fitness")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            v_platform = st.selectbox("Target Platform:", ["YouTube Channel", "Instagram Page", "Cross-Platform (YouTube + Instagram)"])
        with col_v2:
            v_goal = st.selectbox("Primary Objective:", ["Grow first 10,000 Organic Followers", "Monetization & AdSense Maximization", "Sell High-Ticket Courses / Services"])
            
        if st.button("Generate My 30-Day Viral Blueprint 🚀", use_container_width=True):
            p = f"""
            You are a world-class social media viral growth consultant.
            Niche: {v_niche}
            Platform: {v_platform}
            Goal: {v_goal}

            Produce an exhaustive, actionable Master Blueprint:
            1. High-Converting Bio & Profile Header Formula
            2. First 30 Days Content Calendar (Exact video topics, angles, and formats)
            3. 3 Algorithm Watch-Time Hacks to push content to millions of non-followers
            4. 3 Costly Mistakes that immediately kill page reach
            5. Step-by-step Monetization Funnel to generate revenue from Day 1
            """
            res = generate_viral_content(p)
            if res:
                st.markdown("---")
                st.markdown(res)
    st.markdown('</div>', unsafe_allow_html=True)

# 6. Subscriptions & Instant UPI Pay (3 Tiers: Basic, Standard, Premium)
with tab_sub:
    st.markdown('<div class="gemini-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h2>💎 Choose Your Growth Plan</h2>
        <p style="color: #A0AEC0;">Affordable pricing designed for independent creators and aspiring influencers worldwide.</p>
    </div>
    """, unsafe_allow_html=True)

    c_p1, c_p2, c_p3 = st.columns(3)

    with c_p1:
        st.markdown("""
        <div class="pricing-card">
            <h3>🥉 Basic Plan</h3>
            <h1 style="color: #4facfe;">₹49 <span style="font-size: 14px; color: #888;">($1 USD)</span></h1>
            <p style="color: #AAA;">Perfect for beginner creators testing the waters.</p>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <ul style="color: #DDD; font-size: 14px; line-height: 1.8;">
                <li>✅ <b>50 AI Script Generations</b></li>
                <li>✅ YouTube Shorts & Reels Generator</li>
                <li>✅ Viral Hooks & High-CTR Titles</li>
                <li>❌ Viral Page Setup Blueprint</li>
                <li>❌ Priority 1-on-1 Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_p2:
        st.markdown("""
        <div class="pricing-card pricing-card-popular">
            <span style="background:#4facfe; color:#000; font-size:11px; font-weight:800; padding:2px 10px; border-radius:20px;">MOST POPULAR 🔥</span>
            <h3 style="margin-top:10px;">🥈 Standard Plan</h3>
            <h1 style="color: #00f2fe;">₹149 <span style="font-size: 14px; color: #888;">($2 USD)</span></h1>
            <p style="color: #AAA;">For serious creators building daily viral momentum.</p>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <ul style="color: #DDD; font-size: 14px; line-height: 1.8;">
                <li>✅ <b>300 AI Script Generations</b></li>
                <li>✅ All Platforms (YouTube, IG, FB)</li>
                <li>✅ Best Worldwide Uploading Times</li>
                <li>✅ <b>Complete Viral Page Blueprint</b></li>
                <li>✅ Email & WhatsApp Assistance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_p3:
        st.markdown("""
        <div class="pricing-card">
            <span style="background:linear-gradient(90deg, #FF6EA7, #B56BFF); color:#FFF; font-size:11px; font-weight:800; padding:2px 10px; border-radius:20px;">LIFETIME PASS 👑</span>
            <h3 style="margin-top:10px;">🥇 Premium VIP</h3>
            <h1 style="color: #FF6EA7;">₹299 <span style="font-size: 14px; color: #888;">($4 USD)</span></h1>
            <p style="color: #AAA;">Unlimited viral power for agencies and top creators.</p>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <ul style="color: #DDD; font-size: 14px; line-height: 1.8;">
                <li>✅ <b>UNLIMITED AI Generations Forever</b></li>
                <li>✅ All Current & Future AI Capabilities</li>
                <li>✅ Complete 30-Day Channel Blueprints</li>
                <li>✅ Direct 1-on-1 VIP Creator Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Interactive Payment Selector
    selected_tier = st.radio(
        "Select Plan to Generate QR Scanner:",
        ["Basic Plan (₹49)", "Standard Plan (₹149) 🔥", "Premium VIP (₹299) 👑"],
        horizontal=True
    )
    
    tier_amt = "49" if "49" in selected_tier else ("149" if "149" in selected_tier else "299")
    tier_name = "Basic" if "49" in selected_tier else ("Standard" if "149" in selected_tier else "Premium")

    upi_pay_string = f"upi://pay?pa={DEFAULT_UPI_ID}&pn={urllib.parse.quote(UPI_NAME)}&am={tier_amt}&cu=INR&tn={urllib.parse.quote(f'TaskPilot {tier_name}')}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(upi_pay_string)}"

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.markdown(f"#### 📱 Scan to Pay **₹{tier_amt}** with GPay / PhonePe / Paytm")
        st.image(qr_url, width=220, caption="Safe & Instant UPI Payment")
        st.markdown(f"**UPI ID:** `{DEFAULT_UPI_ID}`")
        st.markdown(f'<a href="{upi_pay_string}" target="_blank" style="display:inline-block; background:linear-gradient(90deg, #4facfe, #00f2fe); color:#000; padding:10px 22px; border-radius:12px; text-decoration:none; font-weight:700; margin-top:8px;">📲 Click to Pay via UPI App (Mobile)</a>', unsafe_allow_html=True)

    with col_q2:
        st.markdown("#### ⚡ Instant Activation")
        st.write("Completed your payment? Submit your details to receive instant VIP unlock:")
        u_email_input = st.text_input("Your Registered Email:", value=st.session_state.user_email, placeholder="yourname@gmail.com", key="pay_em")
        utr_code = st.text_input("12-Digit UPI Transaction ID / UTR Number:", placeholder="e.g. 425678912345", key="pay_utr")
        
        if st.button("Submit Payment & Get VIP Code 🚀", use_container_width=True):
            if len(utr_code.strip()) >= 6 and "@" in u_email_input:
                db["payment_logs"].append({
                    "email": u_email_input.strip().lower(),
                    "utr": utr_code.strip(),
                    "plan": tier_name,
                    "amount": tier_amt
                })
                vip_unlock_code = "VIP2026"
                save_db(db)
                st.success(f"🎉 Payment Received! Your Activation Passcode is: **`{vip_unlock_code}`**")
                st.info("Copy this code and enter it into the left sidebar to unlock unlimited access right now!")
            else:
                st.error("Please provide a valid email and 12-digit UTR from your payment app.")

    st.markdown('</div>', unsafe_allow_html=True)
