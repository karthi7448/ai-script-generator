import streamlit as st
from google import genai

st.set_page_config(
    page_title="TaskPilot AI - Viral Content Suite",
    page_icon="⚡",
    layout="wide"
)

# ----------------- Secrets & State -----------------
api_key = st.secrets.get("GEMINI_API_KEY", None)

if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "credits" not in st.session_state:
    st.session_state.credits = 3
if "is_vip" not in st.session_state:
    st.session_state.is_vip = False

# VIP Activation Passcodes (Pay pannavangalukku indha code tharalam)
VIP_PASSCODES = ["VIP2026", "PROCREATOR", "TASKPILOT99", "KARTHI7448"]

# ----------------- Sidebar (Auth & Profile) -----------------
st.sidebar.title("⚡ TaskPilot AI")

if not st.session_state.user_email:
    st.sidebar.subheader("🔑 Sign In to Start")
    email_input = st.sidebar.text_input("Enter Email to get 3 Free Credits:", placeholder="yourname@gmail.com")
    if st.sidebar.button("Claim 3 Free Credits 🎁"):
        if "@" in email_input and "." in email_input:
            st.session_state.user_email = email_input.strip()
            st.rerun()
        else:
            st.sidebar.error("Please enter a valid email address.")
else:
    st.sidebar.success(f"👤 {st.session_state.user_email}")
    if st.session_state.is_vip:
        st.sidebar.markdown("### 👑 Status: **VIP Pro Member**")
        st.sidebar.caption("Unlimited generations unlocked!")
    else:
        st.sidebar.markdown(f"### ⚡ **Credits: {st.session_state.credits} / 3 Free**")

    # VIP Passcode Unlock
    if not st.session_state.is_vip:
        st.sidebar.markdown("---")
        passcode = st.sidebar.text_input("Have a VIP Code? Enter here:", type="password")
        if st.sidebar.button("Unlock VIP 🔓"):
            if passcode.strip() in VIP_PASSCODES:
                st.session_state.is_vip = True
                st.sidebar.success("🎉 VIP Activated! Unlimited access granted.")
                st.rerun()
            else:
                st.sidebar.error("Invalid passcode. Pay via UPI below to receive code.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Upgrade (UPI)")
    st.sidebar.write("• Starter: ₹49 (50 Credits)")
    st.sidebar.write("• Pro Creator: ₹149 (300 Credits)")
    st.sidebar.write("• VIP Unlimited: ₹299 (Lifetime)")
    st.sidebar.info("GPay / PhonePe UPI: `yourname@upi`\nWhatsApp screenshot for code.")
    if st.sidebar.button("Logout"):
        st.session_state.user_email = ""
        st.session_state.credits = 3
        st.session_state.is_vip = False
        st.rerun()

# ----------------- Helper Generation Function -----------------
def generate_ai_content(prompt_text):
    if not st.session_state.user_email:
        st.warning("👉 Please enter your email in the left sidebar to claim your 3 free credits!")
        return None

    if not st.session_state.is_vip and st.session_state.credits <= 0:
        st.error("❌ Your 3 free credits are finished! Upgrade to a plan in the '💎 Pricing & Plans' tab to continue.")
        return None

    if not api_key:
        st.error("API Key not found. Please ensure GEMINI_API_KEY is configured in Streamlit Secrets.")
        return None

    try:
        client = genai.Client(api_key=api_key)
        with st.spinner("⚡ AI is generating your viral content..."):
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt_text
            )
            # Free user-ku credit korayum
            if not st.session_state.is_vip:
                st.session_state.credits -= 1
            return response.text
    except Exception as e:
        st.error(f"Generation error: {e}")
        return None

# ----------------- Main Interface -----------------
st.title("🚀 TaskPilot AI: All-In-One Social Media Growth Suite")
st.markdown("Create viral scripts, hooks, and growth strategies for **YouTube, Instagram, and Facebook** in seconds.")

tab_yt, tab_ig, tab_fb, tab_time, tab_viral, tab_pricing = st.tabs([
    "📺 YouTube Scripts",
    "📸 Instagram Reels",
    "📘 Facebook Viral",
    "⏰ Best Upload Times",
    "🔥 Viral Page Setup (VIP)",
    "💎 Pricing & Plans"
])

