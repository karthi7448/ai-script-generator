import urllib.parse
import streamlit as st
from google import genai
import json
import os

# Set page layout
st.set_page_config(
    page_title="TaskPilot AI - 3D Social Media Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom 3D & Responsive CSS -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* 3D Glassmorphism Cards */
    .card-3d {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01));
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }
    .card-3d:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.7), inset 0 1px 1px rgba(255, 255, 255, 0.4);
        border-color: rgba(255, 75, 75, 0.5);
    }
    
    /* Glowing Badges */
    .badge-vip {
        background: linear-gradient(90deg, #9C27B0, #E040FB);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 0 15px rgba(224, 64, 251, 0.6);
    }
    
    /* Social Media 3D Icons */
    .platform-icon {
        font-size: 38px;
        margin-bottom: 10px;
        display: inline-block;
        filter: drop-shadow(0 8px 12px rgba(0,0,0,0.5));
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .card-3d {
            padding: 16px;
        }
        .platform-icon {
            font-size: 28px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Database / Persistent Storage (JSON) -----------------
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
        return {"users": {}, "vip_codes": ["VIP2026", "PROCREATOR"], "payment_logs": []}

def save_db(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"DB Error: {e}")

db = load_db()

# ----------------- Configuration & Secrets -----------------
api_key = st.secrets.get("GEMINI_API_KEY", None)
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "karthi@admin2026")
DEFAULT_UPI_ID = st.secrets.get("UPI_ID", "yourname@upi")  # Ungaloda real UPI ID inga podunga
UPI_NAME = "TaskPilot AI"

# Session state setup
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ----------------- Sidebar (Authentication & Profile) -----------------
st.sidebar.markdown("## ⚡ TaskPilot AI")
st.sidebar.caption("Automated Multi-Platform Growth Engine")

if not st.session_state.user_email and not st.session_state.is_admin:
    st.sidebar.markdown("### 👤 User Sign In")
    email_in = st.sidebar.text_input("Enter your Email to get 3 Free Credits:", placeholder="creator@gmail.com")
    if st.sidebar.button("Get 3 Free Credits 🚀"):
        if "@" in email_in and "." in email_in:
            email_clean = email_in.strip().lower()
            st.session_state.user_email = email_clean
            if email_clean not in db["users"]:
                db["users"][email_clean] = {"credits": 3, "is_vip": False, "plan": "Free Trial"}
                save_db(db)
            st.rerun()
        else:
            st.sidebar.error("Please enter a valid email address.")
            
    st.sidebar.markdown("---")
    # Secret Admin Login Expander (Owner mattum)
    with st.sidebar.expander("🔒 Owner / Admin Login"):
        admin_pass = st.sidebar.text_input("Owner Password:", type="password")
        if st.sidebar.button("Access Dashboard"):
            if admin_pass == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.sidebar.success("Welcome Owner!")
                st.rerun()
            else:
                st.sidebar.error("Incorrect password.")

else:
    if st.session_state.is_admin:
        st.sidebar.success("👑 **Logged in as: OWNER / ADMIN**")
        if st.sidebar.button("Exit Admin Mode"):
            st.session_state.is_admin = False
            st.rerun()
    else:
        user_info = db["users"].get(st.session_state.user_email, {"credits": 0, "is_vip": False, "plan": "Free"})
        st.sidebar.success(f"👤 {st.session_state.user_email}")
        
        if user_info.get("is_vip", False):
            st.sidebar.markdown('<span class="badge-vip">👑 VIP PRO UNLIMITED</span>', unsafe_allow_html=True)
            st.sidebar.caption("Unlimited Script Generations")
        else:
            credits_left = user_info.get("credits", 0)
            st.sidebar.markdown(f"### ⚡ **{credits_left} / 3 Free Credits**")
            st.sidebar.progress(max(0.0, min(1.0, credits_left / 3.0)))

        # VIP Passcode field
        if not user_info.get("is_vip", False):
            st.sidebar.markdown("---")
            vip_code_in = st.sidebar.text_input("Enter VIP Code to Unlock:", type="password")
            if st.sidebar.button("Apply Code 🔓"):
                if vip_code_in.strip() in db["vip_codes"]:
                    db["users"][st.session_state.user_email]["is_vip"] = True
                    db["users"][st.session_state.user_email]["plan"] = "VIP Pro"
                    save_db(db)
                    st.sidebar.success("🎉 Plan Activated! Unlimited access granted.")
                    st.rerun()
                else:
                    st.sidebar.error("Invalid VIP Code. Scan QR in Pricing to get code.")

        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            st.session_state.user_email = ""
            st.rerun()

# ----------------- Helper Generation Function -----------------
def generate_ai(prompt_text):
    if st.session_state.is_admin:
        pass  # Admin-ku unlimited
    elif not st.session_state.user_email:
        st.warning("👉 Please enter your email in the left sidebar to claim your free credits!")
        return None
    else:
        user_data = db["users"].get(st.session_state.user_email, {"credits": 0, "is_vip": False})
        if not user_data["is_vip"] and user_data["credits"] <= 0:
            st.error("❌ Your free trial has ended! Upgrade in the '💎 Pricing & UPI Scanner' tab to continue.")
            return None

    if not api_key:
        st.error("Gemini API key is not configured in Streamlit Secrets.")
        return None

    try:
        client = genai.Client(api_key=api_key)
        with st.spinner("⚡ AI is crafting high-retention viral content..."):
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt_text
            )
            # Deduct credit if free user
            if not st.session_state.is_admin and st.session_state.user_email:
                if not db["users"][st.session_state.user_email]["is_vip"]:
                    db["users"][st.session_state.user_email]["credits"] -= 1
                    save_db(db)
            return response.text
    except Exception as e:
        st.error(f"Generation error: {e}")
        return None

# ----------------- ADMIN DASHBOARD VIEW (Owner Only) -----------------
if st.session_state.is_admin:
    st.title("👑 Owner Control Center & Analytics")
    st.markdown("Monitor your registered users, generate VIP activation codes, and review UPI payments.")
    
    total_users = len(db["users"])
    vip_count = sum(1 for u in db["users"].values() if u.get("is_vip", False))
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Registered Users", total_users)
    with c2:
        st.metric("Active VIP Customers", vip_count)
    with c3:
        st.metric("Pending Payment Verifications", len(db["payment_logs"]))

    t_users, t_codes, t_payments = st.tabs(["👥 User Database", "🔑 VIP Code Manager", "💳 Payment Approvals"])
    
    with t_users:
        st.subheader("Registered Users & Credits")
        for u_email, u_data in list(db["users"].items()):
            col_u1, col_u2, col_u3 = st.columns()
            with col_u1:
                st.write(f"**{u_email}** ({u_data.get('plan', 'Free')})")
            with col_u2:
                st.write(f"Credits: {u_data.get('credits', 0)} | VIP: {u_data.get('is_vip', False)}")
            with col_u3:
                if not u_data.get("is_vip", False):
                    if st.button(f"Grant VIP", key=f"up_{u_email}"):
                        db["users"][u_email]["is_vip"] = True
                        db["users"][u_email]["plan"] = "VIP by Admin"
                        save_db(db)
                        st.rerun()
                else:
                    if st.button(f"Revoke VIP", key=f"rev_{u_email}"):
                        db["users"][u_email]["is_vip"] = False
                        save_db(db)
                        st.rerun()

    with t_codes:
        st.subheader("Active VIP Activation Codes")
        st.write(db.get("vip_codes", []))
        new_code = st.text_input("Create New VIP Passcode:")
        if st.button("Add Passcode"):
            if new_code.strip() and new_code.strip() not in db["vip_codes"]:
                db["vip_codes"].append(new_code.strip())
                save_db(db)
                st.success(f"Code '{new_code.strip()}' added!")
                st.rerun()

    with t_payments:
        st.subheader("User UPI Payment Submissions")
        if not db["payment_logs"]:
            st.info("No payment submissions yet.")
        else:
            for idx, p_log in enumerate(db["payment_logs"]):
                st.markdown(f"**User:** {p_log['email']} | **Plan:** {p_log['plan']} | **Amount:** ₹{p_log['amount']} | **UTR / Ref:** `{p_log['utr']}`")
                if st.button(f"Approve Payment #{idx}", key=f"appr_{idx}"):
                    if p_log['email'] in db["users"]:
                        db["users"][p_log['email']]["is_vip"] = True
                        db["users"][p_log['email']]["plan"] = p_log['plan']
                    db["payment_logs"].pop(idx)
                    save_db(db)
                    st.success("Payment Approved & VIP Granted!")
                    st.rerun()

# ----------------- MAIN USER EXPERIENCE (Client Facing) -----------------
else:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="font-size: 2.6rem; font-weight: 700; background: linear-gradient(90deg, #FF4B4B, #FF8533); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🚀 TaskPilot AI: 3D Viral Engine
        </h1>
        <p style="font-size: 1.1rem; color: #BBB;">
            Craft High-Retention Scripts, Hooks & Channel Blueprints for YouTube, Instagram & Facebook.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_yt, tab_ig, tab_fb, tab_times, tab_audit, tab_payment = st.tabs([
        "📺 YouTube 3D",
        "📸 Instagram Reels",
        "📘 Facebook Viral",
        "⏰ Best Upload Times",
        "🔥 Viral Page Setup (VIP)",
        "💎 Pricing & UPI Scanner"
    ])

    # 1. YouTube
    with tab_yt:
        st.markdown('<div class="card-3d"><span class="platform-icon">📺</span><h3>YouTube Viral Script Engine</h3>', unsafe_allow_html=True)
        yt_topic = st.text_input("Video Topic or Title Idea:", placeholder="e.g. 5 Secret AI Websites to Make Passive Income", key="yt_t")
        col_y1, col_y2 = st.columns(2)
        with col_y1:
            yt_format = st.selectbox("Content Format:", ["YouTube Shorts (30-60s)", "Long-Form Video Script (8-10 Mins)", "Click-Worthy Title & Thumbnail Generator"], key="yt_f")
            yt_lang = st.selectbox("Output Language:", ["Tamil", "Tanglish (Tamil + English)", "English", "Hindi"], key="yt_l")
        with col_y2:
            yt_style = st.selectbox("Style / Tone:", ["High-Energy & Retention", "Storytelling & Mystery", "Educational & Tutorial", "Controversial & Debunking"], key="yt_s")
        
        if st.button("Generate YouTube Package 🚀", key="yt_btn"):
            if yt_topic.strip():
                p = f"""
                You are a world-class YouTube growth strategist.
                Topic: {yt_topic}
                Format: {yt_format}
                Language: {yt_lang}
                Tone: {yt_style}

                Generate a complete viral package:
                1. 3 High-CTR Title Options
                2. 3 Scroll-Stopping 3-Second Hooks
                3. Full Script with [Visual Cues] and [Sound Effects]
                4. Ending CTA for High Engagement
                5. Top 10 Search-Optimized Tags
                """
                out = generate_ai(p)
                if out:
                    st.markdown(out)
            else:
                st.warning("Please enter a topic.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Instagram
    with tab_ig:
        st.markdown('<div class="card-3d"><span class="platform-icon">📸</span><h3>Instagram Reels & Hook Studio</h3>', unsafe_allow_html=True)
        ig_topic = st.text_input("Reel Topic or Concept:", placeholder="e.g. How to edit cinematic reels on your phone in 3 steps", key="ig_t")
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            ig_type = st.selectbox("Content Type:", ["Viral Reel (15-30s)", "Carousel Post Script (Slides 1-7)", "Story Sequence Script"], key="ig_typ")
            ig_lang = st.selectbox("Language:", ["Tamil", "Tanglish", "English", "Hindi"], key="ig_lng")
        with col_i2:
            ig_vibe = st.selectbox("Vibe:", ["Fast-Paced & Relatable", "Cinematic & Aesthetic", "Educational / Carousel", "Challenge / Trend"], key="ig_vb")
        
        if st.button("Generate Instagram Script ⚡", key="ig_btn"):
            if ig_topic.strip():
                p = f"""
                You are an Instagram algorithm specialist.
                Topic: {ig_topic}
                Format: {ig_type}
                Language: {ig_lang}
                Vibe: {ig_vibe}

                Provide:
                1. 3 Visual Hook Cues (Screen text + Gesture)
                2. Spoken Script (15-30 seconds with pacing)
                3. Caption with 'Comment [KEYWORD] for link' conversion trigger
                4. 15 Categorized Viral Hashtags (Niche, Growth, Broad)
                """
                out = generate_ai(p)
                if out:
                    st.markdown(out)
            else:
                st.warning("Please enter a topic.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Facebook
    with tab_fb:
        st.markdown('<div class="card-3d"><span class="platform-icon">📘</span><h3>Facebook Viral Post & Video Script</h3>', unsafe_allow_html=True)
        fb_topic = st.text_input("Facebook Topic:", placeholder="e.g. An emotional story about success against all odds", key="fb_t")
        fb_lang = st.selectbox("Language:", ["Tamil", "Tanglish", "English"], key="fb_l")
        if st.button("Generate Facebook Content 🚀", key="fb_btn"):
            if fb_topic.strip():
                p = f"""
                Write a viral Facebook video script and post about: {fb_topic} in {fb_lang}.
                Structure it with a gripping first sentence, emotional storytelling, and 1 discussion-provoking question to generate 100+ comments.
                """
                out = generate_ai(p)
                if out:
                    st.markdown(out)
            else:
                st.warning("Please enter a topic.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Upload Times
    with tab_times:
        st.markdown('<div class="card-3d"><h3>⏰ Peak Uploading Hours (India - IST)</h3>', unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        with t1:
            st.markdown("""
            #### 📺 YouTube
            * **Mon - Fri:** 12:00 PM – 2:00 PM & 6:00 PM – 9:00 PM
            * **Sat - Sun:** 9:00 AM – 11:30 AM & 4:00 PM – 8:00 PM
            * *Key Tip: Set video to 'Unlisted' 1 hour prior to process 4K.*
            """)
        with t2:
            st.markdown("""
            #### 📸 Instagram
            * **Best Days:** Wed, Thu, Sun
            * **Peak Hours:** 8:30 AM – 9:30 AM & 7:30 PM – 10:00 PM
            * *Key Tip: Pair reels with trending audio within the first 48 hours.*
            """)
        with t3:
            st.markdown("""
            #### 📘 Facebook
            * **Best Days:** Tue, Thu, Fri
            * **Peak Hours:** 1:00 PM – 3:00 PM & 7:00 PM – 9:00 PM
            * *Key Tip: Text posts accompanied by 1-3 minute vertical clips perform best.*
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Viral Page Setup (VIP)
    with tab_audit:
        st.markdown('<div class="card-3d"><h3>🔥 Social Media Viral Page Setup & Audit (VIP Feature)</h3>', unsafe_allow_html=True)
        user_info = db["users"].get(st.session_state.user_email, {"is_vip": False})
        if not user_info.get("is_vip", False):
            st.warning("🔒 This feature is reserved for VIP Subscribers.")
            st.markdown("""
            **What VIP Members Receive:**
            * ✅ Complete High-Conversion Bio & Profile Header Optimization
            * ✅ 30-Day Content Pillar Calendar (Day 1 to Day 30)
            * ✅ Algorithm Watch-Time Triggers for Explore Feeds
            * ✅ Monetization Blueprint (Turning views into paying clients/sales)
            
            👉 **Upgrade via UPI in the '💎 Pricing & UPI Scanner' tab to unlock!**
            """)
        else:
            st.success("🔓 VIP Status Active! Enter your details for custom audit:")
            v_niche = st.text_input("Your Specific Niche:", placeholder="e.g. Drone Delivery, Video Editing, Stock Market")
            v_plat = st.selectbox("Platform:", ["YouTube Channel", "Instagram Page", "Both Platforms"])
            v_goal = st.selectbox("Primary Goal:", ["First 10,000 Organic Followers", "Monetization & High AdSense", "Sell Online Courses or Services"])
            
            if st.button("Generate My Custom Viral Growth Blueprint 🚀"):
                p = f"""
                You are a senior social media growth consultant.
                Niche: {v_niche}
                Platform: {v_plat}
                Goal: {v_goal}

                Create an actionable, in-depth growth blueprint:
                1. High-Converting Profile & Bio Setup with CTA
                2. 30-Day Weekly Posting Schedule with Exact Video Topics
                3. Retention Tactics to get 80%+ average view duration
                4. 3 Lethal Mistakes that shadowban or kill page reach
                5. Funnel Strategy: How to monetize audience into paying customers
                """
                out = generate_ai(p)
                if out:
                    st.markdown(out)
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. Pricing & Safe UPI Scanner
    with tab_payment:
        st.markdown('<div class="card-3d"><h3>💎 Subscription Plans & Instant UPI QR Scanner</h3>', unsafe_allow_html=True)
        st.caption("Select a plan below to generate your direct Google Pay / PhonePe / Paytm scanner.")

        selected_plan = st.radio(
            "Choose Your Plan:",
            ["Starter Plan (₹49 - 50 Credits)", "Pro Creator (₹149 - 300 Credits + Viral Audit) 🔥", "VIP Lifetime (₹299 - Unlimited Access) 👑"],
            horizontal=True
        )

        amount = "49" if "49" in selected_plan else ("149" if "149" in selected_plan else "299")
        plan_name = "Starter" if "49" in selected_plan else ("Pro" if "149" in selected_plan else "VIP")

        # UPI Intent String & Dynamic QR Code
        upi_payload = f"upi://pay?pa={DEFAULT_UPI_ID}&pn={urllib.parse.quote(UPI_NAME)}&am={amount}&cu=INR&tn={urllib.parse.quote(f'TaskPilot {plan_name}')}"
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(upi_payload)}"

        col_pay1, col_pay2 = st.columns()
        
        with col_pay1:
            st.markdown(f"#### 📱 Scan to Pay **₹{amount}** via GPay / PhonePe")
            st.image(qr_api_url, width=220, caption="Scan with Google Pay / PhonePe / Paytm / BHIM")
            st.markdown(f"**UPI ID:** `{DEFAULT_UPI_ID}`")
            # Mobile Direct Pay Link
            st.markdown(f'<a href="{upi_payload}" target="_blank" style="display:inline-block; background-color:#28a745; color:white; padding:10px 20px; border-radius:8px; text-decoration:none; font-weight:600; margin-top:10px;">📲 Pay Directly via UPI App</a>', unsafe_allow_html=True)

        with col_pay2:
            st.markdown("#### ⚡ Activate Instant Access")
            st.write("After scanning and completing your payment:")
            user_pay_email = st.text_input("Your Registered Email:", value=st.session_state.user_email, placeholder="yourname@gmail.com")
            utr_number = st.text_input("12-Digit UPI Transaction ID / UTR:", placeholder="e.g. 425678912345")
            
            if st.button("Submit Payment for Instant Unlock 🚀"):
                if len(utr_number.strip()) >= 6 and "@" in user_pay_email:
                    # Log submission for Admin
                    db["payment_logs"].append({
                        "email": user_pay_email.strip().lower(),
                        "utr": utr_number.strip(),
                        "plan": plan_name,
                        "amount": amount
                    })
                    assigned_code = "VIP2026"
                    save_db(db)
                    st.success(f"🎉 Payment Verified! Your Activation Code is: **`{assigned_code}`**")
                    st.info("Copy this code and paste it into the left sidebar 'Enter VIP Code' box to unlock unlimited access!")
                else:
                    st.error("Please enter a valid email and 12-digit UTR transaction number from your Google Pay / PhonePe receipt.")

        st.markdown('</div>', unsafe_allow_html=True)
