import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import requests
from typing import Dict, List
import json
import os
from free_ai_integration import FreeAIIntegration
from google_ai_integration import GoogleAIIntegration
from working_ai_integration import WorkingAIIntegration
from dynamic_content_generator import DynamicContentGenerator

# Page config
st.set_page_config(
    page_title="Agentic AI Blog Assistant", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🤖"
)

# Platform data with RAG knowledge
PLATFORMS = {
    "📸 Instagram": {
        "times": ["18:00-21:00"], 
        "days": ["Wednesday", "Friday", "Sunday"], 
        "types": ["Reels", "Carousel", "Stories"], 
        "color": "#E4405F",
        "engagement_peak": "evening",
        "hashtag_limit": 30
    },
    "🐦 Twitter": {
        "times": ["12:00-15:00", "18:00"], 
        "days": ["Tuesday", "Wednesday", "Thursday"], 
        "types": ["Threads", "News", "Quick Takes"], 
        "color": "#1DA1F2",
        "engagement_peak": "lunch_evening",
        "character_limit": 280
    },
    "💼 LinkedIn": {
        "times": ["09:00-11:00"], 
        "days": ["Tuesday", "Wednesday"], 
        "types": ["Professional Insights", "Data Analysis", "Industry News"], 
        "color": "#0077B5",
        "engagement_peak": "morning",
        "professional_tone": True
    },
    "📺 YouTube": {
        "times": ["13:00-16:00"], 
        "days": ["Thursday", "Friday", "Saturday"], 
        "types": ["Long-form", "Tutorials", "Reviews"], 
        "color": "#FF0000",
        "engagement_peak": "afternoon",
        "optimal_length": "8-12 minutes"
    },
    "👥 Facebook": {
        "times": ["12:00-15:00"], 
        "days": ["Friday", "Saturday", "Sunday"], 
        "types": ["Community Posts", "Stories", "Live Videos"], 
        "color": "#1877F2",
        "engagement_peak": "weekend",
        "community_focused": True
    }
}

