from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Sample video lectures data
VIDEO_LECTURES = [
    {
        "id": 1,
        "title": "AI Content Creation Masterclass",
        "youtubeId": "dQw4w9WgXcQ",
        "duration": "45:30",
        "instructor": "Sarah Johnson",
        "rating": 4.8,
        "students": 12500,
        "description": "Learn advanced AI techniques for creating engaging content across all platforms.",
        "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
        "category": "AI & Technology",
        "tags": ["AI", "Content Creation", "Marketing", "Automation"]
    },
    {
        "id": 2,
        "title": "Social Media Strategy 2024",
        "youtubeId": "jNQXAC9IVRw",
        "duration": "38:15",
        "instructor": "Mike Chen",
        "rating": 4.9,
        "students": 8900,
        "description": "Complete guide to building successful social media campaigns.",
        "thumbnail": "https://img.youtube.com/vi/jNQXAC9IVRw/maxresdefault.jpg",
        "category": "Marketing",
        "tags": ["Social Media", "Strategy", "Engagement", "Growth"]
    }
]

# Sample job listings data
JOB_LISTINGS = [
    {
        "id": 1,
        "title": "Senior Content Writer - AI & Tech",
        "company": "TechFlow Inc.",
        "location": "Remote",
        "type": "Full-time",
        "salary": "$75,000 - $95,000",
        "experience": "3-5 years",
        "rating": 4.8,
        "employees": "500-1000",
        "description": "Create compelling content for AI and technology products. Work with cutting-edge AI tools to produce high-quality blog posts, whitepapers, and marketing materials.",
        "requirements": [
            "3+ years of content writing experience",
            "Strong understanding of AI and technology",
            "Experience with SEO optimization",
            "Excellent research skills"
        ],
        "benefits": [
            "Remote work flexibility",
            "Health insurance",
            "401k matching",
            "Professional development budget"
        ],
        "posted": "2 days ago",
        "applicants": 45,
        "logo": "https://via.placeholder.com/60x60/667eea/white?text=TF",
        "skills": ["Content Writing", "AI", "SEO", "Research"],
        "remote": True,
        "urgent": False
    },
    {
        "id": 2,
        "title": "Social Media Content Creator",
        "company": "Digital Spark Agency",
        "location": "New York, NY",
        "type": "Contract",
        "salary": "$50 - $75/hour",
        "experience": "2-4 years",
        "rating": 4.6,
        "employees": "50-200",
        "description": "Create engaging social media content for multiple clients across various industries.",
        "requirements": [
            "2+ years social media experience",
            "Portfolio of successful campaigns",
            "Knowledge of social media trends",
            "Video editing skills preferred"
        ],
        "benefits": [
            "Flexible schedule",
            "Creative freedom",
            "Performance bonuses",
            "Networking opportunities"
        ],
        "posted": "1 day ago",
        "applicants": 32,
        "logo": "https://via.placeholder.com/60x60/764ba2/white?text=DS",
        "skills": ["Social Media", "Content Creation", "Video Editing", "Campaigns"],
        "remote": False,
        "urgent": True
    }
]

@app.route('/api/videos', methods=['GET'])
def get_videos():
    """Get all video lectures"""
    search = request.args.get('search', '').lower()
    category = request.args.get('category', '')
    
    filtered_videos = VIDEO_LECTURES
    
    if search:
        filtered_videos = [v for v in filtered_videos 
                          if search in v['title'].lower() or 
                             search in v['category'].lower() or
                             any(search in tag.lower() for tag in v['tags'])]
    
    if category:
        filtered_videos = [v for v in filtered_videos if v['category'] == category]
    
    return jsonify({
        'success': True,
        'videos': filtered_videos,
        'total': len(filtered_videos)
    })

@app.route('/api/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    """Get specific video details"""
    video = next((v for v in VIDEO_LECTURES if v['id'] == video_id), None)
    
    if not video:
        return jsonify({'success': False, 'error': 'Video not found'}), 404
    
    return jsonify({
        'success': True,
        'video': video
    })

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all job listings"""
    search = request.args.get('search', '').lower()
    job_type = request.args.get('type', '')
    location = request.args.get('location', '')
    remote_only = request.args.get('remote', '').lower() == 'true'
    
    filtered_jobs = JOB_LISTINGS
    
    if search:
        filtered_jobs = [j for j in filtered_jobs 
                        if search in j['title'].lower() or 
                           search in j['company'].lower() or
                           any(search in skill.lower() for skill in j['skills'])]
    
    if job_type:
        filtered_jobs = [j for j in filtered_jobs if j['type'].lower() == job_type.lower()]
    
    if location:
        filtered_jobs = [j for j in filtered_jobs if location.lower() in j['location'].lower()]
    
    if remote_only:
        filtered_jobs = [j for j in filtered_jobs if j['remote']]
    
    return jsonify({
        'success': True,
        'jobs': filtered_jobs,
        'total': len(filtered_jobs)
    })

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get specific job details"""
    job = next((j for j in JOB_LISTINGS if j['id'] == job_id), None)
    
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    return jsonify({
        'success': True,
        'job': job
    })

@app.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
def apply_job(job_id):
    """Apply for a job"""
    job = next((j for j in JOB_LISTINGS if j['id'] == job_id), None)
    
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404
    
    application_data = request.json
    
    # In a real app, you would save this to a database
    # For now, just return success
    return jsonify({
        'success': True,
        'message': 'Application submitted successfully',
        'application_id': f"APP_{job_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    })

@app.route('/api/videos/trending', methods=['GET'])
def get_trending_videos():
    """Get trending video lectures"""
    # Sort by rating and student count
    trending = sorted(VIDEO_LECTURES, 
                     key=lambda x: (x['rating'] * x['students']), 
                     reverse=True)[:3]
    
    return jsonify({
        'success': True,
        'trending_videos': trending
    })

@app.route('/api/jobs/featured', methods=['GET'])
def get_featured_jobs():
    """Get featured job listings"""
    # Get urgent jobs and high-rated companies
    featured = [j for j in JOB_LISTINGS if j.get('urgent', False) or j['rating'] >= 4.7]
    
    return jsonify({
        'success': True,
        'featured_jobs': featured
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    return jsonify({
        'success': True,
        'stats': {
            'total_videos': len(VIDEO_LECTURES),
            'total_jobs': len(JOB_LISTINGS),
            'active_learners': sum(v['students'] for v in VIDEO_LECTURES),
            'job_applications': sum(j['applicants'] for j in JOB_LISTINGS),
            'avg_video_rating': round(sum(v['rating'] for v in VIDEO_LECTURES) / len(VIDEO_LECTURES), 1),
            'avg_company_rating': round(sum(j['rating'] for j in JOB_LISTINGS) / len(JOB_LISTINGS), 1)
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Video & Jobs API Server...")
    print("📺 Video Lectures API: http://localhost:5001/api/videos")
    print("💼 Jobs API: http://localhost:5001/api/jobs")
    print("📊 Stats API: http://localhost:5001/api/stats")
    app.run(debug=True, port=5001)