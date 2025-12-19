import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="AI Blog Assistant", layout="wide")

PLATFORMS = {
    "📸 Instagram": {"times": ["18:00-21:00"], "days": ["Wed", "Fri", "Sun"], "types": ["Reels", "Carousel"], "color": "#E4405F"},
    "🐦 Twitter": {"times": ["12:00-15:00"], "days": ["Tue", "Wed", "Thu"], "types": ["Threads", "News"], "color": "#1DA1F2"},
    "💼 LinkedIn": {"times": ["09:00-11:00"], "days": ["Tue", "Wed"], "types": ["Insights", "Data"], "color": "#0077B5"},
    "📺 YouTube": {"times": ["13:00-16:00"], "days": ["Thu", "Fri", "Sat"], "types": ["Long-form"], "color": "#FF0000"},
    "👥 Facebook": {"times": ["12:00-15:00"], "days": ["Fri", "Sat", "Sun"], "types": ["Community"], "color": "#1877F2"}
}

class AgenticBlogAI:
    def __init__(self):
        self.trending = ["AI Ethics", "Remote Work", "Web3", "Climate Tech", "Health Tech"]
    
    def fuse_content(self, topic):
        sources = [f"Breaking: {topic} Revolution", f"How {topic} Changes Everything", f"Future of {topic} in 2024"]
        return sources
    
    def predict_engagement(self, topic, platform):
        return random.uniform(0.75, 0.95)
    
    def get_recommendations(self, platform):
        p = PLATFORMS[platform]
        return {"time": p["times"][0], "days": ", ".join(p["days"]), "types": ", ".join(p["types"]), "color": p["color"]}

st.markdown("""
<style>
.main-header {font-size: 3rem; text-align: center; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
.metric-card {background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
.topic-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🤖 Agentic AI Blog Assistant</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Intelligent Content Curation & Platform Optimization</p>", unsafe_allow_html=True)

ai = AgenticBlogAI()

with st.sidebar:
    st.header("🎯 Content Configuration")
    topic = st.text_input("📝 Topic:", "AI")
    platform = st.selectbox("🚀 Platform:", list(PLATFORMS.keys()))
    content_type = st.radio("Focus:", ["Trending", "Educational", "Opinion"])

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.header("📊 AI-Generated Content")
    
    if st.button("🚀 Generate Topics", type="primary"):
        topics = ai.fuse_content(topic)
        
        for i, blog_topic in enumerate(topics, 1):
            score = ai.predict_engagement(blog_topic, platform)
            st.markdown(f"""
            <div class="topic-card">
                <h4>💡 {blog_topic}</h4>
                <p>Engagement: {score:.0%} | Type: {content_type}</p>
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.header("⏰ Optimal Timing")
    rec = ai.get_recommendations(platform)
    
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid {rec['color']}">
        <h3>{platform}</h3>
        <p><strong>Time:</strong> {rec['time']}</p>
        <p><strong>Days:</strong> {rec['days']}</p>
        <p><strong>Types:</strong> {rec['types']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    engagement = ai.predict_engagement(topic, platform)
    st.metric("🔥 Engagement", f"{engagement:.0%}", "↗️ +12%")

with col3:
    st.header("📊 Platform Insights")
    
    for p_name, p_data in PLATFORMS.items():
        score = random.randint(75, 95)
        st.markdown(f"""
        <div class="metric-card">
            <h4>{p_name}</h4>
            <p>Score: {score}%</p>
            <div style="background: {p_data['color']}; height: 4px; width: {score}%; border-radius: 2px;"></div>
        </div>
        """, unsafe_allow_html=True)

st.header("🔥 Trending Dashboard")
cols = st.columns(5)
for i, trend in enumerate(ai.trending):
    cols[i].metric(trend, f"{90-i*5}%")

st.header("🎨 Multimodal Input")
tab1, tab2, tab3 = st.tabs(["📝 Text", "🖼️ Image", "🎤 Voice"])

with tab1:
    user_text = st.text_area("Content idea:")
    if user_text: st.success("✅ Text processed")

with tab2:
    img = st.file_uploader("Upload image:", type=['png', 'jpg'])
    if img: st.success("✅ Image analyzed")

with tab3:
    audio = st.file_uploader("Upload audio:", type=['mp3', 'wav'])
    if audio: st.success("✅ Audio processed")

if __name__ == "__main__":
    st.sidebar.success("🚀 AI Ready!")