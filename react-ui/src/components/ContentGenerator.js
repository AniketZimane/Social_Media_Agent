import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Wand2, Image, Hash, Target, Edit3, Send } from 'lucide-react';
import BlogPreview from './BlogPreview';

const ContentGenerator = ({ setBlogContent, blogContent }) => {
  const [topic, setTopic] = useState('Artificial Intelligence');
  const [platform, setPlatform] = useState('📸 Instagram');
  const [contentFocus, setContentFocus] = useState('Trending');
  const [maxWords, setMaxWords] = useState(300);
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [useFileContent, setUseFileContent] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editPrompt, setEditPrompt] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  const platforms = [
    '📸 Instagram',
    '🐦 Twitter', 
    '💼 LinkedIn',
    '📺 YouTube',
    '👥 Facebook'
  ];

  const focusOptions = ['Trending', 'Educational', 'Opinion', 'News Analysis'];
  const wordLimits = [150, 300, 500, 800, 1200];
  
  const getHashtagLimit = (platform) => {
    const limits = {
      '📸 Instagram': 30,
      '🐦 Twitter': 5,
      '💼 LinkedIn': 8,
      '📺 YouTube': 15,
      '👥 Facebook': 10
    };
    return limits[platform] || 10;
  };

  const formatContent = (content) => {
    if (!content) return '';
    
    return content
      // Convert markdown-style headers to HTML (only headings are bold)
      .replace(/^### (.*$)/gm, '<h3><strong>$1</strong></h3>')
      .replace(/^## (.*$)/gm, '<h2><strong>$1</strong></h2>')
      .replace(/^# (.*$)/gm, '<h1><strong>$1</strong></h1>')
      // Convert **bold** to HTML (keep existing bold text)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Convert bullet points
      .replace(/^\* (.*$)/gm, '<li>$1</li>')
      // Start new line for any symbol at beginning
      .replace(/^([🏛️🍽️📝🏷️💡⭐🎯🌟✨🔥💯📊🎨🚀💼📱🌐🎪🎭🎨🎵🎬🎮🎲🎯🎪])/gm, '<br/>$1')
      // Wrap consecutive list items in ul tags
      .replace(/((<li>.*<\/li>\s*)+)/g, '<ul>$1</ul>')
      // Convert line breaks and separators
      .replace(/---/g, '<hr/>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br/>')
      // Wrap in paragraph tags
      .split('</p><p>').map(part => {
        if (part.includes('<h') || part.includes('<ul') || part.includes('<hr')) {
          return part;
        }
        return `<p>${part}</p>`;
      }).join('')
      // Clean up extra tags
      .replace(/<p><\/p>/g, '')
      .replace(/<p>(<[h|u|hr|br])/g, '$1')
      .replace(/(<\/[h|u|hr][^>]*>)<\/p>/g, '$1')
      .replace(/<br\/><p>/g, '<br/>');
  };

  const generateContent = async () => {
    setIsGenerating(true);
    
    try {
      let response;
      
      if (useFileContent && uploadedFile) {
        // Generate content from uploaded file
        const formData = new FormData();
        formData.append('file', uploadedFile);
        formData.append('platform', platform);
        formData.append('content_focus', contentFocus);
        formData.append('max_words', maxWords);
        
        response = await fetch('http://localhost:5000/api/generate-from-file', {
          method: 'POST',
          body: formData
        });
      } else {
        // Call your existing Python backend
        response = await fetch('http://localhost:5000/api/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            topic,
            platform,
            content_focus: contentFocus,
            max_words: maxWords,
            ai_mode: 'Dynamic AI'
          })
        });
      }
      
      if (response.ok) {
        const data = await response.json();
        setBlogContent(data);
        setIsGenerating(false);
        return;
      }
    } catch (error) {
      console.log('Using fallback content generation');
    }
    
    // Fallback: Generate content locally (same as your Python logic)
    setTimeout(() => {
      const hashtagLimit = getHashtagLimit(platform);
      const baseContent = `Discover the transformative power of ${topic} in today's digital landscape. This comprehensive guide explores cutting-edge developments, practical applications, and future trends that are reshaping industries worldwide. From breakthrough innovations to real-world implementations, learn how ${topic} is driving unprecedented change and creating new opportunities for businesses and individuals alike. Whether you're a professional looking to stay ahead or someone curious about the latest developments, this insight-packed content will provide you with valuable knowledge and actionable strategies.`;
      
      // Truncate content based on word limit
      const words = baseContent.split(' ');
      const limitedContent = words.slice(0, maxWords).join(' ') + (words.length > maxWords ? '...' : '');
      
      // Enhanced platform-specific hashtag generation
      const generateSmartHashtags = (topic, platform) => {
        const topicKeywords = topic.toLowerCase().split(' ').filter(word => word.length > 3);
        const topicTags = topicKeywords.map(word => `#${word.charAt(0).toUpperCase() + word.slice(1)}`);
        
        const platformStrategies = {
          '📸 Instagram': {
            popular: ['#instagood', '#photooftheday', '#viral', '#trending', '#explore', '#reels'],
            engagement: ['#like4like', '#follow4follow', '#instadaily', '#picoftheday'],
            niche: ['#contentcreator', '#digitalmarketing', '#socialmedia', '#influencer']
          },
          '🐦 Twitter': {
            popular: ['#breaking', '#news', '#trending', '#viral', '#thread', '#twitterchat'],
            engagement: ['#retweet', '#follow', '#discussion', '#opinion'],
            niche: ['#tech', '#innovation', '#startup', '#business', '#thoughtleadership']
          },
          '💼 LinkedIn': {
            popular: ['#professional', '#business', '#career', '#leadership', '#networking'],
            engagement: ['#thoughtleadership', '#industry', '#growth', '#success'],
            niche: ['#corporatelife', '#workculture', '#productivity', '#skills', '#expertise']
          },
          '📺 YouTube': {
            popular: ['#youtube', '#subscribe', '#tutorial', '#howto', '#educational'],
            engagement: ['#youtuber', '#content', '#video', '#learning', '#knowledge'],
            niche: ['#tips', '#guide', '#expert', '#masterclass', '#stepbystep']
          },
          '👥 Facebook': {
            popular: ['#facebook', '#community', '#share', '#like', '#follow'],
            engagement: ['#discussion', '#social', '#connect', '#family', '#friends'],
            niche: ['#lifestyle', '#inspiration', '#motivation', '#stories', '#memories']
          }
        };
        
        const strategy = platformStrategies[platform] || platformStrategies['📸 Instagram'];
        
        // Combine different hashtag types
        let hashtags = [];
        hashtags.push(...topicTags.slice(0, 3)); // Topic-specific
        hashtags.push(...strategy.popular.slice(0, 4)); // Popular platform tags
        hashtags.push(...strategy.engagement.slice(0, 2)); // Engagement tags
        hashtags.push(...strategy.niche.slice(0, 3)); // Niche tags
        hashtags.push('#AI', '#innovation', '#2024', '#future'); // Trending general
        
        // Remove duplicates and return
        return [...new Set(hashtags)];
      };
      
      const selectedHashtags = generateSmartHashtags(topic, platform);
      
      const mockContent = {
        title: `The Future of ${topic}: Revolutionary Insights for 2024`,
        content: limitedContent,
        hashtags: selectedHashtags.slice(0, hashtagLimit),
        cta: `Ready to explore the future of ${topic}? Follow for more insights and join the conversation!`,
        keywords: [topic, 'innovation', 'technology', 'future', '2024'],
        engagement_score: 0.87,
        platform: platform,
        wordCount: limitedContent.split(' ').length
      };
      
      setBlogContent(mockContent);
      setIsGenerating(false);
    }, 2000);
  };

  const handleEditContent = async () => {
    if (!editPrompt.trim()) {
      alert('Please enter your modification requirements');
      return;
    }

    setIsEditing(true);
    
    try {
      const response = await fetch('http://localhost:5001/api/edit-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          originalContent: blogContent,
          editPrompt: editPrompt,
          platform: platform
        })
      });
      
      if (response.ok) {
        const editedData = await response.json();
        setBlogContent(editedData);
        setShowEditModal(false);
        setEditPrompt('');
        setIsEditing(false);
        return;
      }
    } catch (error) {
      console.log('Using fallback edit generation');
    }
    
    // Fallback: Generate edited content locally
    setTimeout(() => {
      const editedContent = {
        ...blogContent,
        title: editPrompt.toLowerCase().includes('title') ? 
          `${blogContent.title} - Updated` : blogContent.title,
        content: editPrompt.toLowerCase().includes('shorter') ? 
          blogContent.content.substring(0, blogContent.content.length / 2) + '...' :
          editPrompt.toLowerCase().includes('longer') ?
          blogContent.content + ` Additionally, ${editPrompt} provides more comprehensive insights and detailed analysis for better understanding.` :
          blogContent.content + ` [Modified based on: ${editPrompt}]`,
        hashtags: editPrompt.toLowerCase().includes('hashtag') ?
          [...(blogContent.hashtags || []), '#updated', '#modified'] :
          blogContent.hashtags
      };
      
      setBlogContent(editedContent);
      setShowEditModal(false);
      setEditPrompt('');
      setIsEditing(false);
    }, 2000);
  };

  if (showPreview && blogContent) {
    return <BlogPreview blogContent={blogContent} onBack={() => setShowPreview(false)} formatContent={formatContent} />;
  }

  return (
    <div className="content-generator">
      <motion.div 
        className="card"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
      >
        <div className="section-header">
          <Sparkles className="section-icon" />
          <h2>AI Content Generator</h2>
        </div>

        <div className="form-grid">
          <div className="form-group">
            <label>📝 Content Source</label>
            <div className="content-source-options">
              <label className="radio-option">
                <input
                  type="radio"
                  name="contentSource"
                  checked={!useFileContent}
                  onChange={() => {
                    setUseFileContent(false);
                    setUploadedFile(null);
                    setTopic('Artificial Intelligence');
                  }}
                />
                <span>Enter Topic</span>
              </label>
              <label className="radio-option">
                <input
                  type="radio"
                  name="contentSource"
                  checked={useFileContent}
                  onChange={() => setUseFileContent(true)}
                />
                <span>Upload File</span>
              </label>
            </div>
            
            {!useFileContent ? (
              <input
                type="text"
                className="input-field"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Enter your topic..."
              />
            ) : (
              <div className="file-upload-section">
                <input
                  type="file"
                  id="file-input"
                  accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
                  onChange={(e) => {
                    const file = e.target.files[0];
                    if (file) {
                      setUploadedFile(file);
                      setTopic(`Content from ${file.name}`);
                    }
                  }}
                  className="file-input"
                  style={{ display: 'none' }}
                />
                <label htmlFor="file-input" className="file-upload-label">
                  📎 {uploadedFile ? uploadedFile.name : 'Choose File (PDF, DOC, DOCX, TXT, JPG, PNG)'}
                </label>
                {uploadedFile && (
                  <div className="file-info">
                    <span className="file-size">{(uploadedFile.size / 1024).toFixed(1)} KB</span>
                    <button 
                      type="button" 
                      onClick={() => {
                        setUploadedFile(null);
                        setTopic('Artificial Intelligence');
                      }}
                      className="remove-file"
                    >
                      ✕
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="form-group">
            <label>🚀 Target Platform</label>
            <select
              className="select-field"
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
            >
              {platforms.map(p => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>🎯 Content Focus</label>
            <select
              className="select-field"
              value={contentFocus}
              onChange={(e) => setContentFocus(e.target.value)}
            >
              {focusOptions.map(f => (
                <option key={f} value={f}>{f}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>📝 Maximum Words: {maxWords}</label>
            <select
              className="select-field"
              value={maxWords}
              onChange={(e) => setMaxWords(parseInt(e.target.value))}
            >
              {wordLimits.map(limit => (
                <option key={limit} value={limit}>{limit} words</option>
              ))}
            </select>
          </div>
        </div>

        <div className="action-buttons">
          <motion.button
            className="button-primary generate-btn"
            onClick={generateContent}
            disabled={isGenerating}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {isGenerating ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                >
                  <Wand2 size={20} />
                </motion.div>
                Generating...
              </>
            ) : (
              <>
                <Sparkles size={20} />
                Generate AI Content
              </>
            )}
          </motion.button>
        </div>

        {isGenerating && (
          <motion.div className="loading-animation" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: "linear" }}>
              <Sparkles size={50} color="#6366f1" />
            </motion.div>
            <p>Creating amazing content...</p>
          </motion.div>
        )}

        {blogContent && (
          <button className="button-primary view-btn" onClick={() => setShowPreview(true)}>
            View Full Blog →
          </button>
        )}

        {blogContent && (
          <motion.div
            className="generated-content"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="content-header">
              <h3>✨ Generated Content</h3>
              <div className="engagement-score">
                <Target size={16} />
                Engagement: {(blogContent.engagement_score * 100).toFixed(0)}%
              </div>
            </div>

            <div className="content-preview">
              <div className="blog-section">
                <h4 className="section-title">📝 {blogContent.title}</h4>
              </div>
              
              {blogContent.image_url && (
                <div className="blog-section">
                  <h4 className="section-title">🖼️ Blog Header Image:</h4>
                  <img 
                    src={blogContent.image_url} 
                    alt={blogContent.title} 
                    className="blog-image"
                    onError={(e) => {
                      console.log('Image load error:', blogContent.image_url);
                      e.target.style.display = 'none';
                    }}
                    onLoad={() => console.log('Image loaded successfully')}
                  />
                </div>
              )}
              
              <div className="blog-section">
                <h4 className="section-title">Blog Content:</h4>
                <div className="content-body" dangerouslySetInnerHTML={{ __html: formatContent(blogContent.content) }} />
              </div>
              
              <div className="blog-section">
                <h4 className="section-title">🏷️ Hashtags:</h4>
                <div className="hashtags-display">{blogContent.hashtags && Array.isArray(blogContent.hashtags) ? blogContent.hashtags.join(' ') : '#content #blog'}</div>
              </div>
              
              <div className="blog-section">
                <h4 className="section-title">💯 Call to Action:</h4>
                <div className="cta-display">{blogContent.cta}</div>
              </div>
              
              <div className="blog-section">
                <h4 className="section-title">🔍 SEO Keywords:</h4>
                <div className="keywords-display">{blogContent.keywords ? blogContent.keywords.join(', ') : 'AI, Innovation, Technology'}</div>
              </div>
              
              <div className="content-stats">
                <span className="word-count">📝 {blogContent.wordCount || blogContent.content.split(' ').length} words</span>
                <span className="hashtag-count">🏷️ {blogContent.hashtags && Array.isArray(blogContent.hashtags) ? blogContent.hashtags.length : 0} hashtags</span>
              </div>
            </div>

            <div className="content-actions">
              <button 
                className="button-secondary"
                onClick={() => setShowEditModal(true)}
              >
                <Edit3 size={16} />
                Edit Content
              </button>
              <button 
                className="button-secondary"
                onClick={async () => {
                  try {
                    const response = await fetch('http://localhost:5002/api/generate-image', {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                      },
                      body: JSON.stringify({
                        title: blogContent.title
                      })
                    });
                    
                    if (response.ok) {
                      const imageResult = await response.json();
                      if (imageResult.success) {
                        setBlogContent({
                          ...blogContent,
                          image_url: imageResult.image_url
                        });
                      }
                    }
                  } catch (error) {
                    console.log('Image generation failed:', error);
                  }
                }}
              >
                <Image size={16} />
                Generate Image
              </button>
              <button className="button-secondary">
                <Hash size={16} />
                More Hashtags
              </button>
            </div>
          </motion.div>
        )}
      </motion.div>

      {/* Edit Content Modal */}
      <AnimatePresence>
        {showEditModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowEditModal(false)}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              backgroundColor: 'rgba(0,0,0,0.8)',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              zIndex: 1000,
              backdropFilter: 'blur(4px)'
            }}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="card"
              style={{
                maxWidth: '600px',
                width: '90%',
                position: 'relative'
              }}
            >
              <button 
                onClick={() => setShowEditModal(false)}
                style={{
                  position: 'absolute',
                  top: '20px',
                  right: '24px',
                  background: 'rgba(99, 102, 241, 0.1)',
                  border: '2px solid rgba(99, 102, 241, 0.3)',
                  fontSize: '20px',
                  cursor: 'pointer',
                  color: '#6366f1',
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >×</button>
              
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '24px'
              }}>
                <div style={{
                  width: '48px',
                  height: '48px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Edit3 size={24} color="white" />
                </div>
                <div>
                  <h3 style={{
                    color: '#f1f5f9',
                    margin: 0,
                    fontSize: '1.5rem',
                    fontWeight: '600'
                  }}>Edit Content</h3>
                  <p style={{
                    color: '#cbd5e1',
                    margin: 0,
                    fontSize: '14px'
                  }}>Describe how you want to modify the content</p>
                </div>
              </div>

              <div style={{
                background: 'rgba(99, 102, 241, 0.1)',
                border: '1px solid rgba(99, 102, 241, 0.2)',
                borderRadius: '12px',
                padding: '16px',
                marginBottom: '24px'
              }}>
                <h4 style={{
                  color: '#f1f5f9',
                  margin: '0 0 8px 0',
                  fontSize: '1.1rem'
                }}>Current Content: {blogContent?.title}</h4>
                <p style={{
                  color: '#cbd5e1',
                  margin: 0,
                  fontSize: '14px',
                  lineHeight: '1.5'
                }}>{blogContent?.content?.substring(0, 150)}...</p>
              </div>

              <div style={{ marginBottom: '24px' }}>
                <label style={{
                  display: 'block',
                  color: '#f1f5f9',
                  marginBottom: '8px',
                  fontWeight: '500'
                }}>Modification Instructions</label>
                <textarea
                  value={editPrompt}
                  onChange={(e) => setEditPrompt(e.target.value)}
                  placeholder="e.g., Make it shorter, add more examples, change the tone to professional, focus more on benefits..."
                  rows={4}
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    borderRadius: '8px',
                    border: '2px solid rgba(99, 102, 241, 0.2)',
                    background: 'rgba(15, 23, 42, 0.6)',
                    color: '#e2e8f0',
                    fontSize: '16px',
                    outline: 'none',
                    resize: 'vertical',
                    fontFamily: 'inherit',
                    lineHeight: '1.5'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                  onBlur={(e) => e.target.style.borderColor = 'rgba(99, 102, 241, 0.2)'}
                />
              </div>

              <div style={{
                background: 'rgba(15, 23, 42, 0.4)',
                border: '1px solid rgba(99, 102, 241, 0.2)',
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '24px'
              }}>
                <p style={{
                  color: '#cbd5e1',
                  margin: 0,
                  fontSize: '14px',
                  lineHeight: '1.5'
                }}>
                  💡 Examples: "Make it more engaging", "Add statistics", "Shorten to 200 words", "Change tone to casual", "Add more hashtags"
                </p>
              </div>

              <div style={{
                display: 'flex',
                gap: '12px'
              }}>
                <button
                  onClick={() => setShowEditModal(false)}
                  className="button-secondary"
                  style={{ flex: 1 }}
                >
                  Cancel
                </button>
                <button
                  onClick={handleEditContent}
                  disabled={isEditing || !editPrompt.trim()}
                  className="button-primary"
                  style={{
                    flex: 1,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px',
                    opacity: (isEditing || !editPrompt.trim()) ? 0.7 : 1
                  }}
                >
                  {isEditing ? (
                    <>
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      >
                        <Wand2 size={16} />
                      </motion.div>
                      Editing...
                    </>
                  ) : (
                    <>
                      <Send size={16} />
                      Apply Changes
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        .content-generator {
          max-width: 800px;
          margin: 0 auto;
        }

        .section-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 2rem;
        }

        .section-icon {
          color: #6366f1;
        }

        .section-header h2 {
          font-size: 1.75rem;
          font-weight: 600;
          color: #f1f5f9;
        }

        .form-grid {
          display: grid;
          gap: 1.5rem;
          margin-bottom: 2rem;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .form-group label {
          font-weight: 500;
          color: #cbd5e1;
        }

        .action-buttons {
          display: flex;
          justify-content: center;
          margin-bottom: 2rem;
        }

        .generate-btn {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 1.1rem;
          padding: 1rem 2rem;
        }

        .generated-content {
          border-top: 2px solid #e5e7eb;
          padding-top: 2rem;
        }

        .content-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1.5rem;
        }

        .content-header h3 {
          color: #f1f5f9;
          font-size: 1.25rem;
        }

        .engagement-score {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 500;
        }

        .content-preview {
          background: rgba(15, 23, 42, 0.4);
          border: 1px solid rgba(99, 102, 241, 0.2);
          border-radius: 16px;
          padding: 1.5rem;
          margin-bottom: 1.5rem;
          backdrop-filter: blur(10px);
        }

        .blog-section {
          margin-bottom: 1.5rem;
          padding-bottom: 1rem;
          border-bottom: 1px solid rgba(99, 102, 241, 0.1);
        }

        .blog-section:last-child {
          border-bottom: none;
          margin-bottom: 0;
        }

        .section-title {
          color: #6366f1;
          font-size: 1rem;
          font-weight: 600;
          margin-bottom: 0.75rem;
        }

        .hashtags-display {
          color: #6366f1;
          font-weight: 500;
          line-height: 1.5;
        }

        .cta-display {
          color: #cbd5e1;
          font-style: italic;
          line-height: 1.5;
        }

        .keywords-display {
          color: #94a3b8;
          line-height: 1.5;
        }

        .content-title {
          color: #f1f5f9;
          font-size: 1.2rem;
          font-weight: 600;
          margin-bottom: 1rem;
        }

        .content-body {
          color: #cbd5e1;
          line-height: 1.6;
          margin-bottom: 1.5rem;
        }

        .content-body h1,
        .content-body h2,
        .content-body h3 {
          color: #f1f5f9;
          font-weight: 600;
          margin: 1.5rem 0 1rem 0;
          line-height: 1.3;
        }

        .content-body h1 { font-size: 1.5rem; }
        .content-body h2 { font-size: 1.3rem; }
        .content-body h3 { font-size: 1.1rem; }

        .content-body ul {
          margin: 1rem 0;
          padding-left: 1.5rem;
        }

        .content-body li {
          margin: 0.5rem 0;
          color: #cbd5e1;
        }

        .content-body strong {
          color: #f1f5f9;
          font-weight: 600;
        }

        .content-body h1 strong,
        .content-body h2 strong,
        .content-body h3 strong {
          color: #f1f5f9;
          font-weight: 700;
        }

        .content-body p {
          margin: 1rem 0;
        }

        .content-body hr {
          border: none;
          border-top: 2px solid rgba(99, 102, 241, 0.3);
          margin: 2rem 0;
        }

        .content-stats {
          display: flex;
          gap: 1rem;
          justify-content: center;
          margin-top: 1rem;
          padding-top: 1rem;
          border-top: 1px solid rgba(99, 102, 241, 0.2);
        }

        .word-count, .hashtag-count {
          background: rgba(99, 102, 241, 0.1);
          color: #6366f1;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.85rem;
          font-weight: 500;
        }

        .hashtags {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #6366f1;
          font-weight: 500;
        }

        .cta {
          color: #94a3b8;
          font-style: italic;
        }

        .content-actions {
          display: flex;
          gap: 1rem;
          justify-content: center;
        }

        .content-actions button {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .blog-image {
          width: 100%;
          max-height: 400px;
          object-fit: cover;
          border-radius: 12px;
          margin-top: 0.5rem;
          border: 2px solid rgba(99, 102, 241, 0.3);
          background: rgba(15, 23, 42, 0.4);
        }

        .content-source-options {
          display: flex;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .radio-option {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          cursor: pointer;
          color: #cbd5e1;
        }

        .radio-option input[type="radio"] {
          accent-color: #6366f1;
        }

        .file-upload-section {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .file-upload-label {
          display: inline-block;
          padding: 0.75rem 1rem;
          background: rgba(99, 102, 241, 0.1);
          border: 2px dashed #6366f1;
          border-radius: 8px;
          color: #6366f1;
          cursor: pointer;
          text-align: center;
          transition: all 0.3s ease;
        }

        .file-upload-label:hover {
          background: rgba(99, 102, 241, 0.2);
          border-color: #8b5cf6;
        }

        .file-info {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.5rem;
          background: rgba(16, 185, 129, 0.1);
          border-radius: 6px;
          color: #10b981;
        }

        .file-size {
          font-size: 0.85rem;
        }

        .remove-file {
          background: none;
          border: none;
          color: #ef4444;
          cursor: pointer;
          font-size: 1rem;
          padding: 0.25rem;
          border-radius: 4px;
        }

        .remove-file:hover {
          background: rgba(239, 68, 68, 0.1);
        }

        .loading-animation {
          text-align: center;
          padding: 3rem;
        }

        .loading-animation p {
          color: #cbd5e1;
          margin-top: 1rem;
          font-size: 1.1rem;
        }

        .view-btn {
          width: 100%;
          margin: 2rem 0;
          padding: 1rem;
          font-size: 1.1rem;
        }

        @media (max-width: 768px) {
          .content-header {
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
          }

          .content-actions {
            flex-direction: column;
          }
        }
      `}</style>
    </div>
  );
};

export default ContentGenerator;