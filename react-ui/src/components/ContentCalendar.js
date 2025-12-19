import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Clock, Image as ImageIcon } from 'lucide-react';

const ContentCalendar = ({ blogContent }) => {
  const [calendar, setCalendar] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedPlatforms, setSelectedPlatforms] = useState(['📸 Instagram', '🐦 Twitter', '💼 LinkedIn']);

  const platforms = ['📸 Instagram', '🐦 Twitter', '💼 LinkedIn', '📺 YouTube', '👥 Facebook'];

  const generateCalendar = async () => {
    if (!blogContent) {
      alert('Please generate blog content first');
      return;
    }

    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:5000/api/calendar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          blog_content: blogContent,
          platforms: selectedPlatforms
        })
      });

      const data = await response.json();
      setCalendar(data.calendar || []);
    } catch (error) {
      console.error('Calendar error:', error);
    }
    setIsGenerating(false);
  };

  return (
    <div className="content-calendar">
      <motion.div className="card" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <div className="section-header">
          <Calendar className="section-icon" />
          <h2>7-Day Content Calendar</h2>
        </div>

        <div className="platform-selector">
          <h4>Select Platforms:</h4>
          <div className="platforms-grid">
            {platforms.map(p => (
              <label key={p} className="platform-checkbox">
                <input
                  type="checkbox"
                  checked={selectedPlatforms.includes(p)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedPlatforms([...selectedPlatforms, p]);
                    } else {
                      setSelectedPlatforms(selectedPlatforms.filter(x => x !== p));
                    }
                  }}
                />
                <span>{p}</span>
              </label>
            ))}
          </div>
        </div>

        <button className="button-primary" onClick={generateCalendar} disabled={isGenerating}>
          {isGenerating ? 'Generating...' : 'Generate Calendar'}
        </button>

        {calendar.length > 0 && (
          <div className="calendar-grid">
            {calendar.map(post => (
              <motion.div key={post.id} className="calendar-card" initial={{ scale: 0.9 }} animate={{ scale: 1 }}>
                <div className="calendar-header">
                  <span className="day">{post.day}</span>
                  <span className="date">{post.date}</span>
                </div>
                <div className="calendar-body">
                  <h4>{post.title}</h4>
                  <p className="platform">{post.platform}</p>
                  <div className="time-slot">
                    <Clock size={14} />
                    <span>{post.time}</span>
                  </div>
                  <div className="engagement">Engagement: {(post.engagement_score * 100).toFixed(0)}%</div>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        <style jsx>{`
          .content-calendar { max-width: 1200px; margin: 0 auto; }
          .section-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 2rem; }
          .section-header h2 { color: #f1f5f9; font-size: 1.75rem; font-weight: 600; }
          .section-icon { color: #6366f1; }
          .platform-selector { margin-bottom: 2rem; }
          .platforms-grid { display: flex; gap: 1rem; flex-wrap: wrap; }
          .platform-checkbox { display: flex; align-items: center; gap: 0.5rem; color: #cbd5e1; }
          .calendar-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
          .calendar-card { background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 12px; overflow: hidden; }
          .calendar-header { background: #6366f1; color: white; padding: 1rem; display: flex; justify-content: space-between; }
          .calendar-body { padding: 1rem; }
          .calendar-body h4 { color: #f1f5f9; margin-bottom: 0.5rem; }
          .platform { color: #6366f1; font-size: 0.9rem; }
          .time-slot { display: flex; align-items: center; gap: 0.5rem; color: #cbd5e1; margin: 0.5rem 0; }
          .engagement { color: #10b981; font-weight: 500; }
        `}</style>
      </motion.div>
    </div>
  );
};

export default ContentCalendar;
