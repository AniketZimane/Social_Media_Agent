import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, Calendar, CheckCircle, XCircle, Clock } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard = ({ postingHistory }) => {
  const totalPosts = postingHistory.length;
  const postedCount = postingHistory.filter(p => p.status === 'posted').length;
  const failedCount = postingHistory.filter(p => p.status === 'failed').length;
  const scheduledCount = postingHistory.filter(p => p.status === 'scheduled').length;
  const successRate = totalPosts > 0 ? (postedCount / totalPosts * 100).toFixed(0) : 0;

  const platformData = [
    { name: 'Facebook', posts: 12, success: 11 },
    { name: 'Twitter', posts: 15, success: 14 },
    { name: 'LinkedIn', posts: 8, success: 3 },
    { name: 'Instagram', posts: 10, success: 9 }
  ];

  const statusData = [
    { name: 'Posted', value: postedCount, color: '#10b981' },
    { name: 'Failed', value: failedCount, color: '#ef4444' },
    { name: 'Scheduled', value: scheduledCount, color: '#f59e0b' }
  ];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'posted': return <CheckCircle size={16} className="status-icon success" />;
      case 'failed': return <XCircle size={16} className="status-icon error" />;
      case 'scheduled': return <Clock size={16} className="status-icon pending" />;
      default: return null;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'posted': return '#10b981';
      case 'failed': return '#ef4444';
      case 'scheduled': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  return (
    <div className="dashboard">
      <motion.div 
        className="card"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
      >
        <div className="section-header">
          <BarChart3 className="section-icon" />
          <h2>Analytics Dashboard</h2>
        </div>

        <div className="metrics-grid">
          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.02 }}
          >
            <div className="metric-icon total">
              <Calendar size={24} />
            </div>
            <div className="metric-content">
              <h3>{totalPosts}</h3>
              <p>Total Posts</p>
            </div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.02 }}
          >
            <div className="metric-icon success">
              <CheckCircle size={24} />
            </div>
            <div className="metric-content">
              <h3>{postedCount}</h3>
              <p>Posted</p>
            </div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.02 }}
          >
            <div className="metric-icon error">
              <XCircle size={24} />
            </div>
            <div className="metric-content">
              <h3>{failedCount}</h3>
              <p>Failed</p>
            </div>
          </motion.div>

          <motion.div 
            className="metric-card"
            whileHover={{ scale: 1.02 }}
          >
            <div className="metric-icon trending">
              <TrendingUp size={24} />
            </div>
            <div className="metric-content">
              <h3>{successRate}%</h3>
              <p>Success Rate</p>
            </div>
          </motion.div>
        </div>

        <div className="charts-section">
          <div className="chart-container">
            <h3>📊 Platform Performance</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={platformData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="posts" fill="#667eea" name="Total Posts" />
                <Bar dataKey="success" fill="#10b981" name="Successful Posts" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-container">
            <h3>📈 Status Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {postingHistory.length > 0 && (
          <div className="recent-posts">
            <h3>📋 Recent Posts</h3>
            <div className="posts-list">
              {postingHistory.slice(-5).reverse().map(post => (
                <motion.div
                  key={post.id}
                  className="post-item"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="post-header">
                    <div className="post-title">
                      {getStatusIcon(post.status)}
                      <span>{post.title.substring(0, 50)}...</span>
                    </div>
                    <div 
                      className="post-status"
                      style={{ 
                        background: getStatusColor(post.status) + '20',
                        color: getStatusColor(post.status)
                      }}
                    >
                      {post.status.toUpperCase()}
                    </div>
                  </div>
                  
                  <div className="post-meta">
                    <span>Platforms: {post.platforms.join(', ')}</span>
                    <span>Scheduled: {post.scheduledTime.toLocaleString()}</span>
                  </div>

                  {post.results && (
                    <div className="post-results">
                      {post.results.map((result, index) => (
                        <div key={index} className="result-item">
                          {result.success ? '✅' : '❌'} {result.platform}: {result.message}
                        </div>
                      ))}
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {postingHistory.length === 0 && (
          <div className="no-data">
            <p>📊 No posting history yet. Schedule some posts to see analytics!</p>
          </div>
        )}
      </motion.div>

      <style jsx>{`
        .dashboard {
          max-width: 1000px;
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

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1.5rem;
          margin-bottom: 3rem;
        }

        .metric-card {
          background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
          border-radius: 16px;
          padding: 1.5rem;
          display: flex;
          align-items: center;
          gap: 1rem;
          border: 1px solid #e5e7eb;
          transition: all 0.3s ease;
        }

        .metric-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        .metric-icon {
          width: 50px;
          height: 50px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
        }

        .metric-icon.total { background: linear-gradient(135deg, #667eea, #764ba2); }
        .metric-icon.success { background: linear-gradient(135deg, #10b981, #059669); }
        .metric-icon.error { background: linear-gradient(135deg, #ef4444, #dc2626); }
        .metric-icon.trending { background: linear-gradient(135deg, #f59e0b, #d97706); }

        .metric-content h3 {
          font-size: 2rem;
          font-weight: 700;
          color: #1f2937;
          margin: 0;
        }

        .metric-content p {
          color: #6b7280;
          margin: 0;
          font-weight: 500;
        }

        .charts-section {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
          margin-bottom: 3rem;
        }

        .chart-container {
          background: #f9fafb;
          border-radius: 16px;
          padding: 1.5rem;
        }

        .chart-container h3 {
          color: #1f2937;
          margin-bottom: 1rem;
          font-size: 1.1rem;
        }

        .recent-posts {
          margin-top: 2rem;
        }

        .recent-posts h3 {
          color: #1f2937;
          margin-bottom: 1.5rem;
          font-size: 1.25rem;
        }

        .posts-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .post-item {
          background: #f9fafb;
          border-radius: 12px;
          padding: 1.5rem;
          border-left: 4px solid #667eea;
        }

        .post-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }

        .post-title {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 500;
          color: #1f2937;
        }

        .post-status {
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 600;
        }

        .post-meta {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          color: #6b7280;
          font-size: 0.9rem;
          margin-bottom: 1rem;
        }

        .post-results {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          font-size: 0.9rem;
        }

        .result-item {
          color: #4b5563;
        }

        .status-icon.success { color: #10b981; }
        .status-icon.error { color: #ef4444; }
        .status-icon.pending { color: #f59e0b; }

        .no-data {
          text-align: center;
          padding: 3rem;
          color: #6b7280;
          font-size: 1.1rem;
        }

        @media (max-width: 768px) {
          .charts-section {
            grid-template-columns: 1fr;
          }

          .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
          }

          .post-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default Dashboard;