import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Shield, Link, Award, TrendingUp, ExternalLink, Copy, Check } from 'lucide-react';

const BlockchainDashboard = ({ blogContent }) => {
  const [blockchainData, setBlockchainData] = useState(null);
  const [creatorStats, setCreatorStats] = useState(null);
  const [copied, setCopied] = useState('');
  const [verificationStatus, setVerificationStatus] = useState('pending');

  useEffect(() => {
    if (blogContent?.blockchain) {
      setBlockchainData(blogContent.blockchain);
      fetchCreatorStats();
    }
  }, [blogContent]);

  const fetchCreatorStats = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/blockchain/creator-stats');
      if (response.ok) {
        const data = await response.json();
        setCreatorStats(data.stats);
      }
    } catch (error) {
      console.error('Failed to fetch creator stats:', error);
    }
  };

  const verifyContent = async () => {
    if (!blockchainData?.content_hash) return;
    
    setVerificationStatus('verifying');
    try {
      const response = await fetch('http://localhost:5000/api/blockchain/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content_hash: blockchainData.content_hash })
      });
      
      if (response.ok) {
        setVerificationStatus('verified');
      } else {
        setVerificationStatus('failed');
      }
    } catch (error) {
      setVerificationStatus('failed');
    }
  };

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text);
    setCopied(type);
    setTimeout(() => setCopied(''), 2000);
  };

  if (!blockchainData) {
    return (
      <div className="blockchain-dashboard">
        <div className="no-blockchain">
          <Shield size={48} color="#6366f1" />
          <h3>Blockchain Integration</h3>
          <p>Generate content to see blockchain features</p>
        </div>
      </div>
    );
  }

  return (
    <div className="blockchain-dashboard">
      <motion.div 
        className="blockchain-header"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="header-content">
          <Shield size={32} color="#10b981" />
          <div>
            <h2>🔗 Blockchain Verified Content</h2>
            <p>Your content is secured on the blockchain with NFT ownership</p>
          </div>
          <div className="verification-badge">
            {blockchainData.verified ? (
              <span className="verified">✅ Verified</span>
            ) : (
              <span className="unverified">⚠️ Pending</span>
            )}
          </div>
        </div>
      </motion.div>

      <div className="blockchain-grid">
        {/* Content Ownership */}
        <motion.div 
          className="blockchain-card"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
        >
          <div className="card-header">
            <Award size={24} color="#f59e0b" />
            <h3>Content Ownership</h3>
          </div>
          <div className="card-content">
            <div className="info-row">
              <span>Content Hash:</span>
              <div className="hash-display">
                <code>{blockchainData.content_hash?.substring(0, 16)}...</code>
                <button 
                  onClick={() => copyToClipboard(blockchainData.content_hash, 'hash')}
                  className="copy-btn"
                >
                  {copied === 'hash' ? <Check size={16} /> : <Copy size={16} />}
                </button>
              </div>
            </div>
            <div className="info-row">
              <span>Owner:</span>
              <span>Aniket Zimane</span>
            </div>
            <div className="info-row">
              <span>License:</span>
              <span>CC BY-SA 4.0</span>
            </div>
            <div className="info-row">
              <span>Blockchain:</span>
              <span>Polygon Network</span>
            </div>
          </div>
        </motion.div>

        {/* NFT Information */}
        <motion.div 
          className="blockchain-card"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="card-header">
            <TrendingUp size={24} color="#8b5cf6" />
            <h3>NFT Details</h3>
          </div>
          <div className="card-content">
            <div className="info-row">
              <span>Token ID:</span>
              <span>#{blockchainData.nft?.token_id || '1001'}</span>
            </div>
            <div className="info-row">
              <span>Contract:</span>
              <div className="hash-display">
                <code>0x742d...4d8b6</code>
                <button 
                  onClick={() => copyToClipboard(blockchainData.nft?.contract_address, 'contract')}
                  className="copy-btn"
                >
                  {copied === 'contract' ? <Check size={16} /> : <Copy size={16} />}
                </button>
              </div>
            </div>
            <div className="info-row">
              <span>Royalty:</span>
              <span>10%</span>
            </div>
            <div className="info-row">
              <span>Estimated Value:</span>
              <span>0.05 MATIC</span>
            </div>
          </div>
        </motion.div>

        {/* IPFS Storage */}
        <motion.div 
          className="blockchain-card"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="card-header">
            <Link size={24} color="#06b6d4" />
            <h3>Decentralized Storage</h3>
          </div>
          <div className="card-content">
            <div className="info-row">
              <span>IPFS Hash:</span>
              <div className="hash-display">
                <code>{blockchainData.ipfs_hash?.substring(0, 16)}...</code>
                <button 
                  onClick={() => copyToClipboard(blockchainData.ipfs_hash, 'ipfs')}
                  className="copy-btn"
                >
                  {copied === 'ipfs' ? <Check size={16} /> : <Copy size={16} />}
                </button>
              </div>
            </div>
            <div className="info-row">
              <span>Storage:</span>
              <span>IPFS Network</span>
            </div>
            <div className="info-row">
              <span>Accessibility:</span>
              <span>Permanent</span>
            </div>
            <div className="action-row">
              <a 
                href={blockchainData.ipfs_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="ipfs-link"
              >
                <ExternalLink size={16} />
                View on IPFS
              </a>
            </div>
          </div>
        </motion.div>

        {/* Creator Statistics */}
        {creatorStats && (
          <motion.div 
            className="blockchain-card creator-stats"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <div className="card-header">
              <Award size={24} color="#10b981" />
              <h3>Creator Analytics</h3>
            </div>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-value">{creatorStats.total_content_pieces}</span>
                <span className="stat-label">Content Pieces</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">{creatorStats.total_words_written?.toLocaleString()}</span>
                <span className="stat-label">Words Written</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">{(creatorStats.average_engagement * 100).toFixed(0)}%</span>
                <span className="stat-label">Avg Engagement</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">{creatorStats.blockchain_reputation}</span>
                <span className="stat-label">Reputation Score</span>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="blockchain-actions">
        <button 
          onClick={verifyContent}
          className={`verify-btn ${verificationStatus}`}
          disabled={verificationStatus === 'verifying'}
        >
          <Shield size={16} />
          {verificationStatus === 'verifying' ? 'Verifying...' : 
           verificationStatus === 'verified' ? 'Verified ✓' : 
           'Verify Content'}
        </button>

        <a 
          href={blockchainData.nft_marketplace_url || '#'} 
          target="_blank" 
          rel="noopener noreferrer"
          className="marketplace-btn"
        >
          <ExternalLink size={16} />
          View on OpenSea
        </a>

        <a 
          href={blockchainData.blockchain_explorer_url || '#'} 
          target="_blank" 
          rel="noopener noreferrer"
          className="explorer-btn"
        >
          <ExternalLink size={16} />
          Blockchain Explorer
        </a>
      </div>

      <style>{`
        .blockchain-dashboard {
          max-width: 1200px;
          margin: 2rem auto;
          padding: 0 1rem;
        }

        .blockchain-header {
          background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
          border: 1px solid rgba(16, 185, 129, 0.2);
          border-radius: 16px;
          padding: 2rem;
          margin-bottom: 2rem;
        }

        .header-content {
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .header-content h2 {
          color: #f1f5f9;
          margin: 0;
          font-size: 1.5rem;
        }

        .header-content p {
          color: #cbd5e1;
          margin: 0.5rem 0 0 0;
        }

        .verification-badge {
          margin-left: auto;
        }

        .verified {
          background: #10b981;
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 600;
        }

        .unverified {
          background: #f59e0b;
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 600;
        }

        .blockchain-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }

        .blockchain-card {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 16px;
          padding: 1.5rem;
          backdrop-filter: blur(10px);
        }

        .card-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1.5rem;
        }

        .card-header h3 {
          color: #f1f5f9;
          margin: 0;
          font-size: 1.1rem;
        }

        .card-content {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .info-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.5rem 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .info-row:last-child {
          border-bottom: none;
        }

        .info-row span:first-child {
          color: #94a3b8;
          font-size: 0.9rem;
        }

        .info-row span:last-child {
          color: #f1f5f9;
          font-weight: 500;
        }

        .hash-display {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .hash-display code {
          background: rgba(99, 102, 241, 0.2);
          color: #a5b4fc;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.8rem;
        }

        .copy-btn {
          background: none;
          border: none;
          color: #94a3b8;
          cursor: pointer;
          padding: 0.25rem;
          border-radius: 4px;
          transition: color 0.2s;
        }

        .copy-btn:hover {
          color: #f1f5f9;
        }

        .action-row {
          margin-top: 0.5rem;
        }

        .ipfs-link {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          color: #06b6d4;
          text-decoration: none;
          font-size: 0.9rem;
          transition: color 0.2s;
        }

        .ipfs-link:hover {
          color: #0891b2;
        }

        .creator-stats {
          grid-column: 1 / -1;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 1rem;
        }

        .stat-item {
          text-align: center;
          padding: 1rem;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 12px;
        }

        .stat-value {
          display: block;
          font-size: 1.5rem;
          font-weight: 700;
          color: #10b981;
          margin-bottom: 0.5rem;
        }

        .stat-label {
          color: #94a3b8;
          font-size: 0.9rem;
        }

        .blockchain-actions {
          display: flex;
          gap: 1rem;
          justify-content: center;
          flex-wrap: wrap;
        }

        .verify-btn, .marketplace-btn, .explorer-btn {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.5rem;
          border-radius: 12px;
          text-decoration: none;
          font-weight: 500;
          transition: all 0.3s ease;
          border: none;
          cursor: pointer;
        }

        .verify-btn {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
        }

        .verify-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        }

        .verify-btn.verifying {
          opacity: 0.7;
          cursor: not-allowed;
        }

        .verify-btn.verified {
          background: linear-gradient(135deg, #059669 0%, #047857 100%);
        }

        .marketplace-btn {
          background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
          color: white;
        }

        .marketplace-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
        }

        .explorer-btn {
          background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
          color: white;
        }

        .explorer-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(6, 182, 212, 0.3);
        }

        .no-blockchain {
          text-align: center;
          padding: 3rem;
          color: #94a3b8;
        }

        .no-blockchain h3 {
          color: #f1f5f9;
          margin: 1rem 0 0.5rem 0;
        }

        @media (max-width: 768px) {
          .blockchain-grid {
            grid-template-columns: 1fr;
          }
          
          .blockchain-actions {
            flex-direction: column;
            align-items: center;
          }
          
          .verify-btn, .marketplace-btn, .explorer-btn {
            width: 100%;
            max-width: 300px;
            justify-content: center;
          }
        }
      `}</style>
    </div>
  );
};

export default BlockchainDashboard;