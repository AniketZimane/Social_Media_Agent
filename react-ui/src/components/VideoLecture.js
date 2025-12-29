import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Play, Clock, Users, Star, BookOpen, Search } from 'lucide-react';

const VideoLecture = () => {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const videoLectures = [
    {
      id: 5,
      title: "How to Write a Blog Using an AI Social Media Agent",
      youtubeId: "L2LYqQuXS-M",
      duration: "09:00",
      instructor: "AI Content Creator",
      rating: 4.6,
      students: 1200,
      description: "Learn how AI-powered tools can help you write complete, SEO-optimized blog content in minutes. This tutorial covers content writing, keyword optimization, hashtag generation, and social media publishing automation.",
      thumbnail: "https://img.youtube.com/vi/L2LYqQuXS-M/maxresdefault.jpg",
      category: "AI Tutorial"
    },
    {
      id: 6,
      title: "Create the blog through voice command",
      youtubeId: "zg0EqZovvcU",
      duration: "1:30",
      instructor: "Aniket Zimane",
      rating: 4.8,
      students: 10,
      description: "Creating blog trhough voice command",
      thumbnail: "https://img.youtube.com/vi/zg0EqZovvcU/maxresdefault.jpg",
      category: "AI & Technology"
    },
    // {
    //   id: 1,
    //   title: "AI Content Creation Masterclass",
    //   youtubeId: "dQw4w9WgXcQ",
    //   duration: "45:30",
    //   instructor: "Sarah Johnson",
    //   rating: 4.8,
    //   students: 12500,
    //   description: "Learn advanced AI techniques for creating engaging content across all platforms.",
    //   thumbnail: "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
    //   category: "AI & Technology"
    // },
    // {
    //   id: 2,
    //   title: "How to Start Content Creation in 2025? 🚀",
    //   youtubeId: "hE9D6Rv2qbg",
    //   duration: "38:15",
    //   instructor: "Mike Chen",
    //   rating: 4.9,
    //   students: 8900,
    //   description: "Complete guide to building successful social media campaigns.",
    //   thumbnail: "https://img.youtube.com/vi/hE9D6Rv2qbg/maxresdefault.jpg",
    //   category: "Marketing"
    // },
    // {
    //   id: 3,
    //   title: "Content Writing Psychology",
    //   youtubeId: "y6120QOlsfU",
    //   duration: "52:20",
    //   instructor: "Emma Davis",
    //   rating: 4.7,
    //   students: 15200,
    //   description: "Understanding the psychology behind viral content creation.",
    //   thumbnail: "https://img.youtube.com/vi/y6120QOlsfU/maxresdefault.jpg",
    //   category: "Psychology"
    // },
    // {
    //   id: 4,
    //   title: "YouTube Algorithm Secrets",
    //   youtubeId: "kJQP7kiw5Fk",
    //   duration: "41:45",
    //   instructor: "Alex Rodriguez",
    //   rating: 4.6,
    //   students: 9800,
    //   description: "Crack the YouTube algorithm and grow your channel exponentially.",
    //   thumbnail: "https://img.youtube.com/vi/kJQP7kiw5Fk/maxresdefault.jpg",
    //   category: "YouTube"
    // }
    
  ];

  const filteredVideos = videoLectures.filter(video =>
    video.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    video.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleVideoSelect = (video) => {
    setSelectedVideo(video);
  };

  const closeVideo = () => {
    setSelectedVideo(null);
  };

  return (
    <div style={{
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '2rem'
    }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
        style={{
          textAlign: 'center',
          marginBottom: '2rem'
        }}
      >
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.75rem',
          marginBottom: '1rem'
        }}>
          <Play size={24} style={{ color: '#6366f1' }} />
          <h2 style={{
            fontSize: '1.75rem',
            fontWeight: '600',
            color: '#f1f5f9',
            margin: 0
          }}>Video Lectures</h2>
        </div>
        <p style={{ color: '#cbd5e1', fontSize: '1.1rem', marginBottom: '2rem' }}>
          Master content creation with expert-led video courses
        </p>
        
        <div style={{
          display: 'flex',
          alignItems: 'center',
          maxWidth: '400px',
          margin: '0 auto',
          background: 'rgba(15, 23, 42, 0.6)',
          border: '2px solid rgba(99, 102, 241, 0.2)',
          borderRadius: '16px',
          padding: '1rem',
          backdropFilter: 'blur(10px)'
        }}>
          <Search size={20} style={{ color: '#6366f1' }} />
          <input
            type="text"
            placeholder="Search lectures..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              border: 'none',
              outline: 'none',
              marginLeft: '12px',
              flex: 1,
              fontSize: '16px',
              backgroundColor: 'transparent',
              color: '#e2e8f0'
            }}
          />
        </div>
      </motion.div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        {filteredVideos.map((video, index) => (
          <motion.div
            key={video.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -8, scale: 1.02 }}
            onClick={() => handleVideoSelect(video)}
            className="card"
            style={{
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              padding: 0,
              overflow: 'hidden'
            }}
          >
            <div style={{
              position: 'relative',
              width: '100%',
              height: '200px',
              overflow: 'hidden'
            }}>
              <img 
                src={video.thumbnail} 
                alt={video.title}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover'
                }}
              />
              <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                borderRadius: '50%',
                padding: '16px',
                color: 'white',
                opacity: 0,
                transition: 'opacity 0.3s ease',
                boxShadow: '0 8px 25px rgba(99, 102, 241, 0.4)'
              }} className="play-overlay">
                <Play size={32} fill="white" />
              </div>
              <div style={{
                position: 'absolute',
                bottom: '12px',
                right: '12px',
                background: 'rgba(0,0,0,0.8)',
                color: 'white',
                padding: '6px 12px',
                borderRadius: '20px',
                fontSize: '12px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                backdropFilter: 'blur(10px)'
              }}>
                <Clock size={12} />
                {video.duration}
              </div>
            </div>
            
            <div style={{ padding: '1.5rem' }}>
              <h3 style={{
                fontSize: '1.25rem',
                marginBottom: '8px',
                color: '#f1f5f9',
                fontWeight: '600',
                lineHeight: '1.4'
              }}>{video.title}</h3>
              <p style={{
                color: '#6366f1',
                fontSize: '14px',
                marginBottom: '12px',
                fontWeight: '500'
              }}>by {video.instructor}</p>
              <p style={{
                color: '#cbd5e1',
                fontSize: '14px',
                lineHeight: '1.5',
                marginBottom: '16px'
              }}>{video.description}</p>
              
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontSize: '14px',
                color: '#94a3b8',
                paddingTop: '16px',
                borderTop: '1px solid rgba(99, 102, 241, 0.2)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#f59e0b' }}>
                  <Star size={16} fill="#f59e0b" />
                  {video.rating}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <Users size={16} />
                  {video.students.toLocaleString()}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <BookOpen size={16} />
                  {video.category}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {selectedVideo && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={closeVideo}
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
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            onClick={(e) => e.stopPropagation()}
            className="card"
            style={{
              maxWidth: '800px',
              width: '90%',
              position: 'relative'
            }}
          >
            <button 
              onClick={closeVideo}
              style={{
                position: 'absolute',
                top: '16px',
                right: '20px',
                background: 'rgba(99, 102, 241, 0.1)',
                border: '2px solid rgba(99, 102, 241, 0.3)',
                fontSize: '24px',
                cursor: 'pointer',
                color: '#6366f1',
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backdropFilter: 'blur(10px)'
              }}
            >×</button>
            <iframe
              width="100%"
              height="400"
              src={`https://www.youtube.com/embed/${selectedVideo.youtubeId}?autoplay=1`}
              title={selectedVideo.title}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              style={{ borderRadius: '12px' }}
            ></iframe>
            <div style={{ 
              marginTop: '20px', 
              paddingTop: '20px', 
              borderTop: '1px solid rgba(99, 102, 241, 0.2)' 
            }}>
              <h3 style={{ 
                fontSize: '1.5rem', 
                marginBottom: '8px', 
                color: '#f1f5f9' 
              }}>{selectedVideo.title}</h3>
              <p style={{ 
                color: '#6366f1', 
                marginBottom: '12px' 
              }}>Instructor: {selectedVideo.instructor}</p>
              <p style={{ 
                color: '#cbd5e1', 
                lineHeight: '1.6' 
              }}>{selectedVideo.description}</p>
            </div>
          </motion.div>
        </motion.div>
      )}

      <style>{`
        .play-overlay {
          opacity: 0 !important;
        }
        .card:hover .play-overlay {
          opacity: 1 !important;
        }
      `}</style>
    </div>
  );
};

export default VideoLecture;