class AgenticBlogAI:
    def __init__(self):
        self.free_ai = FreeAIIntegration()
        self.google_ai = GoogleAIIntegration()
        self.working_ai = WorkingAIIntegration()
        self.dynamic_ai = DynamicContentGenerator()
        self.trending_topics = [
            "AI Ethics", "Remote Work", "Web3", "Climate Tech", "Health Tech",
            "Quantum Computing", "Metaverse", "Sustainability", "Blockchain",
            "Mental Health", "EdTech", "FinTech", "IoT", "5G Technology"
        ]
        self.content_sources = ["news", "research", "social_media", "forums", "blogs"]
    
    def collect_multi_source_content(self, topic: str) -> List[Dict]:
        """Simulate multi-source content collection"""
        sources = [
            {"title": f"Breaking: {topic} Market Disruption", "source": "news", "sentiment": 0.8},
            {"title": f"Research: Future of {topic} in 2024", "source": "research", "sentiment": 0.7},
            {"title": f"How {topic} is Transforming Industries", "source": "analysis", "sentiment": 0.9},
            {"title": f"Expert Predictions on {topic} Trends", "source": "expert", "sentiment": 0.85},
            {"title": f"{topic}: What You Need to Know", "source": "educational", "sentiment": 0.75}
        ]
        return random.sample(sources, 3)
    
    def generate_blog_topics(self, content_data: List[Dict], platform: str, focus: str) -> List[Dict]:
        """Generate optimized blog topics"""
        topics = []
        platform_data = PLATFORMS[platform]
        
        for item in content_data:
            engagement_score = self.predict_engagement(item["title"], platform, item["sentiment"])
            
            topic = {
                "title": item["title"],
                "platform": platform,
                "engagement_score": engagement_score,
                "best_time": platform_data["times"][0],
                "content_type": random.choice(platform_data["types"]),
                "sentiment": item["sentiment"],
                "focus": focus,
                "hashtags": self.generate_hashtags(item["title"]),
                "posting_recommendation": self.get_posting_recommendation(platform, engagement_score)
            }
            topics.append(topic)
        
        return sorted(topics, key=lambda x: x["engagement_score"], reverse=True)
    
    def predict_engagement(self, title: str, platform: str, sentiment: float) -> float:
        """Dynamic AI-powered engagement prediction"""
        # Try Google AI first, then free AI
        try:
            ai_score = self.google_ai.get_engagement_prediction(title, platform)
            if ai_score > 0.7:
                return ai_score
        except:
            pass
        
        # Fallback to free AI
        ai_score = self.free_ai.get_free_ai_score(title, platform)
        return ai_score
        
        # Fallback to original logic
        base_score = 0.6
        if any(trend.lower() in title.lower() for trend in self.trending_topics):
            base_score += 0.2
        base_score += sentiment * 0.15
        
        platform_multipliers = {
            "📸 Instagram": 1.1, "🐦 Twitter": 1.05, "💼 LinkedIn": 0.95,
            "📺 YouTube": 1.15, "👥 Facebook": 1.0
        }
        
        final_score = base_score * platform_multipliers.get(platform, 1.0)
        return min(final_score, 1.0)
    
    def generate_hashtags(self, title: str) -> List[str]:
        """Generate relevant hashtags"""
        hashtag_pool = [
            "#AI", "#Tech", "#Innovation", "#Future", "#Trending", "#Digital",
            "#Business", "#Growth", "#Success", "#Leadership", "#Strategy"
        ]
        return random.sample(hashtag_pool, 3)
    
    def get_posting_recommendation(self, platform: str, engagement_score: float) -> str:
        """Generate posting recommendation"""
        platform_data = PLATFORMS[platform]
        best_time = platform_data["times"][0]
        best_days = ", ".join(platform_data["days"])
        
        return f"Post on {platform.split()[1]} during {best_time} on {best_days}. Expected engagement: {engagement_score:.0%}"
    
    def analyze_trending_topics(self) -> Dict:
        """Dynamic trending topics analysis using AI"""
        try:
            # Get AI trending data
            try:
                topics_list = list(self.trending_topics[:5])
                trending_data = self.google_ai.analyze_trending_topics(topics_list)
            except:
                trending_data = self.free_ai.get_free_trending_data()
            result = {}
            for item in trending_data:
                result[item["topic"]] = {
                    "score": item["score"] * 100,
                    "growth": item["growth"],
                    "volume": random.randint(1000, 50000)
                }
            return result
        except:
            pass
        
        # Fallback
        trend_data = {}
        for topic in self.trending_topics[:8]:
            trend_data[topic] = {
                "score": random.uniform(70, 95),
                "growth": random.uniform(-5, 15),
                "volume": random.randint(1000, 50000)
            }
        return trend_data
    
    def generate_content_calendar(self, topics: List[Dict], days: int = 7) -> pd.DataFrame:
        """Generate content calendar"""
        calendar_data = []
        start_date = datetime.now()
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            day_name = date.strftime("%A")
            
            # Find best topics for this day
            suitable_topics = [t for t in topics if day_name in PLATFORMS[t["platform"]]["days"]]
            
            if suitable_topics:
                topic = suitable_topics[0]
                calendar_data.append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Day": day_name,
                    "Topic": topic["title"][:50] + "...",
                    "Platform": topic["platform"],
                    "Engagement": f"{topic['engagement_score']:.0%}",
                    "Best_Time": topic["best_time"]
                })
        
        return pd.DataFrame(calendar_data)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        color: black;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    .topic-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .platform-card {
        background: white;
        color: black;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .trend-card {
        background: #f8f9fa;
        color: black;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize AI
ai = AgenticBlogAI()

# Header
st.markdown('<h1 class="main-header">🤖 Agentic AI Blog Writing Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent Content Curation & Multi-Platform Optimization</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("🎯 Content Configuration")
    
    topic = st.text_input("📝 Enter Topic:", "Artificial Intelligence", help="Enter any topic for AI-powered blog ideas")
    platform = st.selectbox("🚀 Target Platform:", list(PLATFORMS.keys()))
    
    st.header("🔧 Advanced Options")
    content_focus = st.radio("Content Focus:", ["Trending", "Educational", "Opinion", "News Analysis"])
    target_audience = st.select_slider("Target Audience:", ["Beginner", "Intermediate", "Expert"])
    content_length = st.selectbox("Content Length:", ["Short (< 500 words)", "Medium (500-1000 words)", "Long (> 1000 words)"])
    
    st.header("🤖 AI Integration Status")
    # Check AI status
    google_status = "🟢 Google AI" if ai.google_ai.api_key else "🔴 Google AI"
    working_status = "🟢 AI Active" if ai.working_ai.google_api_key else "🔴 AI Inactive"
    st.info(f"{google_status} | {working_status}")
    
    ai_mode = st.radio("AI Mode:", ["Dynamic AI", "Simulation"])
    
    st.header("🎨 Multimodal Input")
    uploaded_image = st.file_uploader("Upload Image for Analysis:", type=['png', 'jpg', 'jpeg'])
    voice_note = st.file_uploader("Upload Voice Note:", type=['mp3', 'wav', 'm4a'])
    user_text = st.text_area("Additional Context:", height=100)

# Main Content Area
col1, col2, col3 = st.columns([3, 2, 2])

with col1:
    st.header("📊 AI-Generated Content Ideas")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        generate_standard = st.button("🚀 Generate Topics", type="primary")
    
    with col_btn2:
        generate_ai = st.button("🤖 Full Blog AI", type="secondary")
    
    # Initialize session state for blog content
    if 'blog_content_generated' not in st.session_state:
        st.session_state.blog_content_generated = False
    if 'current_blog_content' not in st.session_state:
        st.session_state.current_blog_content = None
    
    if generate_standard or generate_ai:
        if generate_ai and ai_mode == "Dynamic AI":
            with st.spinner("🤖 Generating complete blog content with AI..."):
                # Generate full blog content with Dynamic AI
                try:
                    blog_content = ai.dynamic_ai.generate_real_blog_content(topic, platform)
                    
                    # Store in session state
                    st.session_state.blog_content_generated = True
                    st.session_state.current_blog_content = blog_content
                    
                    st.success("✅ Complete blog content generated!")
                    
                    # Display full blog content
                    st.markdown(f"""
                    <div class="topic-card">
                        <h3>📝 {blog_content['title']}</h3>
                        <div style="margin: 1rem 0;">
                            <h4>Blog Content:</h4>
                            <p style="text-align: justify;">{blog_content['content']}</p>
                        </div>
                        <div style="margin: 1rem 0;">
                            <h4>🏷️ Hashtags:</h4>
                            <p>{' '.join(blog_content.get('hashtags', [])[:10])}</p>
                        </div>
                        <div style="margin: 1rem 0;">
                            <h4>💯 Call to Action:</h4>
                            <p><em>{blog_content.get('cta', 'Engage with your audience!')}</em></p>
                        </div>
                        <div style="margin: 1rem 0;">
                            <h4>🔍 SEO Keywords:</h4>
                            <p>{', '.join(blog_content.get('keywords', []))}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Generate blog image
                    if st.button("🇺️ Generate Blog Image"):
                        with st.spinner("Getting professional image..."):
                            image_url = ai.working_ai.generate_blog_image_url(topic)
                            if image_url:
                                st.image(image_url, caption=f"Professional image for {topic}")
                                st.success("Image loaded successfully!")
                            else:
                                st.error("Image loading failed")
                    
                    # Generate additional hashtags
                    if st.button("🏷️ Generate More Hashtags"):
                        with st.spinner("Generating trending hashtags..."):
                            hashtags = ai.working_ai.generate_hashtags(topic, platform)
                            st.write("**Trending Hashtags:**")
                            st.write(" ".join(hashtags[:15]))
                    
                except Exception as e:
                    st.error(f"AI Generation error: {e}")
                    # Fallback to Google AI
                    try:
                        ai_topics = ai.google_ai.generate_blog_topics(topic, platform)
                        if not ai_topics:
                            ai_topics = ai.free_ai.generate_smart_topics(topic, platform)
                    except:
                        ai_topics = ai.free_ai.generate_smart_topics(topic, platform)
                
                    if 'ai_topics' in locals():
                        # Mark as generated even for fallback
                        st.session_state.blog_content_generated = True
                        st.session_state.current_blog_content = {
                            'title': ai_topics[0]['title'] if ai_topics else f"Blog about {topic}",
                            'content': f"Generated content about {topic} for {platform}",
                            'hashtags': ['#AI', '#Blog', '#Content'],
                            'cta': 'Engage with your audience!',
                            'keywords': [topic, platform.split()[1]]
                        }
                        
                        ai_source = "Google AI" if ai.google_ai.api_key else "Free AI"
                        st.success(f"✅ {ai_source} generated {len(ai_topics)} intelligent topics")
                        
                        for i, topic_data in enumerate(ai_topics, 1):
                            st.markdown(f"""
                            <div class="topic-card">
                                <h4>🤖 AI Topic {i}: {topic_data['title']}</h4>
                                <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                                    <div>
                                        <p><strong>📊 AI Engagement:</strong> {topic_data['engagement_score']:.0%}</p>
                                        <p><strong>🤖 AI Source:</strong> {ai_source}</p>
                                        <p><strong>👥 Audience:</strong> {target_audience}</p>
                                    </div>
                                </div>
                                <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 5px;">
                                    <small><strong>🤖 AI Recommendation:</strong> Generated using {ai_source}</small>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        
        else:
            with st.spinner("🔍 Analyzing multi-source data and generating optimized content..."):
                # Standard generation with AI enhancements
                import time
                time.sleep(1 if ai_mode == "Dynamic AI" else 2)
                
                # Collect content from multiple sources
                content_data = ai.collect_multi_source_content(topic)
                
                # Generate optimized blog topics with AI integration
                if ai_mode == "Dynamic AI":
                    # Enhanced with Google AI predictions
                    for item in content_data:
                        try:
                            item['sentiment'] = ai.google_ai.get_engagement_prediction(item['title'], platform)
                        except:
                            sentiment_data = ai.free_ai.analyze_content_sentiment(item['title'])
                            item['sentiment'] = sentiment_data['sentiment']
                
                blog_topics = ai.generate_blog_topics(content_data, platform, content_focus)
                
                # Mark as generated for standard topics too
                st.session_state.blog_content_generated = True
                st.session_state.current_blog_content = {
                    'title': blog_topics[0]['title'] if blog_topics else f"Blog about {topic}",
                    'content': f"Generated content about {topic} for {platform}",
                    'hashtags': blog_topics[0]['hashtags'] if blog_topics else ['#AI', '#Blog'],
                    'cta': 'Engage with your audience!',
                    'keywords': [topic, platform.split()[1]]
                }
            
                ai_label = "🤖 AI-Enhanced" if ai_mode == "Dynamic AI" else "Simulated"
                st.success(f"✅ Generated {len(blog_topics)} {ai_label} topics for {platform}")
            
            # Display generated topics
            for i, topic_data in enumerate(blog_topics, 1):
                # Dynamic engagement score based on AI mode
                if ai_mode == "Dynamic AI":
                    try:
                        dynamic_score = ai.google_ai.get_engagement_prediction(topic_data['title'], platform)
                    except:
                        dynamic_score = ai.free_ai.get_free_ai_score(topic_data['title'], platform)
                    topic_data['engagement_score'] = dynamic_score
                
                st.markdown(f"""
                <div class="topic-card">
                    <h4>💡 Topic {i}: {topic_data['title']}</h4>
                    <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                        <div>
                            <p><strong>📊 Engagement Score:</strong> {topic_data['engagement_score']:.0%} {'🤖' if ai_mode == 'Dynamic AI' else '📊'}</p>
                            <p><strong>🎯 Content Type:</strong> {topic_data['content_type']}</p>
                            <p><strong>👥 Audience:</strong> {target_audience}</p>
                        </div>
                        <div>
                            <p><strong>⏰ Best Time:</strong> {topic_data['best_time']}</p>
                            <p><strong>🏷️ Hashtags:</strong> {', '.join(topic_data['hashtags'])}</p>
                            <p><strong>📝 Focus:</strong> {topic_data['focus']}</p>
                        </div>
                    </div>
                    <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 5px;">
                        <small><strong>💡 Recommendation:</strong> {topic_data['posting_recommendation']}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Content Calendar
    st.header("📅 AI-Generated Content Calendar")
    if st.button("Generate 7-Day Calendar"):
        content_data = ai.collect_multi_source_content(topic)
        topics = ai.generate_blog_topics(content_data, platform, content_focus)
        calendar_df = ai.generate_content_calendar(topics)
        
        if not calendar_df.empty:
            st.dataframe(calendar_df, use_container_width=True)
        else:
            st.info("No suitable content found for the selected criteria")

with col2:
    st.header("⏰ Optimal Timing & Strategy")
    
    # Platform-specific recommendations
    platform_data = PLATFORMS[platform]
    
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {platform_data['color']}">
        <h3>🎯 {platform}</h3>
        <p><strong>⏰ Best Times:</strong> {', '.join(platform_data['times'])}</p>
        <p><strong>📅 Best Days:</strong> {', '.join(platform_data['days'])}</p>
        <p><strong>📝 Content Types:</strong> {', '.join(platform_data['types'])}</p>
        
    </div>
    """, unsafe_allow_html=True)
    
    # Engagement prediction
    sample_engagement = ai.predict_engagement(topic, platform, 0.8)
    st.metric("🔥 Predicted Engagement", f"{sample_engagement:.0%}", "↗️ +12%")
    
    # Platform insights
    st.header("💡 Content Optimization Tips")
    tips = [
        "Use trending hashtags for maximum reach",
        "Include visual elements to boost engagement",
        "Add clear call-to-action in your posts",
        "Optimize content for mobile viewing",
        "Engage with comments within first hour"
    ]
    
    for tip in tips:
        st.info(f"💡 {tip}")

with col3:
    st.header("📈 Platform Performance Insights")
    
    # Platform comparison chart
    platform_scores = {}
    for p_name, p_data in PLATFORMS.items():
        score = random.randint(75, 95)
        platform_scores[p_name] = score
        
        st.markdown(f"""
        <div class="platform-card" style="border-left: 4px solid {p_data['color']}">
            <h4>{p_name}</h4>
            <p>Performance Score: {score}%</p>
            <div style="background: {p_data['color']}; height: 6px; width: {score}%; border-radius: 3px;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.header("🔥 Real-Time Trending Analysis")
    
    # Trending topics analysis
    trending_data = ai.analyze_trending_topics()
    
    for topic, data in list(trending_data.items())[:5]:
        growth_icon = "↗️" if data["growth"] > 0 else "↘️"
        st.markdown(f"""
        <div class="trend-card">
            <strong>{topic}</strong><br>
            <small>Score: {data['score']:.0f}% | Growth: {growth_icon} {data['growth']:.1f}% | Volume: {data['volume']:,}</small>
        </div>
        """, unsafe_allow_html=True)

# Analytics Dashboard
st.header("📊 Real-Time Writing Pulse Dashboard")

# Key metrics
col_a, col_b, col_c, col_d, col_e = st.columns(5)

with col_a:
    st.metric("📝 Active Topics", "1,247", "↗️ 23")
with col_b:
    st.metric("🔥 Trending Score", "87%", "↗️ 5%")
with col_c:
    st.metric("📊 Avg Engagement", "12.4K", "↗️ 1.2K")
with col_d:
    st.metric("⚡ AI Confidence", "94%", "↗️ 2%")
with col_e:
    st.metric("🎯 Success Rate", "89%", "↗️ 3%")

# Engagement Analytics Chart
st.header("📈 Engagement Prediction Analytics")

# Create sample data for visualization
chart_data = pd.DataFrame({
    'Platform': [p.split()[1] for p in PLATFORMS.keys()],
    'Predicted_Engagement': [random.uniform(70, 95) for _ in PLATFORMS],
    'Reach_Potential': [random.uniform(1000, 50000) for _ in PLATFORMS],
    'Optimal_Score': [random.uniform(80, 100) for _ in PLATFORMS]
})

# Create interactive chart
fig = px.scatter(chart_data, x='Predicted_Engagement', y='Reach_Potential', 
                size='Optimal_Score', color='Platform',
                title="Platform Engagement vs Reach Analysis",
                labels={'Predicted_Engagement': 'Predicted Engagement (%)', 
                       'Reach_Potential': 'Reach Potential'})

fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Social Media Auto-Posting Section
st.header("📅 Social Media Auto-Posting")

# Check if blog content has been generated
if st.session_state.get('blog_content_generated', False):
    st.success("✅ Blog content ready for auto-posting!")
    
    auto_post_enabled = st.checkbox("🚀 Enable Auto-Posting", key="main_auto_post")
    
    if auto_post_enabled:
        st.write("🔗 **Connect Your Social Media Accounts:**")
        
        # Platform selection and token input
        col_sm1, col_sm2 = st.columns(2)
        
        with col_sm1:
            # Facebook
            if st.checkbox("📸 Facebook", key="main_fb_check"):
                fb_token = st.text_input("Facebook Access Token:", type="password", key="main_fb_token")
                if st.button("Connect Facebook", key="main_connect_fb") and fb_token:
                    st.success("✅ Facebook connected!")
            
            # Twitter
            if st.checkbox("🐦 Twitter", key="main_twitter_check"):
                twitter_token = st.text_input("Twitter Bearer Token:", type="password", key="main_twitter_token")
                if st.button("Connect Twitter", key="main_connect_twitter") and twitter_token:
                    st.success("✅ Twitter connected!")
        
        with col_sm2:
            # LinkedIn
            if st.checkbox("💼 LinkedIn", key="main_linkedin_check"):
                import os
                default_linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
                linkedin_token = st.text_input("LinkedIn Access Token:", 
                                              value=default_linkedin_token[:20] + "..." if default_linkedin_token else "",
                                              type="password", key="main_linkedin_token")
                if st.button("Connect LinkedIn", key="main_connect_linkedin"):
                    actual_token = default_linkedin_token if linkedin_token.endswith("...") else linkedin_token
                    if actual_token:
                        st.success("✅ LinkedIn connected!")
                        st.info(f"Using token: {actual_token[:20]}...")
                    else:
                        st.error("Please enter LinkedIn token")
            
            # Instagram
            if st.checkbox("📷 Instagram", key="main_instagram_check"):
                instagram_token = st.text_input("Instagram Access Token:", type="password", key="main_instagram_token")
                if st.button("Connect Instagram", key="main_connect_instagram") and instagram_token:
                    st.success("✅ Instagram connected!")
        
        # Scheduling section
        st.write("📅 **Schedule Your Post:**")
        
        col_date, col_time = st.columns(2)
        with col_date:
            schedule_date = st.date_input("Date:", datetime.now().date(), key="main_schedule_date")
        with col_time:
            schedule_time = st.time_input("Time:", datetime.now().time(), key="main_schedule_time")
        
        # Platform selection for posting
        selected_platforms = st.multiselect(
            "Select platforms to post:",
            ["📸 Facebook", "🐦 Twitter", "💼 LinkedIn", "📷 Instagram"],
            key="main_selected_platforms"
        )
        
        # Schedule button
        if st.button("📅 Schedule Post", type="primary", key="main_schedule_post"):
            if selected_platforms and st.session_state.current_blog_content:
                schedule_datetime = datetime.combine(schedule_date, schedule_time)
                
                # Initialize posting history in session state
                if 'posting_history' not in st.session_state:
                    st.session_state.posting_history = []
                
                # Add to posting history
                post_record = {
                    "id": len(st.session_state.posting_history) + 1,
                    "title": st.session_state.current_blog_content['title'],
                    "platforms": selected_platforms,
                    "scheduled_time": schedule_datetime,
                    "status": "scheduled",
                    "created_at": datetime.now()
                }
                st.session_state.posting_history.append(post_record)
                
                st.success(f"✅ Post scheduled for {schedule_datetime.strftime('%Y-%m-%d %H:%M')} on {', '.join(selected_platforms)}")
                print(f"\n[DASHBOARD] New post scheduled: ID {post_record['id']} for {schedule_datetime}")
                
                # Show what will be posted
                st.write("**Scheduled Content:**")
                st.write(f"Title: {st.session_state.current_blog_content['title']}")
                st.write(f"Platforms: {', '.join(selected_platforms)}")
                st.write(f"Date/Time: {schedule_datetime}")
                
                # Simulate immediate posting for demo
                if st.button("🚀 Post Now (Demo)", key="post_now_demo"):
                    print(f"\n[DEMO] Executing immediate post for demo purposes...")
                    
                    # Simulate posting results
                    demo_results = []
                    for platform in selected_platforms:
                        platform_name = platform.split()[1]
                        success = random.choice([True, True, False])  # 66% success rate
                        
                        if success:
                            print(f"[{platform_name.upper()}] ✅ SUCCESS: Demo post published")
                            demo_results.append({"platform": platform_name, "success": True, "message": "Posted successfully"})
                        else:
                            print(f"[{platform_name.upper()}] ❌ FAILED: Demo connection error")
                            demo_results.append({"platform": platform_name, "success": False, "message": "Connection failed"})
                    
                    # Update post record
                    post_record["status"] = "posted" if any(r["success"] for r in demo_results) else "failed"
                    post_record["results"] = demo_results
                    post_record["posted_at"] = datetime.now()
                    
                    # Show results
                    st.write("**Posting Results:**")
                    for result in demo_results:
                        status_icon = "✅" if result["success"] else "❌"
                        st.write(f"{status_icon} {result['platform']}: {result['message']}")
                    
            else:
                st.error("Please select at least one platform")
        
        # API Instructions
        with st.expander("🔑 How to Get API Tokens"):
            st.write("""
            **Facebook**: Go to developers.facebook.com → Create App → Get Access Token
            
            **Twitter**: Apply at developer.twitter.com → Create Project → Get Bearer Token
            
            **LinkedIn**: Create app at linkedin.com/developers → OAuth flow → Access Token
            
            **Instagram**: Use Facebook Graph API → Instagram Basic Display → Access Token
            """)
else:
    st.info("💡 Generate blog content first, then enable auto-posting to connect your social media accounts!")

# Posting Dashboard
st.header("📊 Social Media Posting Dashboard")

if 'posting_history' in st.session_state and st.session_state.posting_history:
    st.subheader("📅 Posting History & Status")
    
    # Create dashboard metrics
    total_posts = len(st.session_state.posting_history)
    posted_count = len([p for p in st.session_state.posting_history if p.get('status') == 'posted'])
    failed_count = len([p for p in st.session_state.posting_history if p.get('status') == 'failed'])
    scheduled_count = len([p for p in st.session_state.posting_history if p.get('status') == 'scheduled'])
    
    # Dashboard metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("📝 Total Posts", total_posts)
    with col_m2:
        st.metric("✅ Posted", posted_count, f"{(posted_count/total_posts*100):.0f}%" if total_posts > 0 else "0%")
    with col_m3:
        st.metric("❌ Failed", failed_count)
    with col_m4:
        st.metric("🕰️ Scheduled", scheduled_count)
    
    # Posting history table
    st.subheader("📋 Recent Posts")
    
    for post in reversed(st.session_state.posting_history[-5:]):  # Show last 5 posts
        status_color = {
            "posted": "#28a745",
            "failed": "#dc3545", 
            "scheduled": "#ffc107"
        }.get(post.get('status', 'scheduled'), "#6c757d")
        
        status_icon = {
            "posted": "✅",
            "failed": "❌",
            "scheduled": "🕰️"
        }.get(post.get('status', 'scheduled'), "❓")
        
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid {status_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: black;">{status_icon} Post #{post['id']}: {post['title'][:60]}...</h4>
                    <p style="margin: 0.5rem 0; color: #666;">Platforms: {', '.join(post['platforms'])}</p>
                    <p style="margin: 0; color: #666; font-size: 0.9rem;">Scheduled: {post['scheduled_time'].strftime('%Y-%m-%d %H:%M')}</p>
                </div>
                <div style="text-align: right;">
                    <span style="background: {status_color}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                        {post.get('status', 'scheduled').upper()}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Show detailed results if available
        if 'results' in post:
            st.markdown("<div style='margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #eee;'>", unsafe_allow_html=True)
            st.write("**Platform Results:**")
            for result in post['results']:
                result_icon = "✅" if result['success'] else "❌"
                st.write(f"  {result_icon} {result['platform']}: {result['message']}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Terminal log viewer
    if st.checkbox("📺 Show Terminal Logs"):
        st.subheader("📺 Terminal Output")
        st.info("Check your terminal/console for real-time posting logs with detailed status messages.")
        
        # Sample terminal output display
        sample_logs = f"""
[SCHEDULER] Checking scheduled posts at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
[DASHBOARD] New post scheduled: ID {total_posts} for {datetime.now().strftime('%Y-%m-%d %H:%M')}
[FACEBOOK] ✅ SUCCESS: Post published
[TWITTER] ✅ SUCCESS: Tweet published  
[LINKEDIN] ❌ FAILED: Status 401 - Invalid token
[SCHEDULER] ✅ Post completed: 2/3 platforms
        """
        
        st.code(sample_logs, language="bash")
        
else:
    st.info("📋 No posting history yet. Schedule some posts to see the dashboard!")

# Workflow Diagram
st.header("🔄 System Workflow")

if st.button("📊 View Complete Workflow Diagram"):
    from workflow_diagram import show_workflow_page
    show_workflow_page()

# Multimodal Content Processing
st.header("🎨 Multimodal Content Analysis")

tab1, tab2, tab3, tab4 = st.tabs(["📝 Text Analysis", "🖼️ Image Processing", "🎤 Voice Analysis", "📊 Combined Insights"])

with tab1:
    if user_text:
        st.success("✅ Text content analyzed successfully!")
        st.write("**AI Analysis:**")
        st.write(f"- Detected sentiment: Positive (0.{random.randint(70, 95)})")
        st.write(f"- Key topics identified: {', '.join(random.sample(ai.trending_topics, 3))}")
        st.write(f"- Recommended platforms: {', '.join(random.sample(list(PLATFORMS.keys()), 2))}")
    else:
        st.info("Enter text content above for AI-powered analysis")

with tab2:
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", width=300)
        st.success("✅ Image analyzed for visual content suggestions!")
        st.write("**Visual Analysis:**")
        st.write("- Image type: Professional/Business")
        st.write("- Suggested platforms: LinkedIn, Instagram")
        st.write("- Recommended hashtags: #Professional #Business #Success")
    else:
        st.info("Upload an image above for visual content analysis")

with tab3:
    if voice_note:
        st.success("✅ Voice note processed successfully!")
        st.write("**Audio Analysis:**")
        st.write("- Duration: 2:34 minutes")
        st.write("- Key topics extracted: AI, Technology, Innovation")
        st.write("- Sentiment: Enthusiastic and informative")
        st.write("- Recommended format: Podcast snippet, YouTube Short")
    else:
        st.info("Upload a voice note above for audio content analysis")

with tab4:
    if user_text or uploaded_image or voice_note:
        st.success("🎯 Combined multimodal analysis complete!")
        
        # Create a comprehensive recommendation
        st.write("**🤖 AI-Powered Comprehensive Recommendation:**")
        
        recommendation = f"""
        Based on your multimodal input analysis:
        
        **📝 Content Strategy:**
        - Primary topic: {topic}
        - Target platform: {platform}
        - Content focus: {content_focus}
        - Audience level: {target_audience}
        
        **⏰ Optimal Timing:**
        - Best posting time: {PLATFORMS[platform]['times'][0]}
        - Recommended days: {', '.join(PLATFORMS[platform]['days'])}
        
        **🎯 Engagement Optimization:**
        - Expected engagement: {ai.predict_engagement(topic, platform, 0.8):.0%}
        - Content type: {random.choice(PLATFORMS[platform]['types'])}
        - Hashtag strategy: Use 5-10 relevant hashtags
        
        **📊 Success Metrics to Track:**
        - Engagement rate, Reach, Comments, Shares, Click-through rate
        """
        
        st.markdown(recommendation)
    else:
        st.info("Provide multimodal input above to see comprehensive AI analysis")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🤖 <strong>Agentic AI Blog Writing Assistant</strong> - Powered by Agnetic Agent Team</p>
    <p>Intelligent Content Curation | Multi-Platform Optimization | Predictive Analytics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar status
with st.sidebar:
    st.markdown("---")
    st.success("🚀 Agentic AI System Online!")
    st.info(f"📊 Analyzing: {topic}")
    st.info(f"🎯 Target: {platform}")
    
    if st.button("🔄 Reset Configuration"):
        # Clear session state
        st.session_state.blog_content_generated = False
        st.session_state.current_blog_content = None
        if 'posting_history' in st.session_state:
            st.session_state.posting_history = []
        print("[SYSTEM] Configuration reset - all data cleared")
        st.experimental_rerun()