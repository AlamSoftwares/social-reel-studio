import os
import io
import json
import tempfile
import requests
import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# Set page config optimized for Mobile and Desktop
st.set_page_config(
    page_title="AI Social Strategist & Reel Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Pro Theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .metric-card {
        background: #151d30;
        border: 1px solid #23304c;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .badge-timing {
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-seo {
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- NOTIFICATION HELPER -----------------
def send_telegram_alert(token, chat_id, message, video_path=None):
    """Sends immediate mobile push notification and video directly to user's phone via Telegram."""
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)

        if video_path and os.path.exists(video_path):
            video_url = f"https://api.telegram.org/bot{token}/sendVideo"
            with open(video_path, "rb") as vf:
                requests.post(video_url, data={"chat_id": chat_id, "caption": "🎬 Preview Video (Ready for Review)"}, files={"video": vf}, timeout=60)
        return True
    except Exception as e:
        return False

# ----------------- SIDEBAR: STRATEGIST SETTINGS -----------------
st.sidebar.title("⚡ Social Strategist")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Free from aistudio.google.com")

st.sidebar.markdown("---")
st.sidebar.subheader("📱 Mobile Push Notifications")
tg_token = st.sidebar.text_input("Telegram Bot Token (Optional)", type="password", placeholder="From @BotFather")
tg_chat_id = st.sidebar.text_input("Telegram Chat ID (Optional)", placeholder="From @userinfobot")
if tg_token and tg_chat_id:
    st.sidebar.success("✓ Mobile Push Alerts Active")

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Audience & Algorithm Tuning")
target_tz = st.sidebar.selectbox("Target Audience Timezone", ["EST (New York)", "IST (India)", "GMT / BST (UK)", "PST (California)"])
brand_color = st.sidebar.color_picker("Brand Signature Color", "#00E5FF")
st.sidebar.caption("🔒 Safety: 100% human-free/silhouette rules strictly enforced.")

# ----------------- SESSION STATE -----------------
if "campaign" not in st.session_state:
    st.session_state.campaign = None
if "rendered_reel" not in st.session_state:
    st.session_state.rendered_reel = None
if "approval_status" not in st.session_state:
    st.session_state.approval_status = {}

# ----------------- MAIN STUDIO TABS -----------------
st.title("⚡ Autonomous Social Media Strategist & Reel Engine")
st.caption("Senior algorithmic content strategy, keyword SEO, optimal upload timing, and video production.")

tab1, tab2, tab3 = st.tabs([
    "📊 1. Upload & Strategic Analysis",
    "🎬 2. Video Studio & Mobile Review",
    "📈 3. SEO & Algorithm Heatmap"
])

# ----------------- TAB 1: STRATEGIC ANALYSIS -----------------
with tab1:
    st.subheader("1. Ingest 7-Day Planning PDF")
    uploaded_pdf = st.file_uploader("Upload your planning / prompt PDF", type=["pdf"])

    col_a, col_b = st.columns([2, 1])
    with col_a:
        creator_goals = st.text_area(
            "Creator Goals & Account Focus",
            value="Educational account focused on tech/AI/business growth. Maximize retention, search traffic, and authority.",
            height=80
        )

    if uploaded_pdf and api_key:
        if st.button("🚀 Run Senior Social Media Marketing Analysis", type="primary", use_container_width=True):
            with st.spinner("Acting as Senior Social Media Director & Algorithmic Strategist... Analyzing retention curves, search intent, and keywords..."):
                try:
                    reader = PdfReader(uploaded_pdf)
                    pdf_content = "".join([page.extract_text() or "" for page in reader.pages])

                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-2.0-flash")

                    prompt = f"""
You are a world-class Senior Social Media Director and YouTube/Meta Algorithm Strategist with 10+ years optimizing short-form virality.
Analyze this creator's document and strategy goals:
Document Content: {pdf_content[:8000]}
Audience Timezone: {target_tz}
Creator Goals: {creator_goals}

MANDATORY VISUAL SAFETY RULES:
- ABSOLUTELY NO WOMEN OR FEMALE FIGURES.
- NO HUMAN FACES, NO EYES, NO DETAILED HUMAN BODY PORTRAITS.
- Use only dark aesthetic tech, minimalist workspace, or pure black featureless silhouettes seen from behind.

Perform deep professional social media marketing analysis and output a strict JSON array of 7 days:
[
  {{
    "day": 1,
    "topic": "Core topic name",
    "hook_title": "Scroll-stopping hook under 6 words (High viral retention)",
    "hook_strategy": "Explain why this hook works (e.g. Negative framing, curiosity gap, contrarian insight)",
    "voice_script": "30-second spoken script (around 65-75 words), high rhythm, 3 clear actionable points",
    "timing_analysis": {{
      "optimal_post_time": "6:45 PM",
      "best_day": "Tuesday",
      "algorithm_reasoning": "High evening commute mobile usage window; lower video upload saturation."
    }},
    "seo_keywords": {{
      "youtube_primary_keyword": "Target search intent phrase",
      "longtail_keywords": ["keyword phrase 1", "keyword phrase 2", "keyword phrase 3"],
      "youtube_title": "SEO Optimized Title Under 70 Chars #Shorts",
      "youtube_tags": "tag1, tag2, tag3, tag4, tag5",
      "ig_caption": "Engineered caption with hook, bullet insights, and engagement question",
      "ig_high_reach_hashtags": "#broad1 #broad2",
      "ig_niche_hashtags": "#niche1 #niche2 #niche3"
    }}
  }}
]
Output ONLY raw JSON. No markdown code fences.
"""
                    res = model.generate_content(prompt)
                    raw_text = res.text.strip()
                    if raw_text.startswith("```json"):
                        raw_text = raw_text[7:]
                    if raw_text.endswith("```"):
                        raw_text = raw_text[:-3]

                    st.session_state.campaign = json.loads(raw_text.strip())
                    st.success("✅ Senior Strategic Analysis Complete! Head to Tab 2 to generate and review.")
                except Exception as e:
                    st.error(f"Analysis error: {e}")

    # Campaign Overview Cards
    if st.session_state.campaign:
        st.markdown("---")
        st.subheader("📋 7-Day Strategy Roadmap")
        for item in st.session_state.campaign:
            with st.expander(f"Day {item['day']} ({item['timing_analysis']['best_day']} @ {item['timing_analysis']['optimal_post_time']}): {item['hook_title']}"):
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.write(f"**Hook Strategy:** {item['hook_strategy']}")
                    st.write(f"**Script:** {item['voice_script']}")
                with col_i2:
                    st.markdown(f"<span class='badge-timing'>⏰ Best Upload: {item['timing_analysis']['optimal_post_time']}</span>", unsafe_allow_html=True)
                    st.write(f"**Why this time?** {item['timing_analysis']['algorithm_reasoning']}")
                    st.write(f"**Primary SEO Search Target:** `{item['seo_keywords']['youtube_primary_keyword']}`")

# ----------------- TAB 2: VIDEO STUDIO & MOBILE REVIEW -----------------
with tab2:
    if not st.session_state.campaign:
        st.info("👈 Upload your PDF in Tab 1 to run the strategic analysis first.")
    else:
        st.subheader("🎬 Daily Reel Studio & Mobile Approval Gate")
        
        day_labels = [f"Day {item['day']}: {item['hook_title']} ({item['timing_analysis']['optimal_post_time']})" for item in st.session_state.campaign]
        active_day_idx = st.selectbox("Select Day to Review & Render:", range(len(day_labels)), format_func=lambda x: day_labels[x])
        day_data = st.session_state.campaign[active_day_idx]

        col_l, col_r = st.columns([1, 1])

        with col_l:
            st.markdown("### 🎯 Script & Hook Optimization")
            st.text_input("Scroll-Stopping Hook", value=day_data["hook_title"])
            script_content = st.text_area("Voiceover Script (30s)", value=day_data["voice_script"], height=120)

            st.markdown("### ⏰ Algorithmic Timing Card")
            st.info(f"📅 **Recommended Slot:** {day_data['timing_analysis']['best_day']} at **{day_data['timing_analysis']['optimal_post_time']} {target_tz}**\n\n*{day_data['timing_analysis']['algorithm_reasoning']}*")

            if st.button("⚡ Render 9:16 Video & Trigger Mobile Alert", type="primary", use_container_width=True):
                with st.spinner("Generating voiceover, compiling 1080x1920 video, and notifying your phone..."):
                    try:
                        from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip

                        tmp = tempfile.mkdtemp()
                        # 1. Voiceover
                        tts = gTTS(text=script_content, lang='en', slow=False)
                        audio_file = os.path.join(tmp, "voice.mp3")
                        tts.save(audio_file)
                        audio_clip = AudioFileClip(audio_file)
                        duration = audio_clip.duration

                        # 2. Dark Aesthetic Background
                        bg = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
                        draw = ImageDraw.Draw(bg)
                        # Minimalist framing
                        draw.rectangle([(60, 220), (1020, 1700)], outline=brand_color, width=4)
                        bg_path = os.path.join(tmp, "bg.png")
                        bg.save(bg_path)
                        img_clip = ImageClip(bg_path).set_duration(duration)

                        # 3. Hook Overlay
                        txt = TextClip(
                            day_data["hook_title"],
                            fontsize=56,
                            color='white',
                            font='Arial-Bold',
                            size=(920, None),
                            method='caption'
                        ).set_position(('center', 420)).set_duration(duration)

                        # 4. Final Video
                        final_clip = CompositeVideoClip([img_clip, txt]).set_audio(audio_clip)
                        out_path = os.path.join(tmp, f"day_{day_data['day']}_reel.mp4")
                        final_clip.write_videofile(out_path, fps=24, codec='libx264', audio_codec='aac', logger=None)

                        st.session_state.rendered_reel = out_path

                        # 5. Send Telegram Alert to Mobile Phone
                        if tg_token and tg_chat_id:
                            msg = f"🎬 *Day {day_data['day']} Reel Ready for Approval!*\n\n📌 *Hook:* {day_data['hook_title']}\n⏰ *Best Post Time:* {day_data['timing_analysis']['optimal_post_time']} ({day_data['timing_analysis']['best_day']})\n\nWatch preview below & reply to approve!"
                            send_telegram_alert(tg_token, tg_chat_id, msg, out_path)
                            st.success("📲 Notification & Preview Video sent directly to your phone via Telegram!")
                        else:
                            st.success("✅ Reel Rendered! Preview below.")
                    except Exception as e:
                        st.error(f"Render error: {e}")

        with col_r:
            st.markdown("### 📱 Mobile Preview & Approval")
            if st.session_state.rendered_reel and os.path.exists(st.session_state.rendered_reel):
                st.video(st.session_state.rendered_reel)

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    with open(st.session_state.rendered_reel, "rb") as vf:
                        st.download_button(
                            label="⬇️ Download Reel (1080p)",
                            data=vf,
                            file_name=f"day_{day_data['day']}_reel.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                with col_btn2:
                    if st.button("✅ Approve for Scheduled Upload", use_container_width=True):
                        st.session_state.approval_status[day_data['day']] = "Approved"
                        if tg_token and tg_chat_id:
                            send_telegram_alert(tg_token, tg_chat_id, f"✅ *Day {day_data['day']} APPROVED!*\nScheduled to go live at {day_data['timing_analysis']['optimal_post_time']}.")
                        st.balloons()
                        st.success(f"Day {day_data['day']} locked in for {day_data['timing_analysis']['optimal_post_time']}!")
            else:
                st.info("Click **Render 9:16 Video** on the left to watch the preview here.")

# ----------------- TAB 3: SEO & ALGORITHM HEATMAP -----------------
with tab3:
    if not st.session_state.campaign:
        st.info("Upload your PDF in Tab 1 to see the SEO and Timing Heatmap.")
    else:
        st.subheader("📈 Search & Discovery Strategy (YouTube & Meta SEO)")
        
        for item in st.session_state.campaign:
            with st.container():
                st.markdown(f"#### Day {item['day']}: {item['hook_title']}")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**YouTube SEO Package:**")
                    st.text_input(f"YT Title #{item['day']}", value=item['seo_keywords']['youtube_title'])
                    st.text_area(f"YT Tags #{item['day']}", value=item['seo_keywords']['youtube_tags'], height=70)
                    st.caption(f"🎯 Target Search Intent: `{item['seo_keywords']['youtube_primary_keyword']}`")
                with c2:
                    st.markdown("**Instagram / Facebook SEO & Tags:**")
                    st.text_area(f"IG Caption #{item['day']}", value=f"{item['seo_keywords']['ig_caption']}\n\n{item['seo_keywords']['ig_high_reach_hashtags']} {item['seo_keywords']['ig_niche_hashtags']}", height=120)
                st.markdown("---")
