import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Bot, Sparkles, TrendingUp, Calendar, Settings, BarChart3, Mic } from 'lucide-react';
import Header from './components/Header';
import ContentGenerator from './components/ContentGenerator';
import SocialMediaScheduler from './components/SocialMediaScheduler';
import Dashboard from './components/Dashboard';
import PlatformOptimizer from './components/PlatformOptimizer';
import ContentCalendar from './components/ContentCalendar';
import VoiceAssistant from './components/VoiceAssistant';
import Footer from './components/Footer';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('generate');
  const [blogContent, setBlogContent] = useState(null);
  const [postingHistory, setPostingHistory] = useState([]);

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
    { id: 'optimize', label: 'Platform Optimizer', icon: TrendingUp },
    { id: 'calendar', label: '7-Day Calendar', icon: Calendar },
    { id: 'schedule', label: 'Social Scheduler', icon: Settings },
    { id: 'dashboard', label: 'Analytics', icon: BarChart3 }
  ];

  return (
    <div className="app">
      <Header />
      
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
      
      <Footer />
    </div>
  );
}

export default App;