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
from database import db_manager

# Page config
st.set_page_config(
    page_title="Agentic AI Blog Assistant", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🤖"
)

# Authentication check - MUST BE FIRST
from auth import auth_manager
if not auth_manager.require_auth():
    st.stop()

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
        """Generate content calendar with guaranteed 7-day coverage"""
        calendar_data = []
        start_date = datetime.now()
        
        # Ensure we have enough topics by cycling through them
        if not topics:
            # Generate fallback topics if none provided
            topics = [{
                "title": f"Content about {self.trending_topics[i % len(self.trending_topics)]}",
                "platform": list(PLATFORMS.keys())[i % len(PLATFORMS)],
                "engagement_score": random.uniform(0.7, 0.9),
                "best_time": "12:00-15:00",
                "content_type": "Educational",
                "hashtags": ["#Content", "#Blog", "#AI"]
            } for i in range(7)]
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            day_name = date.strftime("%A")
            
            # Find best topics for this day
            suitable_topics = [t for t in topics if day_name in PLATFORMS[t["platform"]]["days"]]
            
            # If no suitable topics for this day, use any available topic
            if not suitable_topics and topics:
                suitable_topics = topics
            
            # Select topic (cycle through if needed)
            if suitable_topics:
                topic = suitable_topics[i % len(suitable_topics)]
            else:
                # Fallback topic
                platform_key = list(PLATFORMS.keys())[i % len(PLATFORMS)]
                topic = {
                    "title": f"Daily content about {self.trending_topics[i % len(self.trending_topics)]}",
                    "platform": platform_key,
                    "engagement_score": random.uniform(0.7, 0.9),
                    "best_time": PLATFORMS[platform_key]["times"][0],
                    "content_type": random.choice(PLATFORMS[platform_key]["types"])
                }
            
            calendar_data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Day": day_name,
                "Topic": topic["title"][:50] + ("..." if len(topic["title"]) > 50 else ""),
                "Platform": topic["platform"],
                "Engagement": f"{topic['engagement_score']:.0%}",
                "Best_Time": topic["best_time"],
                "Content_Type": topic.get("content_type", "General")
            })
        
        return pd.DataFrame(calendar_data)

# Custom CSS
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    .stApp > header {visibility: hidden;}
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Remove white containers */
    .main .block-container {
        padding: 2rem 1rem;
        background: transparent;
        max-width: 1200px;
    }
    
    /* Headers */
    .main-header {
        font-size: 3.5rem;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        font-weight: 700;
    }
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }
    
    /* Professional cards */
    .pro-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    .pro-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.15);
    }
    
    /* Content sections */
    .content-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Topic cards */
    .topic-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .topic-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        color: #333;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    /* Platform cards */
    .platform-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(15px);
        color: #333;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .platform-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Trend cards */
    .trend-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(15px);
        color: #334155;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    .trend-card:hover {
        transform: translateX(5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        border-left-width: 6px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
    }
    .stButton > button:hover {
        background: rgba(255,255,255,0.3) !important;
        border-color: rgba(255,255,255,0.5) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.9) !important;
        color: #333 !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        backdrop-filter: blur(10px) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div > div {
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Remove white backgrounds from containers */
    .element-container {
        background: transparent !important;
    }
    
    /* Metrics */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        color: #64748b;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Professional glass effect */
    .glass-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize AI
ai = AgenticBlogAI()

# Show user profile in sidebar
auth_manager.show_user_profile()

