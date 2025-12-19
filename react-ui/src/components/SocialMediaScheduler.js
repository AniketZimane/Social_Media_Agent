import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Clock, Send, CheckCircle, XCircle, Settings, Upload, FileText, Image, Key, ArrowRight, ArrowLeft } from 'lucide-react';

const SocialMediaScheduler = ({ blogContent, postingHistory, setPostingHistory, setBlogContent }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedPlatforms, setSelectedPlatforms] = useState([]);
  const [scheduleDate, setScheduleDate] = useState(new Date().toISOString().split('T')[0]);
  const [scheduleTime, setScheduleTime] = useState('18:00');

  const [tokens, setTokens] = useState({
    facebook: '',
    twitter: '',
    linkedin: 'AQWmFzYC_NIKMAnx9ftq...',
    instagram: ''
  });

  const platforms = [
    { id: 'facebook', name: '📘 Facebook', color: '#1877F2' },
    { id: 'twitter', name: '🐦 Twitter', color: '#1DA1F2' },
    { id: 'linkedin', name: '💼 LinkedIn', color: '#0077B5' },
    { id: 'instagram', name: '📷 Instagram', color: '#E4405F' }
  ];

  const handlePlatformToggle = (platformId) => {
    setSelectedPlatforms(prev => 
      prev.includes(platformId) 
        ? prev.filter(id => id !== platformId)
        : [...prev, platformId]
    );
  };



  const saveTokens = () => {
    localStorage.setItem('socialMediaTokens', JSON.stringify(tokens));
    setCurrentStep(3);
  };

  const loadSavedTokens = () => {
    const saved = localStorage.getItem('socialMediaTokens');
    if (saved) {
      setTokens(JSON.parse(saved));
    }
  };

  const schedulePost = () => {
    if (!blogContent || selectedPlatforms.length === 0) return;

    const newPost = {
      id: Date.now(),
      title: blogContent.title,
      platforms: selectedPlatforms.map(id => platforms.find(p => p.id === id).name),
      scheduledTime: new Date(`${scheduleDate}T${scheduleTime}`),
      status: 'scheduled',
      createdAt: new Date(),
      source: 'generated'
    };

    setPostingHistory(prev => [...prev, newPost]);

    // Simulate posting
    setTimeout(() => {
      const results = selectedPlatforms.map(platformId => ({
        platform: platformId,
        success: Math.random() > 0.3, // 70% success rate
        message: Math.random() > 0.3 ? 'Posted successfully' : 'API error'
      }));

      setPostingHistory(prev => 
        prev.map(post => 
          post.id === newPost.id 
            ? { 
                ...post, 
                status: results.some(r => r.success) ? 'posted' : 'failed',
                results,
                postedAt: new Date()
              }
            : post
        )
      );
    }, 2000);
    
    setCurrentStep(1); // Reset to step 1
  };

  React.useEffect(() => {
    loadSavedTokens();
  }, []);

  const renderStep1 = () => (
    <div className="step-content">
      <h3>📝 Step 1: Content Ready</h3>
      
      {blogContent ? (
        <div className="content-preview-card">
          <h4>✨ Generated Content Preview</h4>
          <div className="content-preview-mini">
            <p><strong>{blogContent.title}</strong></p>
            <p>{blogContent.content.substring(0, 150)}...</p>
            <div className="content-stats">
              <span>📝 {blogContent.wordCount || blogContent.content.split(' ').length} words</span>
              <span>🏷️ {blogContent.hashtags?.length || 0} hashtags</span>
            </div>
          </div>
          <button className="button-primary" onClick={() => setCurrentStep(2)}>
            <ArrowRight size={16} />
            Configure Tokens
          </button>
        </div>
      ) : (
        <div className="no-content-card">
          <h4>📝 No Content Available</h4>
          <p>Please generate content first using the Content Generator above.</p>
        </div>
      )}
    </div>
  );

  const renderStep2 = () => (
    <div className="step-content">
      <h3>🔑 Step 2: Configure API Tokens</h3>
      
      <div className="token-config">
        {platforms.map(platform => (
          <div key={platform.id} className="token-field">
            <label>{platform.name} API Token:</label>
            <div className="token-input-group">
              <Key size={16} />
              <input
                type="password"
                className="input-field"
                placeholder={`Enter ${platform.name} token...`}
                value={tokens[platform.id]}
                onChange={(e) => setTokens(prev => ({...prev, [platform.id]: e.target.value}))}
              />
            </div>
          </div>
        ))}
        
        <div className="step-actions">
          <button className="button-secondary" onClick={() => setCurrentStep(1)}>
            <ArrowLeft size={16} />
            Back
          </button>
          <button className="button-primary" onClick={saveTokens}>
            <ArrowRight size={16} />
            Save & Continue
          </button>
        </div>
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="step-content">
      <h3>📅 Step 3: Schedule & Post</h3>
      
      {blogContent && (
        <div className="final-content-preview">
          <h4>📝 Content to Post:</h4>
          <div className="content-summary">
            <p><strong>{blogContent.title}</strong></p>
            <p>{blogContent.content.substring(0, 200)}...</p>
            <div className="content-meta-mini">
              <span>📝 {blogContent.wordCount || blogContent.content.split(' ').length} words</span>
              <span>🏷️ {blogContent.hashtags.length} hashtags</span>
            </div>
          </div>
        </div>
      )}
      
      <div className="platform-selection">
        <h4>🔗 Select Platforms:</h4>
        <div className="platforms-grid">
          {platforms.map(platform => (
            <motion.div
              key={platform.id}
              className={`platform-card ${selectedPlatforms.includes(platform.id) ? 'selected' : ''}`}
              onClick={() => handlePlatformToggle(platform.id)}
              whileHover={{ scale: 1.02 }}
            >
              <span>{platform.name}</span>
              {tokens[platform.id] ? (
                <CheckCircle size={16} className="status-icon success" />
              ) : (
                <XCircle size={16} className="status-icon error" />
              )}
            </motion.div>
          ))}
        </div>
      </div>
      
      <div className="schedule-settings">
        <h4>⏰ Schedule Settings:</h4>
        <div className="schedule-grid">
          <input
            type="date"
            className="input-field"
            value={scheduleDate}
            onChange={(e) => setScheduleDate(e.target.value)}
          />
          <input
            type="time"
            className="input-field"
            value={scheduleTime}
            onChange={(e) => setScheduleTime(e.target.value)}
          />
        </div>
      </div>
      
      <div className="step-actions">
        <button className="button-secondary" onClick={() => setCurrentStep(2)}>
          <ArrowLeft size={16} />
          Back
        </button>
        <button 
          className="button-primary"
          onClick={schedulePost}
          disabled={selectedPlatforms.length === 0}
        >
          <Send size={16} />
          Schedule Post ({selectedPlatforms.length} platforms)
        </button>
      </div>
    </div>
  );

  return (
    <div className="social-scheduler">
      <motion.div 
        className="card"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
      >
        <div className="section-header">
          <Calendar className="section-icon" />
          <h2>Dynamic Social Media Scheduler</h2>
        </div>
        
        <div className="step-indicator">
          {[1, 2, 3].map(step => (
            <div key={step} className={`step ${currentStep >= step ? 'active' : ''}`}>
              <span>{step}</span>
            </div>
          ))}
        </div>

        {currentStep === 1 && renderStep1()}
        {currentStep === 2 && renderStep2()}
        {currentStep === 3 && renderStep3()}
      </motion.div>

      <style jsx>{`
        .social-scheduler {
          max-width: 1000px;
          margin: 0 auto;
        }

        .step-indicator {
          display: flex;
          justify-content: center;
          gap: 2rem;
          margin-bottom: 2rem;
        }

        .step {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: rgba(99, 102, 241, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          color: #6366f1;
          font-weight: 600;
          transition: all 0.3s ease;
        }

        .step.active {
          background: #6366f1;
          color: white;
        }

        .step-content {
          min-height: 400px;
        }

        .content-preview-card {
          background: rgba(15, 23, 42, 0.4);
          border: 1px solid rgba(99, 102, 241, 0.2);
          border-radius: 16px;
          padding: 2rem;
          text-align: center;
          margin-top: 2rem;
        }

        .content-preview-card h4 {
          color: #f1f5f9;
          margin-bottom: 1.5rem;
        }

        .no-content-card {
          background: rgba(15, 23, 42, 0.4);
          border: 2px dashed rgba(99, 102, 241, 0.3);
          border-radius: 16px;
          padding: 3rem;
          text-align: center;
          margin-top: 2rem;
        }

        .no-content-card h4 {
          color: #94a3b8;
          margin-bottom: 1rem;
        }

        .no-content-card p {
          color: #64748b;
        }

        .content-stats {
          display: flex;
          gap: 1rem;
          justify-content: center;
          margin: 1rem 0;
          font-size: 0.9rem;
          color: #6366f1;
        }

        .token-config {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .token-field label {
          color: #cbd5e1;
          font-weight: 500;
          margin-bottom: 0.5rem;
          display: block;
        }

        .token-input-group {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #6366f1;
        }

        .step-actions {
          display: flex;
          justify-content: space-between;
          margin-top: 2rem;
        }

        .content-preview-mini {
          text-align: left;
          background: rgba(99, 102, 241, 0.1);
          padding: 1rem;
          border-radius: 8px;
          margin-top: 1rem;
        }

        .content-preview-mini p {
          color: #cbd5e1;
          margin: 0.5rem 0;
        }

        .final-content-preview {
          background: rgba(15, 23, 42, 0.4);
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }

        .content-summary {
          margin-top: 1rem;
        }

        .content-meta-mini {
          display: flex;
          gap: 1rem;
          margin-top: 1rem;
          font-size: 0.9rem;
          color: #6366f1;
        }

        .section-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 2rem;
        }

        .section-icon {
          color: #667eea;
        }

        .section-header h2 {
          font-size: 1.75rem;
          font-weight: 600;
          color: #f1f5f9;
        }

        .no-content {
          text-align: center;
          padding: 3rem;
          color: #6b7280;
          font-size: 1.1rem;
        }

        .content-preview {
          margin-bottom: 2rem;
        }

        .content-preview h3 {
          color: #1f2937;
          margin-bottom: 1rem;
        }

        .preview-card {
          background: #f9fafb;
          border-radius: 12px;
          padding: 1.5rem;
          border-left: 4px solid #667eea;
        }

        .preview-card h4 {
          color: #1f2937;
          margin-bottom: 0.5rem;
        }

        .preview-card p {
          color: #6b7280;
          margin-bottom: 1rem;
        }

        .hashtags {
          color: #667eea;
          font-weight: 500;
        }

        .platform-selection {
          margin-bottom: 2rem;
        }

        .platform-selection h3 {
          color: #1f2937;
          margin-bottom: 1rem;
        }

        .platforms-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
        }

        .platform-card {
          background: #f9fafb;
          border: 2px solid #e5e7eb;
          border-radius: 12px;
          padding: 1rem;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .platform-card:hover {
          border-color: #667eea;
          background: #f0f4ff;
        }

        .platform-card.selected {
          border-color: #667eea;
          background: linear-gradient(135deg, #667eea10, #764ba210);
        }

        .platform-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
        }

        .platform-name {
          font-weight: 500;
          color: #1f2937;
        }

        .check-icon {
          color: #10b981;
        }

        .token-status {
          font-size: 0.9rem;
        }

        .connected {
          color: #10b981;
        }

        .disconnected {
          color: #ef4444;
        }

        .schedule-settings {
          margin-bottom: 2rem;
        }

        .schedule-settings h3 {
          color: #1f2937;
          margin-bottom: 1rem;
        }

        .schedule-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1rem;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .form-group label {
          font-weight: 500;
          color: #374151;
        }

        .action-section {
          display: flex;
          justify-content: center;
        }

        .schedule-btn {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1.1rem;
          padding: 1rem 2rem;
        }

        .schedule-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        @media (max-width: 768px) {
          .platforms-grid {
            grid-template-columns: 1fr;
          }

          .schedule-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default SocialMediaScheduler;