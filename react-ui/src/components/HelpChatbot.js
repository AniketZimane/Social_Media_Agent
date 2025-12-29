import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, X, Send, Bot } from 'lucide-react';

const HelpChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your AI Blog Assistant guide. Ask me about any feature or how to use this application!",
      isBot: true,
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');

  const knowledgeBase = {
    'generate content': 'The Generate Content tab lets you create AI-powered blog topics. Enter your topic, select platform, choose content focus, and click "Generate Blog Topics" to get personalized suggestions with engagement predictions.',
    'voice assistant': 'Voice Assistant allows you to create content using voice commands. Click the microphone, speak your topic, and the AI will generate blog content automatically. Perfect for hands-free content creation.',
    'video lectures': 'Video Lectures provide educational content about content creation, AI tools, and social media strategies. Click on any video to watch and learn from experts.',
    'opportunity': 'The Opportunity tab shows content writing jobs and freelance opportunities. Filter by category, location, or salary to find the perfect writing gig.',
    'auto post': 'Auto Post lets you schedule content across multiple platforms. Set date, time, select platforms, and your content will be posted automatically.',
    'platform optimizer': 'Platform Optimizer analyzes your content and provides platform-specific recommendations for Instagram, Twitter, LinkedIn, YouTube, and Facebook.',
    'calendar': '7-Day Calendar generates a complete week-long content schedule with optimized posting times and platform-specific content suggestions.',
    'social scheduler': 'Social Scheduler helps you plan and schedule posts across different social media platforms with optimal timing recommendations.',
    'analytics': 'Analytics Dashboard shows your content performance, engagement metrics, trending topics, and platform comparison charts.',
    'how to use': 'Start with Generate Content to create topics, use Voice Assistant for quick creation, check Video Lectures to learn, find jobs in Opportunity tab, and schedule posts with Auto Post feature.',
    'features': 'Key features include: AI content generation, voice commands, video learning, job marketplace, auto-posting, platform optimization, content calendar, and analytics dashboard.',
    'getting started': 'To get started: 1) Go to Generate Content, 2) Enter your topic, 3) Select target platform, 4) Generate content, 5) Use Platform Optimizer for improvements, 6) Schedule with Auto Post.'
  };

  const getResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    
    for (const [key, response] of Object.entries(knowledgeBase)) {
      if (message.includes(key)) {
        return response;
      }
    }
    
    if (message.includes('hello') || message.includes('hi')) {
      return "Hello! I'm here to help you navigate the AI Blog Assistant. Ask me about any feature like 'generate content', 'voice assistant', 'auto post', or 'how to use' the application.";
    }
    
    return "I can help you with: Generate Content, Voice Assistant, Video Lectures, Opportunity (jobs), Auto Post, Platform Optimizer, 7-Day Calendar, Social Scheduler, and Analytics. What would you like to know about?";
  };

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      text: inputMessage,
      isBot: false,
      timestamp: new Date()
    };

    const botResponse = {
      id: messages.length + 2,
      text: getResponse(inputMessage),
      isBot: true,
      timestamp: new Date()
    };

    setMessages([...messages, userMessage, botResponse]);
    setInputMessage('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <motion.button
        className="chat-toggle-btn"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
          border: 'none',
          color: 'white',
          cursor: 'pointer',
          boxShadow: '0 8px 25px rgba(99, 102, 241, 0.4)',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
      </motion.button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.8 }}
            style={{
              position: 'fixed',
              bottom: '90px',
              right: '20px',
              width: '350px',
              height: '500px',
              background: 'rgba(15, 23, 42, 0.95)',
              border: '2px solid rgba(99, 102, 241, 0.3)',
              borderRadius: '20px',
              backdropFilter: 'blur(20px)',
              zIndex: 999,
              display: 'flex',
              flexDirection: 'column',
              overflow: 'hidden',
              boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)'
            }}
          >
            {/* Header */}
            <div style={{
              padding: '20px',
              borderBottom: '1px solid rgba(99, 102, 241, 0.2)',
              display: 'flex',
              alignItems: 'center',
              gap: '12px'
            }}>
              <div style={{
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Bot size={20} color="white" />
              </div>
              <div>
                <h3 style={{ color: '#f1f5f9', margin: 0, fontSize: '16px' }}>AI Assistant Guide</h3>
                <p style={{ color: '#cbd5e1', margin: 0, fontSize: '12px' }}>Ask me anything about this app</p>
              </div>
            </div>

            {/* Messages */}
            <div style={{
              flex: 1,
              padding: '20px',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px'
            }}>
              {messages.map((message) => (
                <div
                  key={message.id}
                  style={{
                    alignSelf: message.isBot ? 'flex-start' : 'flex-end',
                    maxWidth: '80%'
                  }}
                >
                  <div style={{
                    padding: '12px 16px',
                    borderRadius: message.isBot ? '18px 18px 18px 4px' : '18px 18px 4px 18px',
                    background: message.isBot 
                      ? 'rgba(99, 102, 241, 0.1)' 
                      : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                    color: message.isBot ? '#e2e8f0' : 'white',
                    fontSize: '14px',
                    lineHeight: '1.4',
                    border: message.isBot ? '1px solid rgba(99, 102, 241, 0.2)' : 'none'
                  }}>
                    {message.text}
                  </div>
                </div>
              ))}
            </div>

            {/* Input */}
            <div style={{
              padding: '20px',
              borderTop: '1px solid rgba(99, 102, 241, 0.2)',
              display: 'flex',
              gap: '12px'
            }}>
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about any feature..."
                style={{
                  flex: 1,
                  padding: '12px 16px',
                  borderRadius: '25px',
                  border: '2px solid rgba(99, 102, 241, 0.2)',
                  background: 'rgba(15, 23, 42, 0.6)',
                  color: '#e2e8f0',
                  fontSize: '14px',
                  outline: 'none'
                }}
              />
              <button
                onClick={handleSendMessage}
                style={{
                  width: '44px',
                  height: '44px',
                  borderRadius: '50%',
                  border: 'none',
                  background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                  color: 'white',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <Send size={18} />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default HelpChatbot;