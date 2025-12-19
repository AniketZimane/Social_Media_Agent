import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Target } from 'lucide-react';

const BlogPreview = ({ blogContent, onBack, formatContent }) => {
  return (
    <motion.div
      className="blog-preview-page"
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.5 }}
    >
      <button className="back-button" onClick={onBack}>
        <ArrowLeft size={20} /> Back to Generator
      </button>

      <div className="preview-header">
        <h1>{blogContent.title}</h1>
        <div className="engagement-badge">
          <Target size={16} />
          {(blogContent.engagement_score * 100).toFixed(0)}% Engagement
        </div>
      </div>

      {blogContent.image_url && (
        <img src={blogContent.image_url} alt={blogContent.title} className="preview-image" />
      )}

      <div className="preview-content" dangerouslySetInnerHTML={{ __html: formatContent(blogContent.content) }} />

      <div className="preview-meta">
        <div className="meta-section">
          <h3>🏷️ Hashtags</h3>
          <p>{blogContent.hashtags.join(' ')}</p>
        </div>
        <div className="meta-section">
          <h3>💯 Call to Action</h3>
          <p>{blogContent.cta}</p>
        </div>
      </div>

      <style jsx>{`
        .blog-preview-page {
          max-width: 900px;
          margin: 0 auto;
          padding: 2rem;
        }
        .back-button {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: rgba(99, 102, 241, 0.1);
          border: 1px solid #6366f1;
          color: #6366f1;
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          cursor: pointer;
          margin-bottom: 2rem;
        }
        .preview-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
        }
        .preview-header h1 {
          color: #f1f5f9;
          font-size: 2rem;
        }
        .engagement-badge {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: #10b981;
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
        }
        .preview-image {
          width: 100%;
          border-radius: 12px;
          margin-bottom: 2rem;
        }
        .preview-content {
          color: #cbd5e1;
          line-height: 1.8;
          font-size: 1.1rem;
        }
        .preview-meta {
          margin-top: 3rem;
          padding-top: 2rem;
          border-top: 2px solid rgba(99, 102, 241, 0.3);
        }
        .meta-section {
          margin-bottom: 1.5rem;
        }
        .meta-section h3 {
          color: #6366f1;
          margin-bottom: 0.5rem;
        }
        .meta-section p {
          color: #cbd5e1;
        }
      `}</style>
    </motion.div>
  );
};

export default BlogPreview;
