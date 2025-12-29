import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Bot, Sparkles, TrendingUp, Calendar, Settings, BarChart3, Mic, Play, Briefcase, Clock } from 'lucide-react';
import Header from './components/Header';
import ContentGenerator from './components/ContentGenerator';
import SocialMediaScheduler from './components/SocialMediaScheduler';
import Dashboard from './components/Dashboard';
import PlatformOptimizer from './components/PlatformOptimizer';
import ContentCalendar from './components/ContentCalendar';
import VoiceAssistant from './components/VoiceAssistant';
import VideoLecture from './components/VideoLecture';
import ContentWriterJobs from './components/ContentWriterJobs';
import ScheduledPosts from './components/ScheduledPosts';
import HelpChatbot from './components/HelpChatbot';
import AuthModal from './components/AuthModal';
import Footer from './components/Footer';
import './App.css';
import './components/AuthModal.css';

function App() {
  const [activeTab, setActiveTab] = useState('generate');
  const [blogContent, setBlogContent] = useState(null);
  const [postingHistory, setPostingHistory] = useState([]);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [user, setUser] = useState(null);
  const [isGuest, setIsGuest] = useState(false);

  // Check authentication on app load
  useEffect(() => {
    const authToken = localStorage.getItem('authToken');
    const skipAuth = localStorage.getItem('skipAuth');
    const username = localStorage.getItem('username');
    const userId = localStorage.getItem('userId');

    if (authToken && username && userId) {
      // Validate token with backend
      validateToken(authToken);
    } else if (skipAuth === 'true') {
      setIsGuest(true);
    } else {
      setShowAuthModal(true);
    }
  }, []);

  const validateToken = async (token) => {
    try {
      const response = await fetch('http://localhost:5001/api/auth/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token })
      });

      const result = await response.json();
      
      if (result.success) {
        setUser({
          id: result.user_id,
          username: result.username,
          token: token
        });
      } else {
        // Token invalid, show auth modal
        localStorage.removeItem('authToken');
        localStorage.removeItem('userId');
        localStorage.removeItem('username');
        setShowAuthModal(true);
      }
    } catch (error) {
      console.error('Token validation failed:', error);
      setShowAuthModal(true);
    }
  };

  const handleAuthSuccess = (authData) => {
    if (authData.skip) {
      setIsGuest(true);
    } else {
      setUser({
        id: authData.user_id,
        username: authData.username,
        token: authData.session_token
      });
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    localStorage.removeItem('skipAuth');
    setUser(null);
    setIsGuest(false);
    setShowAuthModal(true);
  };

  // Listen for navigation events from Voice Assistant
  useEffect(() => {
    const handleNavigateToOptimizer = (event) => {
      console.log('Received navigation event:', event.detail);
      if (event.detail && event.detail.blogContent) {
        setBlogContent(event.detail.blogContent);
        setActiveTab('optimize');
      }
    };
    
    window.addEventListener('navigateToOptimizer', handleNavigateToOptimizer);
    
    return () => {
      window.removeEventListener('navigateToOptimizer', handleNavigateToOptimizer);
    };
  }, []);

  const tabs = [
    { id: 'generate', label: 'Generate Content', icon: Sparkles },
    { id: 'voice', label: 'Voice Assistant', icon: Mic },
    { id: 'videos', label: 'Video Lectures', icon: Play },
    { id: 'jobs', label: 'Opportunity', icon: Briefcase },
    { id: 'scheduled', label: 'Auto Post', icon: Clock },
    { id: 'optimize', label: 'Platform Optimizer', icon: TrendingUp },
    { id: 'calendar', label: '7-Day Calendar', icon: Calendar },
    { id: 'schedule', label: 'Social Scheduler', icon: Settings },
    { id: 'dashboard', label: 'Analytics', icon: BarChart3 }
  ];

  return (
    <div className="app">
      {showAuthModal && (
        <AuthModal
          isOpen={showAuthModal}
          onClose={() => setShowAuthModal(false)}
          onAuthSuccess={handleAuthSuccess}
        />
      )}
      
      <Header user={user} isGuest={isGuest} onLogout={handleLogout} />
      
      <nav className="tab-navigation">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <motion.button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Icon size={20} />
              {tab.label}
            </motion.button>
          );
        })}
      </nav>

      <main className="main-content">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'generate' && (
            <ContentGenerator 
              setBlogContent={setBlogContent}
              blogContent={blogContent}
            />
          )}
          
          {activeTab === 'voice' && (
            <VoiceAssistant />
          )}
          
          {activeTab === 'videos' && (
            <VideoLecture />
          )}
          
          {activeTab === 'jobs' && (
            <ContentWriterJobs />
          )}
          
          {activeTab === 'scheduled' && (
            <ScheduledPosts blogContent={blogContent} />
          )}
          
          {activeTab === 'optimize' && (
            <PlatformOptimizer 
              blogContent={blogContent} 
            />
          )}
          
          {activeTab === 'calendar' && (
            <ContentCalendar blogContent={blogContent} />
          )}
          
          {activeTab === 'schedule' && (
            <SocialMediaScheduler 
              blogContent={blogContent}
              postingHistory={postingHistory}
              setPostingHistory={setPostingHistory}
              setBlogContent={setBlogContent}
            />
          )}
          
          {activeTab === 'dashboard' && (
            <Dashboard postingHistory={postingHistory} />
          )}
        </motion.div>
      </main>
      
      <HelpChatbot />
      <Footer />
    </div>
  );
}

export default App;