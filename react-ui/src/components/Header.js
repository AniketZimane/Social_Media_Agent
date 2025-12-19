import React from 'react';
import { motion } from 'framer-motion';
import { Bot, Sparkles } from 'lucide-react';

const Header = () => {
  return (
    <motion.header 
      className="header"
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="header-content">
        <div className="logo">
          <Bot size={40} className="logo-icon" />
          <div>
            <h1 className="gradient-text">Agentic AI Blog Assistant</h1>
            <p className="tagline">Intelligent Content Curation & Multi-Platform Optimization</p>
          </div>
        </div>
        
        <div className="ai-status">
          <Sparkles size={20} />
          <span>AI Active</span>
        </div>
      </div>
      
      <style>{`
        .header {
          background: rgba(0, 0, 0, 0.2);
          backdrop-filter: blur(30px);
          padding: 2rem;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .header-content {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .logo {
          display: flex;
          align-items: center;
          gap: 1rem;
        }
        
        .logo-icon {
          color: white;
          background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
          padding: 0.5rem;
          border-radius: 16px;
          box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
        }
        
        .logo h1 {
          font-size: 2rem;
          font-weight: 700;
          margin: 0;
        }
        
        .tagline {
          color: rgba(255, 255, 255, 0.8);
          margin: 0;
          font-size: 0.9rem;
        }
        
        .ai-status {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: rgba(34, 197, 94, 0.2);
          color: #22c55e;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 500;
          border: 1px solid rgba(34, 197, 94, 0.3);
          backdrop-filter: blur(10px);
        }
        
        @media (max-width: 768px) {
          .header-content {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
          }
          
          .logo h1 {
            font-size: 1.5rem;
          }
        }
      `}</style>
    </motion.header>
  );
};

export default Header;