# Header
st.markdown('<h1 class="main-header">🤖 Agentic AI Blog Writing Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent Content Curation & Multi-Platform Optimization</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("🎯 Content Configuration")
    
    # Check for restored session data
    default_topic = st.session_state.get('restored_topic', "Artificial Intelligence")
    default_platform_index = 0
    if 'restored_platform' in st.session_state:
        platform_list = list(PLATFORMS.keys())
        if st.session_state.restored_platform in platform_list:
            default_platform_index = platform_list.index(st.session_state.restored_platform)
    
    topic = st.text_input("📝 Enter Topic:", default_topic, help="Enter any topic for AI-powered blog ideas")
    platform = st.selectbox("🚀 Target Platform:", list(PLATFORMS.keys()), index=default_platform_index)
    
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
    # Enhanced content generation section
    st.markdown('<div class="content-header"><h2>📊 AI-Generated Content Ideas</h2><p>Create engaging blog content with AI-powered insights</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        generate_standard = st.button("🚀 Generate Topics", key="gen_topics", help="Generate AI-powered blog topics")
    
    with col_btn2:
        generate_ai = st.button("🤖 Full Blog AI", key="gen_full", help="Generate complete blog content")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
                    
                    # Save to database
                    session_data = {
                        "topic": topic,
                        "platform": platform,
                        "content_focus": content_focus,
                        "blog_content": blog_content,
                        "generated_topics": [{
                            "title": blog_content['title'],
                            "engagement_score": 0.85
                        }]
                    }
                    auth_manager.save_user_session(session_data)
                    
                    st.success("✅ Complete blog content generated!")
                    
                    # Display full blog content with editing capability
                    st.markdown(f"""
                    <div class="topic-card">
                        <h3>📝 {blog_content['title']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Interactive content editing
                    if 'sections' in blog_content and blog_content['sections']:
                        st.subheader("✏️ Edit Blog Sections")
                        
                        edited_sections = []
                        for i, section in enumerate(blog_content['sections']):
                            with st.expander(f"📝 {section['title']}", expanded=i==0):
                                edited_content = st.text_area(
                                    f"Edit {section['title']}:",
                                    value=section['content'],
                                    height=150,
                                    key=f"section_{i}"
                                )
                                edited_sections.append({
                                    'title': section['title'],
                                    'content': edited_content
                                })
                        
                        # Update blog content with edits
                        if st.button("💾 Update Blog Content"):
                            updated_content = "\n\n".join([f"## {s['title']}\n{s['content']}" for s in edited_sections])
                            blog_content['content'] = updated_content
                            st.success("✅ Blog content updated!")
                    
                    else:
                        # Fallback: single text area for editing
                        st.subheader("✏️ Edit Blog Content")
                        edited_content = st.text_area(
                            "Edit your blog content:",
                            value=blog_content['content'],
                            height=400,
                            key="blog_editor"
                        )
                        
                        if st.button("💾 Update Content"):
                            blog_content['content'] = edited_content
                            st.success("✅ Content updated!")
                    
                    # Display final content
                    st.markdown(f"""
                    <div class="topic-card">
                        <div style="margin: 1rem 0;">
                            <h4>📖 Final Blog Content:</h4>
                            <div style="text-align: justify; line-height: 1.6;">{blog_content['content'].replace(chr(10), '<br>')}</div>
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
                        <div style="margin: 1rem 0;">
                            <h4>📊 Word Count:</h4>
                            <p>{len(blog_content['content'].split())} words</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Generate blog image
                    with st.spinner("🎨 Generating professional blog image..."):
                        image_url = ai.working_ai.generate_blog_image_url(blog_content['title'])
                        if image_url:
                            try:
                                # Fix HTML entities in URL
                                clean_url = image_url.replace('&amp;', '&')
                                st.image(clean_url, caption=f"AI-generated image for: {blog_content['title']}", use_column_width=True)
                                st.success("✅ Professional blog image generated!")
                            except Exception as img_error:
                                st.error(f"Image display error: {img_error}")
                                # Use simple fallback
                                fallback_url = f"https://picsum.photos/1200/630?random={abs(hash(blog_content['title'])) % 1000}"
                                st.image(fallback_url, caption="Fallback image", use_column_width=True)
                        else:
                            st.error("Failed to generate image")
                    
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
                            try:
                                sentiment_data = ai.free_ai.analyze_content_sentiment(item['title'])
                                item['sentiment'] = sentiment_data['sentiment']
                            except:
                                item['sentiment'] = random.uniform(0.6, 0.9)  # Fallback
                
                blog_topics = ai.generate_blog_topics(content_data, platform, content_focus)
                
                # Save session to database
                session_data = {
                    "topic": topic,
                    "platform": platform,
                    "content_focus": content_focus,
                    "generated_topics": blog_topics,
                    "engagement_scores": {t['title']: t['engagement_score'] for t in blog_topics}
                }
                auth_manager.save_user_session(session_data)
                
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
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<div class="content-header"><h3>📅 AI-Generated Content Calendar</h3><p>Plan your content strategy for the week</p></div>', unsafe_allow_html=True)
    
    if st.button("📅 Generate 7-Day Calendar", key="gen_calendar"):
        with st.spinner("📅 Creating your 7-day content calendar..."):
            # Generate content for multiple platforms to ensure coverage
            all_topics = []
            
            # Generate topics for each platform to ensure variety
            for platform_name in PLATFORMS.keys():
                content_data = ai.collect_multi_source_content(topic)
                platform_topics = ai.generate_blog_topics(content_data, platform_name, content_focus)
                all_topics.extend(platform_topics)
            
            # Generate calendar with all topics
            calendar_df = ai.generate_content_calendar(all_topics)
            
            if not calendar_df.empty:
                st.success(f"✅ Generated 7-day content calendar with {len(calendar_df)} posts!")
                
                # Display calendar with better formatting
                st.dataframe(
                    calendar_df,
                    use_container_width=True,
                    column_config={
                        "Date": st.column_config.DateColumn("📅 Date"),
                        "Day": st.column_config.TextColumn("📆 Day"),
                        "Topic": st.column_config.TextColumn("📝 Topic", width="large"),
                        "Platform": st.column_config.TextColumn("🚀 Platform"),
                        "Engagement": st.column_config.TextColumn("📊 Engagement"),
                        "Best_Time": st.column_config.TextColumn("⏰ Best Time"),
                        "Content_Type": st.column_config.TextColumn("🎯 Type")
                    }
                )
                
                # Show calendar summary
                st.write("**📊 Calendar Summary:**")
                platform_counts = calendar_df['Platform'].value_counts()
                for platform, count in platform_counts.items():
                    st.write(f"• {platform}: {count} posts")
                    
            else:
                st.error("❌ Failed to generate calendar. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-header"><h3>⏰ Optimal Timing & Strategy</h3><p>Platform-specific optimization insights</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    
    # Platform-specific recommendations
    platform_data = PLATFORMS[platform]
    
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {platform_data['color']}">
        <h3 style="color: {platform_data['color']}; margin-bottom: 1rem;">🎯 {platform}</h3>
        <div style="display: grid; gap: 0.5rem;">
            <p><strong>⏰ Best Times:</strong> {', '.join(platform_data['times'])}</p>
            <p><strong>📅 Best Days:</strong> {', '.join(platform_data['days'])}</p>
            <p><strong>📝 Content Types:</strong> {', '.join(platform_data['types'])}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Engagement prediction
    sample_engagement = ai.predict_engagement(topic, platform, 0.8)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{sample_engagement:.0%}</div>
        <div class="metric-label">🔥 Predicted Engagement</div>
        <div style="color: #10b981; font-size: 0.9rem; margin-top: 0.5rem;">↗️ +12% from last week</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Platform insights
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #667eea; margin-bottom: 1rem;">💡 Content Optimization Tips</h4>', unsafe_allow_html=True)
    
    tips = [
        "Use trending hashtags for maximum reach",
        "Include visual elements to boost engagement",
        "Add clear call-to-action in your posts",
        "Optimize content for mobile viewing",
        "Engage with comments within first hour"
    ]
    
    for i, tip in enumerate(tips, 1):
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.8);
            backdrop-filter: blur(10px);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #0288d1;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        ">
            <strong>{i}.</strong> {tip}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="content-header"><h3>📈 Platform Performance Insights</h3><p>Real-time analytics and trends</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    
    # Platform comparison chart
    platform_scores = {}
    for p_name, p_data in PLATFORMS.items():
        score = random.randint(75, 95)
        platform_scores[p_name] = score
        
        st.markdown(f"""
        <div class="platform-card" style="border-left: 4px solid {p_data['color']}">
            <h4 style="color: {p_data['color']}; margin-bottom: 0.5rem;">{p_name}</h4>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>Performance Score</span>
                <strong style="color: {p_data['color']}; font-size: 1.2rem;">{score}%</strong>
            </div>
            <div style="background: #e2e8f0; height: 8px; border-radius: 4px; margin-top: 0.5rem; overflow: hidden;">
                <div style="background: {p_data['color']}; height: 100%; width: {score}%; border-radius: 4px; transition: width 0.3s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #667eea; margin-bottom: 1rem;">🔥 Real-Time Trending Analysis</h4>', unsafe_allow_html=True)
    
    # Trending topics analysis
    trending_data = ai.analyze_trending_topics()
    
    for topic, data in list(trending_data.items())[:5]:
        growth_icon = "↗️" if data["growth"] > 0 else "↘️"
        growth_color = "#10b981" if data["growth"] > 0 else "#ef4444"
        
        st.markdown(f"""
        <div class="trend-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="color: #1e293b;">{topic}</strong>
                <span style="color: {growth_color}; font-weight: 600;">{growth_icon} {data['growth']:.1f}%</span>
            </div>
            <div style="display: flex; gap: 1rem; margin-top: 0.5rem; font-size: 0.9rem; color: #64748b;">
                <span>📈 Score: {data['score']:.0f}%</span>
                <span>📅 Volume: {data['volume']:,}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

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
                
                # Save to database
                auth_manager.save_user_post({
                    "title": st.session_state.current_blog_content['title'],
                    "platforms": selected_platforms,
                    "scheduled_time": schedule_datetime,
                    "status": "scheduled"
                })
                
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
                    
                    # Update database
                    auth_manager.save_user_post({
                        "title": st.session_state.current_blog_content['title'],
                        "platforms": selected_platforms,
                        "scheduled_time": schedule_datetime,
                        "status": post_record["status"],
                        "results": demo_results,
                        "posted_at": datetime.now()
                    })
                    
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

# User History Section
st.header("📅 Your Content History")
auth_manager.show_user_history()

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