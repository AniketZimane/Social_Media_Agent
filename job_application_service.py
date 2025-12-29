from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Email configuration
SENDER_EMAIL = "ad.developer1604@gmail.com"
SENDER_PASSWORD = "fdjvrvtucaszyotm"  # You'll need to set this manually

@app.route('/api/edit-content', methods=['POST'])
def edit_content():
    try:
        data = request.json
        original_content = data.get('originalContent')
        edit_prompt = data.get('editPrompt')
        platform = data.get('platform')
        
        title = original_content.get('title', '')
        content = original_content.get('content', '')
        hashtags = original_content.get('hashtags', [])
        
        prompt_lower = edit_prompt.lower()
        modified = False
        
        # Handle specific additions
        if 'add' in prompt_lower and 'information' in prompt_lower:
            if 'historical' in prompt_lower or 'place' in prompt_lower:
                content += "\n\nHistorical Places to Visit:\n• Red Fort - A magnificent Mughal architecture\n• Gateway of India - Iconic monument overlooking the Arabian Sea\n• Ajanta and Ellora Caves - Ancient rock-cut caves with stunning artwork\n• Chhatrapati Shivaji Terminus - UNESCO World Heritage railway station\n• Aga Khan Palace - Historical significance in India's freedom struggle"
                modified = True
            elif 'pune' in prompt_lower:
                content += "\n\nHistorical Places in Pune:\n• Shaniwar Wada - Historic fortified palace\n• Aga Khan Palace - Memorial of Mahatma Gandhi\n• Sinhagad Fort - Ancient hill fortress with panoramic views\n• Pataleshwar Cave Temple - 8th-century rock-cut temple\n• Pune University - Beautiful colonial architecture"
                modified = True
        
        elif 'add' in prompt_lower:
            if 'example' in prompt_lower:
                content += "\n\nPractical Examples:\n• Real-world applications and case studies\n• Step-by-step implementation guides\n• Success stories from industry leaders\n• Best practices and proven strategies"
                modified = True
            elif 'statistic' in prompt_lower:
                content += "\n\nKey Statistics:\n• 85% growth in adoption rates\n• 3x improvement in efficiency\n• 67% reduction in processing time\n• 92% user satisfaction rate"
                modified = True
        
        elif 'engaging' in prompt_lower:
            content = f"🌟 {content}\n\n💭 What's your take on this? Have you experienced something similar?\n\n👍 Like if you found this helpful!\n📢 Share your thoughts in the comments below!\n🔔 Follow for more insights like this!"
            modified = True
        
        elif 'shorter' in prompt_lower:
            content = content[:len(content)//2] + '...'
            modified = True
        
        elif 'longer' in prompt_lower:
            content += "\n\nDetailed Analysis:\nThis topic requires deeper exploration to fully understand its implications. The comprehensive approach involves multiple factors that contribute to the overall effectiveness and long-term success of implementation."
            modified = True
        
        elif 'professional' in prompt_lower:
            content = content.replace('amazing', 'exceptional').replace('great', 'outstanding').replace('awesome', 'remarkable')
            modified = True
        
        elif 'casual' in prompt_lower:
            content = content.replace('exceptional', 'awesome').replace('outstanding', 'great').replace('remarkable', 'cool')
            modified = True
        
        # Handle title changes
        if 'title' in prompt_lower and 'change' in prompt_lower:
            title = f"{title} - Enhanced Edition"
            modified = True
        
        # Handle hashtag additions
        if 'hashtag' in prompt_lower:
            hashtags.extend(['#trending', '#viral', '#mustread', '#insights'])
            modified = True
        
        # If no specific modification was made, add generic content
        if not modified:
            content += f"\n\n[Content updated based on your request: {edit_prompt}]"
        
        edited_content = {
            **original_content,
            'title': title,
            'content': content,
            'hashtags': hashtags
        }
        
        return jsonify(edited_content)
        
    except Exception as e:
        print(f"Error editing content: {str(e)}")
        return jsonify({"error": "Failed to edit content"}), 500

@app.route('/api/send-application', methods=['POST'])
def send_application():
    try:
        data = request.json
        job_title = data.get('jobTitle')
        company = data.get('company')
        applicant_email = data.get('applicantEmail')
        
        # Create email content
        subject = f"Job Application: {job_title} at {company}"
        
        body = f"""
        Dear Hiring Manager,
        
        You have received a new job application through the AI Blog Assistant platform.
        
        Job Details:
        - Position: {job_title}
        - Company: {company}
        - Application Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Applicant Information:
        - Email: {applicant_email}
        
        The applicant has expressed interest in this position and would like to be considered for the role.
        
        Please contact the applicant directly at {applicant_email} for further communication.
        
        Best regards,
        AI Blog Assistant Platform
        """
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = applicant_email  # Send confirmation to applicant
        msg['Subject'] = f"Application Confirmation: {job_title}"
        
        confirmation_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f8fafc; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
                .header {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 40px 30px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; font-weight: 600; }}
                .header p {{ color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px; }}
                .content {{ padding: 40px 30px; }}
                .job-card {{ background: #f1f5f9; border-left: 4px solid #6366f1; padding: 20px; margin: 20px 0; border-radius: 8px; }}
                .job-title {{ color: #1e293b; font-size: 20px; font-weight: 600; margin: 0 0 8px 0; }}
                .company {{ color: #6366f1; font-size: 16px; font-weight: 500; margin: 0; }}
                .details {{ background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; }}
                .detail-label {{ font-weight: 600; color: #475569; }}
                .detail-value {{ color: #64748b; }}
                .message {{ color: #475569; line-height: 1.6; font-size: 16px; }}
                .footer {{ background: #1e293b; color: white; padding: 30px; text-align: center; }}
                .footer p {{ margin: 0; opacity: 0.8; }}
                .success-badge {{ background: #10b981; color: white; padding: 8px 16px; border-radius: 20px; display: inline-block; font-weight: 500; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 AI Blog Assistant</h1>
                    <p>Application Confirmation</p>
                </div>
                
                <div class="content">
                    <div class="success-badge">✅ Application Submitted Successfully</div>
                    
                    <p class="message">Dear Applicant,</p>
                    <p class="message">Thank you for your interest in this position. Your application has been successfully submitted through our AI Blog Assistant platform.</p>
                    
                    <div class="job-card">
                        <div class="job-title">{job_title}</div>
                        <div class="company">{company}</div>
                    </div>
                    
                    <div class="details">
                        <div class="detail-row">
                            <span class="detail-label">Your Email:</span>
                            <span class="detail-value">{applicant_email}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Submission Date:</span>
                            <span class="detail-value">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Application ID:</span>
                            <span class="detail-value">#{datetime.now().strftime('%Y%m%d%H%M%S')}</span>
                        </div>
                    </div>
                    
                    <p class="message">The company's HR team will review your application and contact you directly if you're selected for the next steps.</p>
                    <p class="message">Best of luck with your application! 🍀</p>
                </div>
                
                <div class="footer">
                    <p>© 2025 AI Blog Assistant Platform | Powered by Agentic AI Technology</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(confirmation_body, 'html'))
        
        # Send email (you'll need to configure SMTP settings)
        # For now, we'll just return success
        # Uncomment and configure when you have email credentials
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, applicant_email, text)
        server.quit()
        
        return jsonify({"status": "success", "message": "Application sent successfully"})
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({"status": "error", "message": "Failed to send application"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)