# ----------------- Tab 1: YouTube -----------------
with tab_yt:
    st.subheader("📺 YouTube Viral Script & Shorts Generator")
    yt_topic = st.text_input("YouTube Video Topic:", placeholder="e.g. 5 AI tools that will save 10 hours a week", key="yt_topic")
    col1, col2 = st.columns(2)
    with col1:
        yt_type = st.selectbox("Format:", ["YouTube Shorts (Under 60s)", "Long Video Outline & Hook (8-10 mins)"], key="yt_type")
        yt_lang = st.selectbox("Language:", ["Tamil", "Tanglish (Tamil + English)", "English", "Hindi"], key="yt_lang")
    with col2:
        yt_tone = st.selectbox("Tone:", ["High-Energy & Retention", "Educational & Trustworthy", "Storytelling / Mystery"], key="yt_tone")

    if st.button("Generate YouTube Script 🚀", key="yt_btn"):
        if yt_topic.strip():
            p = f"""
            You are an elite YouTube strategist.
            Topic: {yt_topic}
            Format: {yt_type}
            Language: {yt_lang}
            Tone: {yt_tone}

            Provide:
            1. 3 High-CTR Title Ideas
            2. 3 Opening Hook Variations (First 5 seconds)
            3. Full Script with [Visual Cue] and [B-Roll Notes]
            4. Ending Call To Action (Subscribers & Comments)
            5. Top 10 High-Ranking SEO Tags & Keywords
            """
            res = generate_ai_content(p)
            if res:
                st.success("Generated successfully!")
                st.markdown(res)
        else:
            st.warning("Please enter a topic.")

# ----------------- Tab 2: Instagram -----------------
with tab_ig:
    st.subheader("📸 Instagram Reels & Hook Generator")
    ig_topic = st.text_input("Reel / Post Topic:", placeholder="e.g. How to edit viral videos on CapCut mobile", key="ig_topic")
    col1, col2 = st.columns(2)
    with col1:
        ig_format = st.selectbox("Content Type:", ["Viral Reel (15-30s)", "Carousel Post Script", "Story Series Script"], key="ig_format")
        ig_lang = st.selectbox("Language:", ["Tamil", "Tanglish (Tamil + English)", "English", "Hindi"], key="ig_lang")
    with col2:
        ig_vibe = st.selectbox("Style:", ["Fast-Paced & Relatable", "Luxury / Aesthetic", "Controversial Hook / Myth Busting"], key="ig_vibe")

    if st.button("Generate Instagram Script ⚡", key="ig_btn"):
        if ig_topic.strip():
            p = f"""
            You are a top Instagram algorithm creator.
            Topic: {ig_topic}
            Format: {ig_format}
            Language: {ig_lang}
            Style: {ig_vibe}

            Provide:
            1. 3 Scroll-Stopping Visual Hooks (Screen text + Gesture)
            2. Audio/Voiceover Script (Timed for 15-30s)
            3. High-Conversion Caption with 'Comment [KEYWORD]' trigger
            4. 15 Categorized Viral Hashtags (Niche, Trending, Broad)
            """
            res = generate_ai_content(p)
            if res:
                st.success("Generated successfully!")
                st.markdown(res)
        else:
            st.warning("Please enter a topic.")

# ----------------- Tab 3: Facebook -----------------
with tab_fb:
    st.subheader("📘 Facebook Viral Video & Discussion Post")
    fb_topic = st.text_input("Facebook Topic:", placeholder="e.g. Inspiring story or shocking business reality", key="fb_topic")
    fb_lang = st.selectbox("Language:", ["Tamil", "Tanglish", "English"], key="fb_lang")
    if st.button("Generate Facebook Content 🚀", key="fb_btn"):
        if fb_topic.strip():
            p = f"""
            Write a viral Facebook video script and discussion post for: {fb_topic} in {fb_lang}.
            Make it emotionally engaging, encouraging shares and comments.
            Include 1 engaging question at the end to boost comment count.
            """
            res = generate_ai_content(p)
            if res:
                st.success("Generated successfully!")
                st.markdown(res)
        else:
            st.warning("Please enter a topic.")

# ----------------- Tab 4: Best Upload Times -----------------
with tab_time:
    st.subheader("⏰ Best Uploading Times Guide (India - IST)")
    st.write("Post during these peak traffic hours to maximize algorithm boost and get initial high velocity:")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.markdown("""
        ### 📺 YouTube
        * **Weekdays (Mon-Fri):**
          * ⏰ **12:00 PM – 2:00 PM** (Lunch break)
          * ⏰ **6:00 PM – 9:00 PM** (Peak evening traffic)
        * **Weekends (Sat-Sun):**
          * ⏰ **9:00 AM – 11:00 AM**
          * ⏰ **4:00 PM – 8:00 PM**
        * *Pro-Tip: Upload as 'Unlisted' 1 hour early so YouTube processes HD/4K resolution.*
        """)

    with col_t2:
        st.markdown("""
        ### 📸 Instagram
        * **Best Days:** Wednesday, Thursday, Sunday
        * **Best Hours:**
          * ⏰ **8:30 AM – 9:30 AM** (Morning scroll)
          * ⏰ **1:00 PM – 2:30 PM** (Lunch break)
          * ⏰ **7:30 PM – 10:00 PM** (Highest reel views)
        * *Pro-Tip: Keep reels between 7-15s with trending audio for faster viral push.*
        """)

    with col_t3:
        st.markdown("""
        ### 📘 Facebook
        * **Best Days:** Tuesday, Thursday, Friday
        * **Best Hours:**
          * ⏰ **1:00 PM – 3:00 PM**
          * ⏰ **7:00 PM – 9:00 PM**
        * *Pro-Tip: Longer storytelling posts + 1-3 min vertical videos get maximum shares.*
        """)

