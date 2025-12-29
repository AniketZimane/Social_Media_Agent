import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Clock, Send, Trash2, CheckCircle, AlertCircle, Settings } from 'lucide-react';

const ScheduledPosts = ({ blogContent }) => {
  const [scheduledPosts, setScheduledPosts] = useState([]);
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [selectedPlatforms, setSelectedPlatforms] = useState([]);
  const [scheduledDateTime, setScheduledDateTime] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const platforms = [
    { id: 'linkedin', name: '💼 LinkedIn', color: '#0077b5' },
    { id: 'twitter', name: '🐦 Twitter', color: '#1da1f2' },
    { id: 'facebook', name: '👥 Facebook', color: '#4267b2' },
    { id: 'instagram', name: '📸 Instagram', color: '#e4405f' },
    { id: 'youtube', name: '📺 YouTube', color: '#ff0000' }
  ];

  useEffect(() => {
    fetchScheduledPosts();
    // Refresh every 30 seconds
    const interval = setInterval(fetchScheduledPosts, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchScheduledPosts = async () => {
    try {
      const response = await fetch('http://localhost:5003/api/scheduled-posts');
      if (response.ok) {
        const data = await response.json();
        setScheduledPosts(data.posts || []);
      }
    } catch (error) {
      console.error('Error fetching scheduled posts:', error);
    }
  };

  const schedulePost = async () => {
    if (!blogContent || selectedPlatforms.length === 0 || !scheduledDateTime) {
      alert('Please select platforms and set a schedule time');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5003/api/schedule-post', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: blogContent.title || 'Untitled Post',
          content: blogContent.content || '',
          hashtags: blogContent.hashtags || [],
          platforms: selectedPlatforms,
          scheduled_time: scheduledDateTime,
          image_url: blogContent.image_url || ''
        })
      });

      const result = await response.json();
      
      if (result.success) {
        setShowScheduleModal(false);
        setSelectedPlatforms([]);
        setScheduledDateTime('');
        fetchScheduledPosts();
        alert('Post scheduled successfully!');
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      console.error('Error scheduling post:', error);
      alert('Network error - please check if the scheduler service is running');
    } finally {
      setIsLoading(false);
    }
  };

  const postNow = async () => {
    if (!blogContent || selectedPlatforms.length === 0) {
      alert('Please select platforms');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5003/api/post-now', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: blogContent.title,
          content: blogContent.content,
          hashtags: blogContent.hashtags || [],
          platforms: selectedPlatforms,
          image_url: blogContent.image_url || ''
        })
      });

      if (response.ok) {
        const data = await response.json();
        alert('Posted successfully to selected platforms!');
        setSelectedPlatforms([]);
      }
    } catch (error) {
      console.error('Error posting now:', error);
      alert('Error posting to platforms');
    } finally {
      setIsLoading(false);
    }
  };

  const deleteScheduledPost = async (postId) => {
    try {
      const response = await fetch(`http://localhost:5003/api/scheduled-posts/${postId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        fetchScheduledPosts();
      }
    } catch (error) {
      console.error('Error deleting post:', error);
    }
  };

  const getMinDateTime = () => {
    const now = new Date();
    now.setMinutes(now.getMinutes() + 5); // Minimum 5 minutes from now
    return now.toISOString().slice(0, 16);
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
        style={{ marginBottom: '2rem' }}
      >
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '2rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Calendar size={24} style={{ color: '#6366f1' }} />
            <h2 style={{
              fontSize: '1.75rem',
              fontWeight: '600',
              color: '#f1f5f9',
              margin: 0
            }}>Scheduled Posts</h2>
          </div>
          
          {blogContent && (
            <div style={{ display: 'flex', gap: '1rem' }}>
              <button
                className="button-secondary"
                onClick={() => setShowScheduleModal(true)}
                disabled={isLoading}
              >
                <Calendar size={16} />
                Schedule Post
              </button>
              <button
                className="button-primary"
                onClick={postNow}
                disabled={isLoading || selectedPlatforms.length === 0}
              >
                <Send size={16} />
                Post Now
              </button>
            </div>
          )}
        </div>

        {/* Platform Selection */}
        {blogContent && (
          <div style={{ marginBottom: '2rem' }}>
            <h3 style={{ color: '#f1f5f9', marginBottom: '1rem' }}>Select Platforms:</h3>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {platforms.map(platform => (
                <label
                  key={platform.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    padding: '0.75rem 1rem',
                    background: selectedPlatforms.includes(platform.id) 
                      ? 'rgba(99, 102, 241, 0.2)' 
                      : 'rgba(15, 23, 42, 0.6)',
                    border: selectedPlatforms.includes(platform.id)
                      ? '2px solid #6366f1'
                      : '2px solid rgba(99, 102, 241, 0.2)',
                    borderRadius: '12px',
                    cursor: 'pointer',
                    color: '#f1f5f9',
                    transition: 'all 0.3s ease'
                  }}
                >
                  <input
                    type="checkbox"
                    checked={selectedPlatforms.includes(platform.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedPlatforms([...selectedPlatforms, platform.id]);
                      } else {
                        setSelectedPlatforms(selectedPlatforms.filter(p => p !== platform.id));
                      }
                    }}
                    style={{ accentColor: '#6366f1' }}
                  />
                  {platform.name}
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Scheduled Posts List */}
        <div>
          <h3 style={{ color: '#f1f5f9', marginBottom: '1rem' }}>
            Upcoming Posts ({scheduledPosts.filter(p => p.status === 'scheduled').length})
          </h3>
          
          {scheduledPosts.length === 0 ? (
            <div style={{
              textAlign: 'center',
              padding: '3rem',
              color: '#94a3b8'
            }}>
              <Calendar size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
              <p>No scheduled posts yet</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gap: '1rem' }}>
              {scheduledPosts.map(post => (
                <motion.div
                  key={post.id}
                  className="card"
                  style={{
                    background: 'rgba(15, 23, 42, 0.4)',
                    border: '1px solid rgba(99, 102, 241, 0.2)',
                    padding: '1.5rem'
                  }}
                  whileHover={{ scale: 1.01 }}
                >
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    marginBottom: '1rem'
                  }}>
                    <div style={{ flex: 1 }}>
                      <h4 style={{
                        color: '#f1f5f9',
                        fontSize: '1.1rem',
                        marginBottom: '0.5rem'
                      }}>{post.title}</h4>
                      
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '1rem',
                        marginBottom: '0.5rem',
                        fontSize: '14px',
                        color: '#94a3b8'
                      }}>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                          <Clock size={14} />
                          {new Date(post.scheduled_time).toLocaleString()}
                        </span>
                        <span style={{
                          padding: '0.25rem 0.75rem',
                          borderRadius: '12px',
                          background: post.status === 'scheduled' 
                            ? 'rgba(59, 130, 246, 0.2)' 
                            : 'rgba(16, 185, 129, 0.2)',
                          color: post.status === 'scheduled' ? '#3b82f6' : '#10b981',
                          fontSize: '12px'
                        }}>
                          {post.status === 'scheduled' ? 'Scheduled' : 'Posted'}
                        </span>
                      </div>
                      
                      <div style={{
                        display: 'flex',
                        gap: '0.5rem',
                        flexWrap: 'wrap'
                      }}>
                        {post.platforms.map(platform => (
                          <span
                            key={platform}
                            style={{
                              padding: '0.25rem 0.5rem',
                              background: 'rgba(99, 102, 241, 0.1)',
                              color: '#6366f1',
                              borderRadius: '8px',
                              fontSize: '12px'
                            }}
                          >
                            {platforms.find(p => p.id === platform)?.name || platform}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    {post.status === 'scheduled' && (
                      <button
                        onClick={() => deleteScheduledPost(post.id)}
                        style={{
                          background: 'rgba(239, 68, 68, 0.1)',
                          border: '1px solid rgba(239, 68, 68, 0.3)',
                          color: '#ef4444',
                          padding: '0.5rem',
                          borderRadius: '8px',
                          cursor: 'pointer'
                        }}
                      >
                        <Trash2 size={16} />
                      </button>
                    )}
                  </div>
                  
                  <p style={{
                    color: '#cbd5e1',
                    fontSize: '14px',
                    lineHeight: '1.5',
                    margin: 0
                  }}>
                    {post.content.substring(0, 150)}...
                  </p>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </motion.div>

      {/* Schedule Modal */}
      {showScheduleModal && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="modal-overlay"
          onClick={() => setShowScheduleModal(false)}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            background: 'rgba(0,0,0,0.8)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000
          }}
        >
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            className="card"
            onClick={(e) => e.stopPropagation()}
            style={{
              maxWidth: '500px',
              width: '90%',
              position: 'relative'
            }}
          >
            <h3 style={{ color: '#f1f5f9', marginBottom: '1.5rem' }}>Schedule Post</h3>
            
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ color: '#cbd5e1', display: 'block', marginBottom: '0.5rem' }}>
                Select Date & Time:
              </label>
              <input
                type="datetime-local"
                value={scheduledDateTime}
                onChange={(e) => setScheduledDateTime(e.target.value)}
                min={getMinDateTime()}
                className="input-field"
                style={{ width: '100%' }}
              />
            </div>
            
            <div style={{ marginBottom: '2rem' }}>
              <label style={{ color: '#cbd5e1', display: 'block', marginBottom: '0.5rem' }}>
                Select Platforms:
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                {platforms.map(platform => (
                  <label
                    key={platform.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      padding: '0.5rem',
                      background: selectedPlatforms.includes(platform.id) 
                        ? 'rgba(99, 102, 241, 0.2)' 
                        : 'rgba(15, 23, 42, 0.6)',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      color: '#f1f5f9'
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={selectedPlatforms.includes(platform.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedPlatforms([...selectedPlatforms, platform.id]);
                        } else {
                          setSelectedPlatforms(selectedPlatforms.filter(p => p !== platform.id));
                        }
                      }}
                      style={{ accentColor: '#6366f1' }}
                    />
                    {platform.name}
                  </label>
                ))}
              </div>
            </div>
            
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
              <button
                className="button-secondary"
                onClick={() => setShowScheduleModal(false)}
              >
                Cancel
              </button>
              <button
                className="button-primary"
                onClick={schedulePost}
                disabled={isLoading || selectedPlatforms.length === 0 || !scheduledDateTime}
              >
                {isLoading ? 'Scheduling...' : 'Schedule Post'}
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
};

export default ScheduledPosts;