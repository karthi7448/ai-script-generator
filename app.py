import urllib.parse
import streamlit as st
from google import genai
import json
import os

# 1. Page Config
st.set_page_config(
    page_title="TaskPilot AI — Viral Script Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Modern 3D Gemini CSS & Anime SVG Avatar Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .gemini-title {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 40%, #fbc2eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 5px;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    .anime-box {
        display: flex;
        align-items: center;
        gap: 16px;
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.12), rgba(241, 140, 209, 0.08));
        border: 1px solid rgba(79, 172, 254, 0.35);
        border-radius: 20px;
        padding: 16px 20px;
        margin-bottom: 22px;
    }
    .price-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 20px;
        text-align: center;
    }
    .popular-border {
        border: 2px solid #00f2fe !important;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# 3. Database
DB_FILE = "user_database.json"
def load_db():
    if not os.path.exists(DB_FILE):
        d = {"users": {}, "vip_codes": ["VIP2026", "PROCREATOR", "KARTHI7448"], "payment_logs": []}
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

# 4. Sidebar (User Profile)
with st.sidebar:
    st.markdown("## ✨ TaskPilot AI")
    st.caption("Next-Gen Viral Content Engine")
    st.markdown("---")
    
    if not st.session_state.user_email:
        st.markdown("### 🎁 3 Free Trial Credits")
        u_email = st.text_input("Enter your Email:", placeholder="creator@gmail.com")
        if st.button("Claim 3 Credits 🚀", use_container_width=True):
            if "@" in u_email and "." in u_email:
                st.session_state.user_email = u_email.strip().lower()
                if st.session_state.user_email not in db["users"]:
                    db["users"][st.session_state.user_email] = {"credits": 3, "is_vip": False}
                    save_db(db)
                st.rerun()
            else:
                st.error("Enter a valid email.")
    else:
        u_data = db["users"].get(st.session_state.user_email, {"credits": 0, "is_vip": False})
        st.success(f"👤 {st.session_state.user_email}")
        if u_data.get("is_vip", False):
            st.markdown("### 👑 **PREMIUM VIP MEMBER**")
            st.caption("Unlimited AI Generations Unlocked!")
        else:
            credits_left = u_data.get("credits", 0)
            st.markdown(f"**Credits Balance:** `{credits_left} / 3 Free`")
            st.progress(max(0.0, min(1.0, credits_left / 3.0)))
            st.markdown("---")
            code_in = st.text_input("Have a VIP Code?", type="password", placeholder="e.g. VIP2026")
            if st.button("Unlock Unlimited 🔓", use_container_width=True):
                if code_in.strip() in db.get("vip_codes", []):
                    db["users"][st.session_state.user_email]["is_vip"] = True
                    save_db(db)
                    st.success("VIP Activated! Unlimited Access Granted.")
                    st.rerun()
                else:
                    st.error("Invalid VIP Code.")
        
        st.markdown("---")
        if st.button("Sign Out", use_container_width=True):
            st.session_state.user_email = ""
            st.rerun()

# 5. Gemini AI Generation Core
def generate_ai(prompt_text):
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
        with st.spinner("✨ Gemini is generating your viral content..."):
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

# 6. Hero Header
st.markdown("""
<div style="text-align: center; padding: 15px 0 10px 0;">
    <h1 class="gemini-title">TaskPilot AI Studio</h1>
    <p style="color: #A0AEC0; font-size: 1.1rem; max-width: 600px; margin: 0 auto 15px auto;">
        Create scroll-stopping viral scripts and hooks for YouTube, Instagram & Facebook in 30 seconds.
    </p>
</div>
""", unsafe_allow_html=True)

# 7. Guaranteed Anime Avatar SVG Component
st.markdown("""
<div class="anime-box">
    <svg width="65" height="65" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="border-radius:50%; box-shadow: 0 0 20px rgba(0, 242, 254, 0.6); flex-shrink: 0; background: linear-gradient(135deg, #1f1c2c, #928dab);">
        <circle cx="50" cy="50" r="46" fill="#131722" stroke="#00f2fe" stroke-width="2"/>
        <path d="M22 42C24 25 36 15 50 15C64 15 76 25 78 42C72 32 60 30 50 34C40 30 28 32 22 42Z" fill="#ff4b8b"/>
        <ellipse cx="50" cy="56" rx="26" ry="24" fill="#ffdfba"/>
        <path d="M24 40C25 55 28 62 30 65C28 55 27 46 26 40Z" fill="#ff4b8b"/>
        <path d="M76 40C75 55 72 62 70 65C72 55 73 46 74 40Z" fill="#ff4b8b"/>
        <ellipse cx="38" cy="54" rx="6" ry="8" fill="#111"/>
        <ellipse cx="62" cy="54" rx="6" ry="8" fill="#111"/>
        <ellipse cx="38" cy="55" rx="5" ry="6" fill="#00f2fe"/>
        <ellipse cx="62" cy="55" rx="5" ry="6" fill="#00f2fe"/>
        <circle cx="36" cy="52" r="2.5" fill="#fff"/>
        <circle cx="60" cy="52" r="2.5" fill="#fff"/>
        <path d="M46 65C48 68 52 68 54 65" stroke="#d63031" stroke-width="1.8" stroke-linecap="round"/>
        <path d="M20 28L30 14L34 26" fill="#00f2fe" stroke="#fff" stroke-width="1.5"/>
        <path d="M80 28L70 14L66 26" fill="#00f2fe" stroke="#fff" stroke-width="1.5"/>
    </svg>
    <div>
        <h4 style="margin: 0 0 4px 0; color: #FFF; font-weight: 700;">✨ Kon'nichiwa Creator! I am Kira, your AI Viral Sensei</h4>
        <p style="margin: 0; color: #CBD5E0; font-size: 0.92rem;">
            Pick your platform below, enter your topic, and click Generate! I'll craft high-retention viral hooks in seconds! 🚀
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# 8. Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📺 YouTube Studio",
    "📸 Instagram Reels",
    "📘 Facebook Viral",
    "⏰ Best Upload Times",
    "🔥 Viral Page Blueprint (VIP)",
    "💎 Subscriptions & UPI Pay"
])

LANGUAGES = [
    "English", "Tamil", "Tanglish (Tamil + English)", "Hindi", "Telugu", 
    "Malayalam", "Kannada", "Spanish", "French", "German", "Arabic", "Japanese"
]

# Tab 1: YouTube
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📺 YouTube Viral Script & Shorts Engine")
    col1, col2, col3 = st.columns(3)
    with col1:
        yt_topic = st.text_input("Video Topic:", placeholder="e.g. 5 AI Websites to Make Passive Income", key="y_t")
    with col2:
        yt_format = st.selectbox("Format:", ["YouTube Shorts (< 60s)", "Long Video Script (8-10m)", "Titles & Thumbnails"], key="y_f")
    with col3:
        yt_lang = st.selectbox("Language:", LANGUAGES, key="y_l")
    
    if st.button("Generate YouTube Package 🚀", key="y_btn", use_container_width=True):
        if yt_topic.strip():
            p = f"Act as top YouTube strategist. Topic: {yt_topic}, Format: {yt_format}, Language: {yt_lang}. Provide 3 Clickable Titles, 3 First-3-Seconds Visual Hooks, Full Script with visual cues, ending CTA, and 10 SEO Tags."
            out = generate_ai(p)
            if out:
                st.markdown("---")
                st.markdown(out)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Instagram
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📸 Instagram Reels & Hook Studio")
    col1, col2, col3 = st.columns(3)
    with col1:
        ig_topic = st.text_input("Reel Topic:", placeholder="e.g. 3 Video Editing Tricks in CapCut", key="i_t")
    with col2:
        ig_format = st.selectbox("Format:", ["Viral Reel (15-30s)", "Carousel Post Script", "Story Funnel"], key="i_f")
    with col3:
        ig_lang = st.selectbox("Language:", LANGUAGES, key="i_l")
        
    if st.button("Generate Instagram Script ⚡", key="i_btn", use_container_width=True):
        if ig_topic.strip():
            p = f"Act as Instagram algorithm specialist. Topic: {ig_topic}, Format: {ig_format}, Language: {ig_lang}. Provide 3 Visual Hooks, 15-30s Voiceover Script, High-Converting Caption with 'Comment [KEYWORD]', and 15 Viral Hashtags."
            out = generate_ai(p)
            if out:
                st.markdown("---")
                st.markdown(out)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Facebook
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📘 Facebook Viral Video & Discussion Engine")
    col1, col2 = st.columns(2)
    with col1:
        fb_topic = st.text_input("Story / Topic:", placeholder="e.g. Inspiring success story of a college dropout", key="f_t")
    with col2:
        fb_lang = st.selectbox("Language:", LANGUAGES, key="f_l")
        
    if st.button("Generate Facebook Content 🚀", key="f_btn", use_container_width=True):
        if fb_topic.strip():
            p = f"Write an emotionally engaging Facebook video script and viral post about: {fb_topic} in {fb_lang}. Include 1 engaging question to generate 100+ comments."
            out = generate_ai(p)
            if out:
                st.markdown("---")
                st.markdown(out)
        else:
            st.warning("Please enter a topic.")
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Best Upload Times
with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⏰ Best Peak Uploading Hours")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        #### 📺 YouTube
        * **India (IST):** 12:00 PM – 2:00 PM & 6:00 PM – 9:00 PM
        * **Best Days:** Thursday, Friday, Saturday
        * *Upload as Unlisted 1 hr early for HD render.*
        """)
    with col2:
        st.markdown("""
        #### 📸 Instagram Reels
        * **India (IST):** 8:30 AM – 9:30 AM & 7:30 PM – 10:00 PM
        * **Best Days:** Wednesday, Thursday, Sunday
        * *Use trending audio within first 48 hrs.*
        """)
    with col3:
        st.markdown("""
        #### 📘 Facebook
        * **India (IST):** 1:00 PM – 3:30 PM & 7:00 PM – 9:30 PM
        * **Best Days:** Tuesday, Thursday, Friday
        * *Vertical clips with captions perform best.*
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 5: Viral Page Blueprint (VIP)
with tab5:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔥 360° Social Media Viral Page Blueprint & Audit (VIP)")
    u_info = db["users"].get(st.session_state.user_email, {"is_vip": False})
    if not u_info.get("is_vip", False):
        st.warning("🔒 This advanced audit suite is reserved for Basic, Standard, and Premium Subscribers.")
        st.markdown("""
        * ✅ Complete Channel/Profile Bio Optimization (10x Follower Conversion)
        * ✅ 30-Day Content Calendar (Exact video topics to post Mon–Sun)
        * ✅ Algorithmic Retention Hacks to hit Explore feeds
        * 👉 **Upgrade in the Subscriptions tab to unlock instantly!**
        """)
    else:
        st.success("🔓 VIP Active! Enter your channel details:")
        v_niche = st.text_input("Your Channel Niche:", placeholder="e.g. Video Editing, Technology, Fitness")
        col1, col2 = st.columns(2)
        with col1:
            v_plat = st.selectbox("Platform:", ["YouTube Channel", "Instagram Page", "Both Platforms"])
        with col2:
            v_goal = st.selectbox("Goal:", ["First 10,000 Organic Followers", "Monetization & AdSense", "Sell Courses / Products"])
            
        if st.button("Generate My 30-Day Viral Blueprint 🚀", use_container_width=True):
            p = f"Act as viral growth consultant. Niche: {v_niche}, Platform: {v_plat}, Goal: {v_goal}. Produce high-converting bio, 30-day weekly content calendar, retention triggers, and monetization funnel."
            out = generate_ai(p)
            if out:
                st.markdown("---")
                st.markdown(out)
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 6: Subscriptions & UPI Pay
with tab6:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>💎 Choose Your Growth Plan</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="price-box">
            <h3>🥉 Basic Plan</h3>
            <h1 style="color:#4facfe;">₹49</h1>
            <p>50 AI Script Generations<br>YouTube Shorts & Reels<br>High-CTR Titles & Hooks</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="price-box popular-border">
            <span style="background:#00f2fe; color:#000; font-size:11px; font-weight:800; padding:2px 8px; border-radius:10px;">MOST POPULAR 🔥</span>
            <h3 style="margin-top:6px;">🥈 Standard Plan</h3>
            <h1 style="color:#00f2fe;">₹149</h1>
            <p>300 AI Script Generations<br>All Platforms (YT, IG, FB)<br>Full Viral Page Blueprint</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="price-box">
            <span style="background:#ff4b8b; color:#fff; font-size:11px; font-weight:800; padding:2px 8px; border-radius:10px;">LIFETIME PASS 👑</span>
            <h3 style="margin-top:6px;">🥇 Premium VIP</h3>
            <h1 style="color:#ff4b8b;">₹299</h1>
            <p>UNLIMITED Generations Forever<br>All Future Features<br>1-on-1 Creator Support</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    selected_plan = st.radio("Select Plan to Generate QR Scanner:", ["Basic Plan (₹49)", "Standard Plan (₹149) 🔥", "Premium VIP (₹299) 👑"], horizontal=True)
    amount = "49" if "49" in selected_plan else ("149" if "149" in selected_plan else "299")
    
    upi_string = f"upi://pay?pa={DEFAULT_UPI_ID}&pn=TaskPilotAI&am={amount}&cu=INR&tn=TaskPilot"
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(upi_string)}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### 📱 Scan to Pay **₹{amount}** via GPay / PhonePe")
        st.image(qr_code_url, width=210, caption="Scan with any UPI App")
        st.markdown(f"**UPI ID:** `{DEFAULT_UPI_ID}`")
        st.markdown(f'<a href="{upi_string}" target="_blank" style="display:inline-block; background:#00f2fe; color:#000; padding:8px 18px; border-radius:10px; text-decoration:none; font-weight:700;">📲 Pay via UPI App (Mobile)</a>', unsafe_allow_html=True)
        
    with col2:
        st.markdown("#### ⚡ Instant Activation")
        u_email_input = st.text_input("Your Registered Email:", value=st.session_state.user_email, placeholder="yourname@gmail.com")
        utr_num = st.text_input("12-Digit UPI Transaction ID / UTR:", placeholder="e.g. 425678912345")
        if st.button("Submit Payment & Get Code 🚀", use_container_width=True):
            if len(utr_num.strip()) >= 6 and "@" in u_email_input:
                db["payment_logs"].append({"email": u_email_input.strip().lower(), "utr": utr_num.strip(), "amount": amount})
                save_db(db)
                st.success("🎉 Payment Received! Your Activation Code is: **`VIP2026`**")
                st.info("Enter this code in the left sidebar to unlock unlimited access!")
            else:
                st.error("Please enter a valid email and 12-digit UTR.")
    st.markdown('</div>', unsafe_allow_html=True)
