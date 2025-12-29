from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db_manager
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user via React"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'success': False, 'message': 'All fields required'}), 400
        
        result = db_manager.register_user(username, email, password)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user via React"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        result = db_manager.login_user(username, password)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/validate', methods=['POST'])
def validate_session():
    """Validate session token"""
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token required'}), 400
        
        result = db_manager.validate_session(token)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/blog/save-session', methods=['POST'])
def save_blog_session():
    """Save blog session via React"""
    try:
        data = request.json
        user_id = data.get('user_id')
        session_data = data.get('session_data')
        
        if not all([user_id, session_data]):
            return jsonify({'success': False, 'message': 'User ID and session data required'}), 400
        
        result = db_manager.save_blog_session(user_id, session_data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/blog/get-sessions/<user_id>', methods=['GET'])
def get_user_sessions(user_id):
    """Get user sessions via React"""
    try:
        sessions = db_manager.get_user_sessions(user_id)
        return jsonify({'success': True, 'sessions': sessions})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/posts/save', methods=['POST'])
def save_post():
    """Save post history via React"""
    try:
        data = request.json
        user_id = data.get('user_id')
        post_data = data.get('post_data')
        
        if not all([user_id, post_data]):
            return jsonify({'success': False, 'message': 'User ID and post data required'}), 400
        
        result = db_manager.save_posting_history(user_id, post_data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/analytics/<user_id>', methods=['GET'])
def get_analytics(user_id):
    """Get user analytics via React"""
    try:
        analytics = db_manager.get_user_analytics(user_id)
        return jsonify({'success': True, 'analytics': analytics})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting React Auth API on http://localhost:5001")
    app.run(debug=True, port=5001)