# ----------------- Tab 5: Viral Page Growth (VIP) -----------------
with tab_viral:
    st.subheader("🔥 Social Media Viral Page Setup & Audit (VIP Feature)")
    if not st.session_state.is_vip:
        st.warning("🔒 This feature is reserved for VIP Subscribers.")
        st.markdown("""
        **What you get with VIP Page Setup:**
        * ✅ Complete Profile / Bio Optimization (High Follower Conversion)
        * ✅ Weekly Content Roadmap (What to post Mon–Sun)
        * ✅ Retention & Algorithm Hacks to push videos to Explore & Suggestion feeds
        * ✅ Custom Monetization Plan (How to convert viewers into paying buyers/clients)
        
        👉 **Upgrade to VIP in the Pricing tab or enter your VIP code in the left sidebar to unlock!**
        """)
    else:
        st.success("🔓 VIP Unlocked! Enter your page details for custom audit:")
        niche = st.text_input("Your Channel/Page Niche:", placeholder="e.g. Tech Reviews, Video Editing, Fitness")
        platform = st.selectbox("Target Platform:", ["YouTube Channel", "Instagram Page", "Both YouTube & Instagram"])
        goal = st.selectbox("Main Goal:", ["Reach first 10,000 followers", "Get monetized / High views", "Sell online course or services"])
        
        if st.button("Generate My Viral Growth Blueprint 🚀"):
            p = f"""
            Act as an elite viral social media consultant.
            Niche: {niche}
            Platform: {platform}
            Goal: {goal}
            
            Provide an actionable, step-by-step master plan:
            1. High-Converting Bio / About Section with clear CTA
            2. First 30 Days Content Roadmap (Exact themes to cover)
            3. Algorithm triggers to maximize watch time and shares
            4. 3 Critical Mistakes to avoid that kill page reach
            5. Exact monetization funnel to convert viewers into paying subscribers
            """
            res = generate_ai_content(p)
            if res:
                st.markdown(res)

# ----------------- Tab 6: Pricing & Plans -----------------
with tab_pricing:
    st.subheader("💎 Simple, Creator-Friendly Pricing Plans")
    st.caption("Start with 3 free trial credits, then choose a plan that fits your growth.")

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
        ### 🥉 Starter Plan
        ## **₹49** <small>/ one-time</small>
        * ✅ **50 AI Script Generations**
        * ✅ YouTube Shorts & Reels
        * ✅ Viral Hooks & Title Ideas
        * ❌ Viral Page Audit
        * ❌ Priority WhatsApp Support
        """, unsafe_allow_html=True)
        st.info("Pay **₹49** via UPI: `yourname@upi`")

    with p2:
        st.markdown("""
        ### 🥈 Pro Creator 🔥
        ## **₹149** <small>/ 300 credits</small>
        * ✅ **300 AI Script Generations**
        * ✅ All Platforms (YouTube, IG, FB)
        * ✅ Best Uploading Times Guide
        * ✅ **Full Viral Page Setup Blueprint**
        * ✅ Email / WhatsApp Support
        """, unsafe_allow_html=True)
        st.success("Pay **₹149** via UPI: `yourname@upi`")

    with p3:
        st.markdown("""
        ### 🥇 VIP Lifetime
        ## **₹299** <small>/ lifetime</small>
        * ✅ **UNLIMITED AI Generations Forever**
        * ✅ All Present & Future AI Features
        * ✅ Full Viral Page Growth Blueprints
        * ✅ Direct 1-on-1 Creator Support
        """, unsafe_allow_html=True)
        st.warning("Pay **₹299** via UPI: `yourname@upi`")

    st.markdown("---")
    st.subheader("📲 How to Activate Your Plan in 1 Minute:")
    st.markdown("""
    1. Send payment to UPI ID: **`yourname@upi`** (GPay / PhonePe / Paytm).
    2. Take a screenshot of the completed payment.
    3. Send the screenshot to WhatsApp: **`+91 98765 43210`**.
    4. You will instantly receive your **VIP Passcode** to enter in the left sidebar!
    """)
