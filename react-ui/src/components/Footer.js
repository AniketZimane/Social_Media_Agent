import React from 'react';
import { Heart } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <p>
          Developed with <Heart size={16} className="heart-icon" /> by 
          <strong> Aniket Zimane,Kiran Janjal,Abhay Sangle</strong> | Team - Agentic Agent
        </p>
        <p className="footer-year">© 2025 Agentic AI Blog Assistant</p>
      </div>
      
      <style jsx>{`
        .app-footer {
          background: rgba(15, 23, 42, 0.8);
          border-top: 1px solid rgba(99, 102, 241, 0.3);
          padding: 2rem 1rem;
          text-align: center;
          margin-top: 4rem;
        }
        
        .footer-content {
          max-width: 1200px;
          margin: 0 auto;
        }
        
        .footer-content p {
          color: #cbd5e1;
          margin: 0.5rem 0;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
        }
        
        .heart-icon {
          color: #ef4444;
          animation: heartbeat 1.5s ease-in-out infinite;
        }
        
        .footer-content strong {
          color: #6366f1;
          font-weight: 600;
        }
        
        .footer-year {
          font-size: 0.9rem;
          color: #94a3b8;
        }
        
        @keyframes heartbeat {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.1); }
        }
      `}</style>
    </footer>
  );
};

export default Footer;
