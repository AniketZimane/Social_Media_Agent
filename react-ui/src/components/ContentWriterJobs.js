import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Briefcase, MapPin, Clock, DollarSign, Users, Star, Filter, Search, ExternalLink, Mail, X, Send } from 'lucide-react';

const ContentWriterJobs = () => {
  const [selectedJob, setSelectedJob] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [showApplicationModal, setShowApplicationModal] = useState(false);
  const [applicantEmail, setApplicantEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const jobs = [
    {
      id: 1,
      title: "Senior Content Writer - AI & Tech",
      company: "TechFlow Inc.",
      location: "Remote",
      type: "Full-time",
      salary: "$75,000 - $95,000",
      experience: "3-5 years",
      rating: 4.8,
      employees: "500-1000",
      description: "Create compelling content for AI and technology products. Work with cutting-edge AI tools to produce high-quality blog posts, whitepapers, and marketing materials.",
      requirements: [
        "3+ years of content writing experience",
        "Strong understanding of AI and technology",
        "Experience with SEO optimization",
        "Excellent research skills"
      ],
      benefits: [
        "Remote work flexibility",
        "Health insurance",
        "401k matching",
        "Professional development budget"
      ],
      posted: "2 days ago",
      applicants: 45,
      logo: "https://via.placeholder.com/60x60/6366f1/white?text=TF"
    },
    {
      id: 2,
      title: "Social Media Content Creator",
      company: "Digital Spark Agency",
      location: "New York, NY",
      type: "Contract",
      salary: "$50 - $75/hour",
      experience: "2-4 years",
      rating: 4.6,
      employees: "50-200",
      description: "Create engaging social media content for multiple clients across various industries. Focus on Instagram, LinkedIn, and TikTok content creation.",
      requirements: [
        "2+ years social media experience",
        "Portfolio of successful campaigns",
        "Knowledge of social media trends",
        "Video editing skills preferred"
      ],
      benefits: [
        "Flexible schedule",
        "Creative freedom",
        "Performance bonuses",
        "Networking opportunities"
      ],
      posted: "1 day ago",
      applicants: 32,
      logo: "https://via.placeholder.com/60x60/8b5cf6/white?text=DS"
    },
    {
      id: 3,
      title: "Blog Writer - Marketing & Business",
      company: "Growth Masters",
      location: "San Francisco, CA",
      type: "Part-time",
      salary: "$40,000 - $55,000",
      experience: "1-3 years",
      rating: 4.7,
      employees: "100-500",
      description: "Write informative blog posts about marketing strategies, business growth, and entrepreneurship. Collaborate with marketing team to create SEO-optimized content.",
      requirements: [
        "1+ years of blog writing experience",
        "Understanding of marketing principles",
        "SEO knowledge",
        "Ability to meet deadlines"
      ],
      benefits: [
        "Flexible hours",
        "Learning opportunities",
        "Team collaboration",
        "Growth potential"
      ],
      posted: "3 days ago",
      applicants: 28,
      logo: "https://via.placeholder.com/60x60/06b6d4/white?text=GM"
    },
    {
      id: 4,
      title: "Freelance Content Writer",
      company: "ContentHub Platform",
      location: "Remote",
      type: "Freelance",
      salary: "$25 - $50/hour",
      experience: "1-2 years",
      rating: 4.5,
      employees: "10-50",
      description: "Join our platform of freelance writers. Work on diverse projects including blog posts, articles, product descriptions, and marketing copy.",
      requirements: [
        "Strong writing portfolio",
        "Ability to adapt writing style",
        "Research skills",
        "Time management"
      ],
      benefits: [
        "Choose your projects",
        "Work from anywhere",
        "Weekly payments",
        "Skill development"
      ],
      posted: "5 days ago",
      applicants: 67,
      logo: "https://via.placeholder.com/60x60/10b981/white?text=CH"
    }
  ];

  const filteredJobs = jobs.filter(job => {
    const matchesSearch = job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         job.company.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || job.type.toLowerCase() === filterType.toLowerCase();
    return matchesSearch && matchesFilter;
  });

  const handleJobSelect = (job) => {
    setSelectedJob(job);
  };

  const closeJobDetails = () => {
    setSelectedJob(null);
  };

  const handleApplyJob = () => {
    setShowApplicationModal(true);
  };

  const closeApplicationModal = () => {
    setShowApplicationModal(false);
    setApplicantEmail('');
  };

  const handleSubmitApplication = async () => {
    if (!applicantEmail.trim()) {
      alert('Please enter your email address');
      return;
    }

    setIsSubmitting(true);
    
    try {
      const response = await fetch('http://localhost:5001/api/send-application', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jobTitle: selectedJob.title,
          company: selectedJob.company,
          applicantEmail: applicantEmail,
          senderEmail: 'ad.developer1604@gmail.com'
        })
      });

      if (response.ok) {
        alert('Application submitted successfully! Check your email for confirmation.');
        closeApplicationModal();
      } else {
        alert('Failed to submit application. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting application:', error);
      alert('Please start the email service first by running start_job_service.bat');
    }
    
    setIsSubmitting(false);
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
          <Briefcase size={24} style={{ color: '#6366f1' }} />
          <h2 style={{
            fontSize: '1.75rem',
            fontWeight: '600',
            color: '#f1f5f9',
            margin: 0
          }}>Job Opportunity</h2>
        </div>
        <p style={{ color: '#cbd5e1', fontSize: '1.1rem', marginBottom: '2rem' }}>
          Find your dream content writing position
        </p>
        
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '1rem',
          flexWrap: 'wrap'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            background: 'rgba(15, 23, 42, 0.6)',
            border: '2px solid rgba(99, 102, 241, 0.2)',
            borderRadius: '16px',
            padding: '1rem',
            minWidth: '300px',
            backdropFilter: 'blur(10px)'
          }}>
            <Search size={20} style={{ color: '#6366f1' }} />
            <input
              type="text"
              placeholder="Search jobs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field"
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
          
          <div style={{
            display: 'flex',
            alignItems: 'center',
            background: 'rgba(15, 23, 42, 0.6)',
            border: '2px solid rgba(99, 102, 241, 0.2)',
            borderRadius: '16px',
            padding: '1rem',
            backdropFilter: 'blur(10px)'
          }}>
            <Filter size={20} style={{ color: '#6366f1' }} />
            <select 
              value={filterType} 
              onChange={(e) => setFilterType(e.target.value)}
              className="select-field"
              style={{
                border: 'none',
                outline: 'none',
                marginLeft: '12px',
                fontSize: '16px',
                backgroundColor: 'transparent',
                color: '#e2e8f0'
              }}
            >
              <option value="all">All Types</option>
              <option value="full-time">Full-time</option>
              <option value="part-time">Part-time</option>
              <option value="contract">Contract</option>
              <option value="freelance">Freelance</option>
            </select>
          </div>
        </div>
      </motion.div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        {filteredJobs.map((job, index) => (
          <motion.div
            key={job.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -8, scale: 1.02 }}
            onClick={() => handleJobSelect(job)}
            className="card"
            style={{
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '1rem',
              marginBottom: '1.5rem'
            }}>
              <img 
                src={job.logo} 
                alt={job.company} 
                style={{
                  width: '60px',
                  height: '60px',
                  borderRadius: '12px',
                  objectFit: 'cover',
                  boxShadow: '0 4px 15px rgba(99, 102, 241, 0.3)'
                }}
              />
              <div style={{ flex: 1 }}>
                <h3 style={{
                  fontSize: '1.25rem',
                  marginBottom: '6px',
                  color: '#f1f5f9',
                  fontWeight: '600',
                  lineHeight: '1.4'
                }}>{job.title}</h3>
                <p style={{
                  color: '#6366f1',
                  fontWeight: '500',
                  marginBottom: '12px',
                  fontSize: '15px'
                }}>{job.company}</p>
                <div style={{
                  display: 'flex',
                  gap: '16px',
                  fontSize: '14px',
                  color: '#94a3b8'
                }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <MapPin size={14} />
                    {job.location}
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Briefcase size={14} />
                    {job.type}
                  </span>
                </div>
              </div>
            </div>
            
            <div style={{
              display: 'flex',
              gap: '12px',
              marginBottom: '16px'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                background: 'rgba(99, 102, 241, 0.1)',
                border: '1px solid rgba(99, 102, 241, 0.2)',
                padding: '8px 12px',
                borderRadius: '20px',
                fontSize: '14px',
                color: '#6366f1',
                fontWeight: '500'
              }}>
                <DollarSign size={14} />
                {job.salary}
              </div>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                background: 'rgba(99, 102, 241, 0.1)',
                border: '1px solid rgba(99, 102, 241, 0.2)',
                padding: '8px 12px',
                borderRadius: '20px',
                fontSize: '14px',
                color: '#6366f1',
                fontWeight: '500'
              }}>
                <Clock size={14} />
                {job.experience}
              </div>
            </div>
            
            <p style={{
              color: '#cbd5e1',
              lineHeight: '1.6',
              marginBottom: '20px',
              fontSize: '14px'
            }}>{job.description}</p>
            
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
                {job.rating}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Users size={16} />
                {job.employees}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Clock size={16} />
                {job.posted}
              </div>
            </div>
            
            <div style={{
              textAlign: 'center',
              color: '#94a3b8',
              fontSize: '13px',
              marginTop: '12px',
              padding: '8px',
              background: 'rgba(15, 23, 42, 0.4)',
              borderRadius: '8px',
              fontWeight: '500'
            }}>
              {job.applicants} applicants
            </div>
          </motion.div>
        ))}
      </div>

      {selectedJob && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={closeJobDetails}
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
              maxWidth: '700px',
              width: '90%',
              maxHeight: '90vh',
              overflowY: 'auto',
              position: 'relative'
            }}
          >
            <button 
              onClick={closeJobDetails}
              style={{
                position: 'absolute',
                top: '20px',
                right: '24px',
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
            
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '20px',
              marginBottom: '32px',
              paddingBottom: '24px',
              borderBottom: '2px solid rgba(99, 102, 241, 0.2)'
            }}>
              <img 
                src={selectedJob.logo} 
                alt={selectedJob.company} 
                style={{
                  width: '80px',
                  height: '80px',
                  borderRadius: '16px',
                  objectFit: 'cover',
                  boxShadow: '0 8px 25px rgba(99, 102, 241, 0.4)'
                }}
              />
              <div>
                <h2 style={{
                  fontSize: '1.75rem',
                  marginBottom: '8px',
                  color: '#f1f5f9',
                  fontWeight: '700'
                }}>{selectedJob.title}</h2>
                <h3 style={{
                  color: '#6366f1',
                  marginBottom: '16px',
                  fontSize: '1.1rem',
                  fontWeight: '500'
                }}>{selectedJob.company}</h3>
                <div style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px',
                  fontSize: '15px',
                  color: '#94a3b8'
                }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <MapPin size={16} /> {selectedJob.location}
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Briefcase size={16} /> {selectedJob.type}
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <DollarSign size={16} /> {selectedJob.salary}
                  </span>
                </div>
              </div>
            </div>
            
            <div>
              <section style={{ marginBottom: '28px' }}>
                <h4 style={{
                  fontSize: '1.25rem',
                  marginBottom: '12px',
                  color: '#f1f5f9',
                  fontWeight: '600'
                }}>Job Description</h4>
                <p style={{ color: '#cbd5e1', lineHeight: '1.6', fontSize: '15px' }}>{selectedJob.description}</p>
              </section>
              
              <section style={{ marginBottom: '28px' }}>
                <h4 style={{
                  fontSize: '1.25rem',
                  marginBottom: '12px',
                  color: '#f1f5f9',
                  fontWeight: '600'
                }}>Requirements</h4>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                  {selectedJob.requirements.map((req, index) => (
                    <li key={index} style={{
                      padding: '10px 0',
                      borderBottom: '1px solid rgba(99, 102, 241, 0.1)',
                      position: 'relative',
                      paddingLeft: '24px',
                      fontSize: '15px',
                      lineHeight: '1.5',
                      color: '#cbd5e1'
                    }}>
                      <span style={{
                        position: 'absolute',
                        left: 0,
                        color: '#10b981',
                        fontWeight: 'bold',
                        fontSize: '16px'
                      }}>✓</span>
                      {req}
                    </li>
                  ))}
                </ul>
              </section>
              
              <section style={{ marginBottom: '28px' }}>
                <h4 style={{
                  fontSize: '1.25rem',
                  marginBottom: '12px',
                  color: '#f1f5f9',
                  fontWeight: '600'
                }}>Benefits</h4>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                  {selectedJob.benefits.map((benefit, index) => (
                    <li key={index} style={{
                      padding: '10px 0',
                      borderBottom: '1px solid rgba(99, 102, 241, 0.1)',
                      position: 'relative',
                      paddingLeft: '24px',
                      fontSize: '15px',
                      lineHeight: '1.5',
                      color: '#cbd5e1'
                    }}>
                      <span style={{
                        position: 'absolute',
                        left: 0,
                        color: '#10b981',
                        fontWeight: 'bold',
                        fontSize: '16px'
                      }}>✓</span>
                      {benefit}
                    </li>
                  ))}
                </ul>
              </section>
            </div>
            
            <div style={{
              display: 'flex',
              gap: '16px',
              marginTop: '32px',
              paddingTop: '24px',
              borderTop: '2px solid rgba(99, 102, 241, 0.2)'
            }}>
              <button 
                className="button-primary" 
                onClick={handleApplyJob}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}
              >
                Apply Now <ExternalLink size={16} />
              </button>
              <button className="button-secondary">Save Job</button>
            </div>
          </motion.div>
        </motion.div>
      )}

      {/* Application Modal */}
      <AnimatePresence>
        {showApplicationModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeApplicationModal}
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
              zIndex: 1001,
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
                maxWidth: '500px',
                width: '90%',
                position: 'relative'
              }}
            >
              <button 
                onClick={closeApplicationModal}
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
              >
                <X size={16} />
              </button>
              
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
                  <Mail size={24} color="white" />
                </div>
                <div>
                  <h3 style={{
                    color: '#f1f5f9',
                    margin: 0,
                    fontSize: '1.5rem',
                    fontWeight: '600'
                  }}>Apply for Job</h3>
                  <p style={{
                    color: '#cbd5e1',
                    margin: 0,
                    fontSize: '14px'
                  }}>Submit your application</p>
                </div>
              </div>

              {selectedJob && (
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
                  }}>{selectedJob.title}</h4>
                  <p style={{
                    color: '#6366f1',
                    margin: 0,
                    fontWeight: '500'
                  }}>{selectedJob.company}</p>
                </div>
              )}

              <div style={{ marginBottom: '24px' }}>
                <label style={{
                  display: 'block',
                  color: '#f1f5f9',
                  marginBottom: '8px',
                  fontWeight: '500'
                }}>Your Email Address</label>
                <input
                  type="email"
                  value={applicantEmail}
                  onChange={(e) => setApplicantEmail(e.target.value)}
                  placeholder="Enter your email address"
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    borderRadius: '8px',
                    border: '2px solid rgba(99, 102, 241, 0.2)',
                    background: 'rgba(15, 23, 42, 0.6)',
                    color: '#e2e8f0',
                    fontSize: '16px',
                    outline: 'none',
                    transition: 'border-color 0.3s ease'
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
                  📧 Your application will be sent to the company's HR team. 
                  You'll receive a confirmation email at the address you provided.
                </p>
              </div>

              <div style={{
                display: 'flex',
                gap: '12px'
              }}>
                <button
                  onClick={closeApplicationModal}
                  className="button-secondary"
                  style={{ flex: 1 }}
                >
                  Cancel
                </button>
                <button
                  onClick={handleSubmitApplication}
                  disabled={isSubmitting}
                  className="button-primary"
                  style={{
                    flex: 1,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px',
                    opacity: isSubmitting ? 0.7 : 1
                  }}
                >
                  {isSubmitting ? 'Sending...' : (
                    <>
                      <Send size={16} />
                      Submit Application
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ContentWriterJobs;