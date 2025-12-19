import React from 'react';
import { motion } from 'framer-motion';
import { Target, Clock, Hash, Users, TrendingUp } from 'lucide-react';

const PlatformOptimizer = ({ blogContent }) => {
  // Use the main blog content
  const activeContent = blogContent;
  const platforms = [
    {
      id: 'instagram',
      name: '📸 Instagram',
      color: '#E4405F',
      bestTimes: ['6-9 PM'],
      bestDays: ['Wed', 'Fri', 'Sun'],
      contentTypes: ['Reels', 'Carousel', 'Stories'],
      engagement: 92,
      tips: [
        'Use high-quality visuals',
        'Include 8-12 relevant hashtags',
        'Post during evening hours',
        'Use Instagram Stories for behind-the-scenes content'
      ]
    },
    {
      id: 'twitter',
      name: '🐦 Twitter',
      color: '#1DA1F2',
      bestTimes: ['12-3 PM', '6 PM'],
      bestDays: ['Tue', 'Wed', 'Thu'],
      contentTypes: ['Threads', 'News', 'Quick Takes'],
      engagement: 87,
      tips: [
        'Keep tweets under 280 characters',
        'Use trending hashtags',
        'Engage with replies quickly',
        'Share bite-sized insights'
      ]
    },
    {
      id: 'linkedin',
      name: '💼 LinkedIn',
      color: '#0077B5',
      bestTimes: ['9-11 AM'],
      bestDays: ['Tue', 'Wed'],
      contentTypes: ['Professional Insights', 'Industry News'],
      engagement: 78,
      tips: [
        'Focus on professional value',
        'Share industry insights',
        'Use professional tone',
        'Include relevant statistics'
      ]
    },
    {
      id: 'youtube',
      name: '📺 YouTube',
      color: '#FF0000',
      bestTimes: ['1-4 PM'],
      bestDays: ['Thu', 'Fri', 'Sat'],
      contentTypes: ['Tutorials', 'Long-form', 'Reviews'],
      engagement: 85,
      tips: [
        'Create compelling thumbnails',
        'Optimize video titles for SEO',
        'Include clear call-to-actions',
        'Maintain 8-12 minute length'
      ]
    }
  ];

  const getOptimizedContent = (platform, content = activeContent) => {
    if (!content) return null;

    const maxLength = {
      twitter: 280,
      instagram: 2200,
      linkedin: 1300,
      youtube: 5000
    };

    const textContent = content.content ? content.content.substring(0, maxLength[platform.id] || 1000) : '';
    
    // Handle different hashtag formats
    let hashtags = [];
    if (content.hashtags) {
      if (Array.isArray(content.hashtags)) {
        hashtags = content.hashtags.slice(0, platform.id === 'instagram' ? 10 : 5);
      } else if (typeof content.hashtags === 'string') {
        hashtags = content.hashtags.split(' ').filter(tag => tag.startsWith('#')).slice(0, platform.id === 'instagram' ? 10 : 5);
      }
    }
    
    // Generate default hashtags if none exist or array is empty
    if (!hashtags || hashtags.length === 0) {
      const topic = content.title || content.topic || 'content';
      const cleanTopic = topic.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '');
      const platformName = platform.id;
      hashtags = [`#${cleanTopic}`, `#${platformName}tips`, '#contentcreation', '#blog', '#2024'];
    }

    return {
      content: textContent + (content.content && textContent.length < content.content.length ? '...' : ''),
      hashtags: Array.isArray(hashtags) ? hashtags.join(' ') : hashtags
    };
  };

  return (
    <div className="platform-optimizer">
      <motion.div 
        className="card"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
      >
        <div className="section-header">
          <Target className="section-icon" />
          <h2>Platform Optimizer</h2>
        </div>

        {!activeContent ? (
          <div className="no-content">
            <p>💡 Generate blog content first to see platform-specific optimizations!</p>
            <p>Go to the "Generate Content" tab to create your first blog post.</p>
          </div>
        ) : (
          <div className="platforms-container">
            {platforms.map((platform, index) => {
              const optimizedContent = getOptimizedContent(platform, activeContent);
              
              return (
                <motion.div
                  key={platform.id}
                  className="platform-card"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                >
                  <div className="platform-header">
                    <div className="platform-info">
                      <h3>{platform.name}</h3>
                      <div className="engagement-score">
                        <TrendingUp size={16} />
                        {platform.engagement}% engagement
                      </div>
                    </div>
                    <div 
                      className="platform-indicator"
                      style={{ background: platform.color }}
                    />
                  </div>

                  <div className="platform-details">
                    <div className="detail-grid">
                      <div className="detail-item">
                        <Clock size={16} />
                        <div>
                          <strong>Best Times:</strong>
                          <span>{platform.bestTimes.join(', ')}</span>
                        </div>
                      </div>

                      <div className="detail-item">
                        <Users size={16} />
                        <div>
                          <strong>Best Days:</strong>
                          <span>{platform.bestDays.join(', ')}</span>
                        </div>
                      </div>

                      <div className="detail-item">
                        <Hash size={16} />
                        <div>
                          <strong>Content Types:</strong>
                          <span>{platform.contentTypes.join(', ')}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="optimized-content">
                    <h4>📝 Optimized Content Preview</h4>
                    <div className="content-preview">
                      <div className="content-title">
                        <strong>{activeContent.title || 'Blog Post'}</strong>
                      </div>
                      <p>{optimizedContent.content}</p>
                      <div className="hashtags">
                        {optimizedContent.hashtags}
                      </div>
                    </div>
                  </div>

                  <div className="optimization-tips">
                    <h4>💡 Optimization Tips</h4>
                    <ul>
                      {platform.tips.map((tip, tipIndex) => (
                        <li key={tipIndex}>{tip}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="platform-actions">
                    <button 
                      className="button-secondary"
                      style={{ borderColor: platform.color, color: platform.color }}
                    >
                      Copy Content
                    </button>
                    <button 
                      className="button-primary"
                      style={{ background: platform.color }}
                    >
                      Schedule Post
                    </button>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </motion.div>

      <style jsx>{`
        .platform-optimizer {
          max-width: 1200px;
          margin: 0 auto;
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

        .platforms-container {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
          gap: 2rem;
        }

        .platform-card {
          background: #f9fafb;
          border-radius: 16px;
          padding: 1.5rem;
          border: 1px solid #e5e7eb;
          transition: all 0.3s ease;
        }

        .platform-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .platform-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1.5rem;
        }

        .platform-info h3 {
          color: #1f2937;
          font-size: 1.25rem;
          margin: 0 0 0.5rem 0;
        }

        .engagement-score {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #10b981;
          font-weight: 500;
          font-size: 0.9rem;
        }

        .platform-indicator {
          width: 12px;
          height: 60px;
          border-radius: 6px;
        }

        .platform-details {
          margin-bottom: 1.5rem;
        }

        .detail-grid {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .detail-item {
          display: flex;
          align-items: flex-start;
          gap: 0.75rem;
          color: #4b5563;
        }

        .detail-item svg {
          margin-top: 0.25rem;
          flex-shrink: 0;
        }

        .detail-item strong {
          display: block;
          color: #1f2937;
          margin-bottom: 0.25rem;
        }

        .optimized-content {
          margin-bottom: 1.5rem;
        }

        .optimized-content h4 {
          color: #1f2937;
          margin-bottom: 1rem;
          font-size: 1rem;
        }

        .content-preview {
          background: white;
          border-radius: 8px;
          padding: 1rem;
          border-left: 3px solid #667eea;
        }

        .content-title {
          margin-bottom: 0.75rem;
          color: #1f2937;
          font-size: 1.1rem;
        }

        .content-preview p {
          color: #374151;
          line-height: 1.5;
          margin-bottom: 0.75rem;
        }

        .hashtags {
          color: #667eea;
          font-weight: 500;
          font-size: 0.9rem;
        }

        .optimization-tips {
          margin-bottom: 1.5rem;
        }

        .optimization-tips h4 {
          color: #1f2937;
          margin-bottom: 0.75rem;
          font-size: 1rem;
        }

        .optimization-tips ul {
          list-style: none;
          padding: 0;
          margin: 0;
        }

        .optimization-tips li {
          color: #4b5563;
          padding: 0.25rem 0;
          position: relative;
          padding-left: 1.5rem;
        }

        .optimization-tips li:before {
          content: '•';
          color: #667eea;
          font-weight: bold;
          position: absolute;
          left: 0;
        }

        .platform-actions {
          display: flex;
          gap: 1rem;
        }

        .platform-actions button {
          flex: 1;
          padding: 0.75rem 1rem;
          border-radius: 8px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .platform-actions button:hover {
          transform: translateY(-1px);
        }

        @media (max-width: 768px) {
          .platforms-container {
            grid-template-columns: 1fr;
          }

          .platform-actions {
            flex-direction: column;
          }
        }
      `}</style>
    </div>
  );
};

export default PlatformOptimizer;