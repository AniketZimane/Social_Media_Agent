import streamlit as st
from database import db_manager
from typing import Dict, Optional
import traceback

class AuthManager:
    def __init__(self):
        self.db = db_manager
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'session_token' not in st.session_state:
            st.session_state.session_token = None
        if 'skip_login' not in st.session_state:
            st.session_state.skip_login = False
    
    def show_optional_login_page(self):
        """Display improved optional login page with skip option"""
        # Enhanced CSS styles
        st.markdown("""
        <style>
            .auth-container {
                max-width: 500px;
                margin: 2rem auto;
                padding: 2rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                color: white;
            }
            .auth-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            .auth-title {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .auth-subtitle {
                font-size: 1.1rem;
                opacity: 0.9;
                margin-bottom: 2rem;
            }
            .skip-section {
                text-align: center;
                margin-bottom: 2rem;
                padding: 1.5rem;
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            .stButton > button {
                width: 100%;
                background: rgba(255,255,255,0.2) !important;
                color: white !important;
                border: 2px solid rgba(255,255,255,0.3) !important;
                border-radius: 12px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                transition: all 0.3s ease !important;
                backdrop-filter: blur(10px) !important;
            }
            .stButton > button:hover {
                background: rgba(255,255,255,0.3) !important;
                border-color: rgba(255,255,255,0.5) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Main container
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        <div class="auth-header">
            <div class="auth-title">🤖 Agentic AI</div>
            <div class="auth-subtitle">Intelligent Blog Writing Assistant</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Skip option
        st.markdown('<div class="skip-section">', unsafe_allow_html=True)
        st.markdown("**🎆 Quick Start Option**")
        st.markdown("Try the app instantly without creating an account")
        
        if st.button("⏭️ Continue as Guest", key="skip_login", help="Full access, no data saved"):
            st.session_state.skip_login = True
            st.session_state.authenticated = False
            st.success("✅ Welcome! Using guest mode - your data won't be saved")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider
        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 2rem 0;'>", unsafe_allow_html=True)
        
        # Login/Register tabs
        st.markdown("**🔐 Save Your Progress**")
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            self.show_enhanced_login_form()
        
        with tab2:
            self.show_enhanced_register_form()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def show_enhanced_login_form(self):
        """Enhanced login form with better styling"""
        st.markdown("**Enter your credentials to access saved sessions**")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            remember_me = st.checkbox("🔄 Keep me logged in for 7 days")
            
            submitted = st.form_submit_button("🚀 Sign In", type="primary")
            
            if submitted:
                if username and password:
                    with st.spinner("🔐 Signing you in..."):
                        try:
                            # Direct database connection - no API calls
                            result = self.db.login_user(username, password)
                            
                            if result["success"]:
                                st.session_state.authenticated = True
                                st.session_state.user_id = result["user_id"]
                                st.session_state.username = result["username"]
                                st.session_state.session_token = result["session_token"]
                                st.session_state.skip_login = False
                                
                                st.success(f"✅ Welcome back, {username}! 🎉")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"❌ {result['message']}")
                                
                        except Exception as e:
                            st.error(f"❌ Login failed: {str(e)}")
                            st.info("🛠️ Database connection issue - check MongoDB status")
                            print(f"Login error details: {e}")
                            traceback.print_exc()
                else:
                    st.error("❌ Please fill in all fields")
    
    def show_enhanced_register_form(self):
        """Enhanced registration form with better styling"""
        st.markdown("**Create your account to save and sync your blog sessions**")
        
        with st.form("register_form"):
            username = st.text_input("👤 Choose Username", placeholder="Pick a unique username")
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Repeat your password")
            
            agree_terms = st.checkbox("✅ I agree to the Terms of Service and Privacy Policy")
            
            submitted = st.form_submit_button("🎆 Create Account", type="primary")
            
            if submitted:
                if not all([username, email, password, confirm_password]):
                    st.error("❌ Please fill in all fields")
                elif password != confirm_password:
                    st.error("❌ Passwords don't match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif not agree_terms:
                    st.error("❌ Please agree to the Terms of Service")
                else:
                    with st.spinner("📝 Creating your account..."):
                        try:
                            # Direct database connection - no API calls
                            result = self.db.register_user(username, email, password)
                            
                            if result["success"]:
                                st.success("✅ Account created successfully! 🎉")
                                st.success("🔄 Please switch to the Login tab to sign in")
                                st.balloons()
                            else:
                                st.error(f"❌ {result['message']}")
                                
                        except Exception as e:
                            st.error(f"❌ Registration failed: {str(e)}")
                            st.info("🛠️ Database connection issue - check MongoDB status")
                            print(f"Registration error details: {e}")
                            traceback.print_exc()
    
    def show_user_profile(self):
        """Display enhanced user profile in sidebar"""
        with st.sidebar:
            st.markdown("---")
            
            if st.session_state.authenticated:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 1rem;
                    border-radius: 15px;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <h3 style="margin: 0; font-size: 1.2rem;">👤 {st.session_state.username}</h3>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">Premium User</p>
                </div>
                """, unsafe_allow_html=True)
                
                analytics = self.db.get_user_analytics(st.session_state.user_id)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📊 Sessions", analytics["total_sessions"])
                    st.metric("✅ Success", f"{analytics['success_rate']:.1f}%")
                with col2:
                    st.metric("📝 Posts", analytics["total_posts"])
                    st.metric("🔥 Active", "7 days")
                
                if st.button("🚪 Logout", type="secondary"):
                    self.logout()
            
            elif st.session_state.get('skip_login', False):
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
                    color: white;
                    padding: 1rem;
                    border-radius: 15px;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <h3 style="margin: 0; font-size: 1.2rem;">👥 Guest Mode</h3>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">Data not saved</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("📝 Create account to save your work")
                
                if st.button("🔑 Login to Save Data", type="primary"):
                    st.session_state.skip_login = False
                    st.rerun()
    
    def logout(self):
        """Logout user"""
        if st.session_state.get('session_token'):
            self.db.logout_user(st.session_state.session_token)
        
        self.clear_session()
        st.success("👋 Logged out successfully!")
        st.rerun()
    
    def validate_session(self) -> bool:
        """Validate current session"""
        if not st.session_state.get('session_token'):
            return False
        
        result = self.db.validate_session(st.session_state.session_token)
        
        if not result["success"]:
            self.clear_session()
            return False
        
        return True
    
    def clear_session(self):
        """Clear session state"""
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.session_token = None
        st.session_state.skip_login = False
    
    def require_auth(self):
        """Optional authentication - user can skip or login"""
        self.init_session_state()
        
        if st.session_state.authenticated and self.validate_session():
            return True
        
        if st.session_state.get('skip_login', False):
            return True
        
        self.show_optional_login_page()
        return False
    
    def save_user_session(self, session_data: Dict):
        """Save user's blog session to database"""
        if st.session_state.authenticated and not st.session_state.get('skip_login', False):
            result = self.db.save_blog_session(st.session_state.user_id, session_data)
            if result["success"]:
                print(f"✅ Session saved for user {st.session_state.username}")
        elif st.session_state.get('skip_login', False):
            print("📝 Guest mode - session not saved")
    
    def save_user_post(self, post_data: Dict):
        """Save user's posting history to database"""
        if st.session_state.authenticated and not st.session_state.get('skip_login', False):
            result = self.db.save_posting_history(st.session_state.user_id, post_data)
            if result["success"]:
                print(f"✅ Post history saved for user {st.session_state.username}")
        elif st.session_state.get('skip_login', False):
            print("📝 Guest mode - post history not saved")
    
    def get_user_history(self):
        """Get user's previous sessions"""
        if st.session_state.authenticated:
            return self.db.get_user_sessions(st.session_state.user_id)
        return []
    
    def show_user_history(self):
        """Display user's previous sessions"""
        if not st.session_state.authenticated:
            return
        
        st.subheader("📚 Your Previous Sessions")
        
        sessions = self.get_user_history()
        
        if sessions:
            for i, session in enumerate(sessions[:5], 1):
                created_at = session["created_at"].strftime("%Y-%m-%d %H:%M")
                
                with st.expander(f"📝 Session {i}: {session.get('topic', 'Unknown')} - {created_at}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Topic:** {session.get('topic', 'N/A')}")
                        st.write(f"**Platform:** {session.get('platform', 'N/A')}")
                        st.write(f"**Focus:** {session.get('content_focus', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Created:** {created_at}")
                        if session.get('generated_topics'):
                            st.write(f"**Topics Generated:** {len(session['generated_topics'])}")
                    
                    if st.button(f"🔄 Restore Session {i}", key=f"restore_{session['_id']}"):
                        if session.get('topic'):
                            st.session_state.restored_topic = session['topic']
                        if session.get('platform'):
                            st.session_state.restored_platform = session['platform']
                        st.success(f"✅ Session {i} restored!")
                        st.rerun()
        else:
            st.info("📝 No previous sessions found. Start creating content to build your history!")

# Global auth manager instance
auth_manager = AuthManager()