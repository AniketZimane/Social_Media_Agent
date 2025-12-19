import datetime
from typing import List, Dict
import random

class ContentCalendar:
    def __init__(self):
        self.optimal_times = {
            '📸 Instagram': [
                {'day': 'Monday', 'time': '11:00', 'engagement': 0.85},
                {'day': 'Wednesday', 'time': '15:00', 'engagement': 0.92},
                {'day': 'Friday', 'time': '18:00', 'engagement': 0.88},
                {'day': 'Sunday', 'time': '19:00', 'engagement': 0.90}
            ],
            '🐦 Twitter': [
                {'day': 'Tuesday', 'time': '09:00', 'engagement': 0.87},
                {'day': 'Wednesday', 'time': '12:00', 'engagement': 0.91},
                {'day': 'Thursday', 'time': '15:00', 'engagement': 0.89},
                {'day': 'Friday', 'time': '17:00', 'engagement': 0.86}
            ],
            '💼 LinkedIn': [
                {'day': 'Tuesday', 'time': '08:00', 'engagement': 0.93},
                {'day': 'Wednesday', 'time': '10:00', 'engagement': 0.95},
                {'day': 'Thursday', 'time': '09:00', 'engagement': 0.91},
                {'day': 'Friday', 'time': '11:00', 'engagement': 0.88}
            ],
            '📺 YouTube': [
                {'day': 'Thursday', 'time': '14:00', 'engagement': 0.89},
                {'day': 'Friday', 'time': '16:00', 'engagement': 0.92},
                {'day': 'Saturday', 'time': '15:00', 'engagement': 0.94},
                {'day': 'Sunday', 'time': '17:00', 'engagement': 0.90}
            ],
            '👥 Facebook': [
                {'day': 'Wednesday', 'time': '13:00', 'engagement': 0.86},
                {'day': 'Friday', 'time': '19:00', 'engagement': 0.91},
                {'day': 'Saturday', 'time': '12:00', 'engagement': 0.93},
                {'day': 'Sunday', 'time': '20:00', 'engagement': 0.89}
            ]
        }
    
    def generate_weekly_calendar(self, blog_content: Dict, platforms: List[str]) -> List[Dict]:
        """Generate 7-day content calendar with optimal posting times"""
        calendar = []
        today = datetime.datetime.now()
        
        for day_offset in range(7):
            post_date = today + datetime.timedelta(days=day_offset)
            day_name = post_date.strftime('%A')
            
            # Find platforms that have optimal times for this day
            for platform in platforms:
                optimal_slots = self.optimal_times.get(platform, [])
                day_slots = [slot for slot in optimal_slots if slot['day'] == day_name]
                
                if day_slots:
                    slot = day_slots[0]
                    calendar.append({
                        'id': len(calendar) + 1,
                        'date': post_date.strftime('%Y-%m-%d'),
                        'day': day_name,
                        'time': slot['time'],
                        'platform': platform,
                        'title': blog_content.get('title', 'Blog Post'),
                        'content_preview': blog_content.get('content', '')[:100] + '...',
                        'hashtags': blog_content.get('hashtags', [])[:5],
                        'engagement_score': slot['engagement'],
                        'status': 'scheduled',
                        'image_url': None
                    })
        
        # Sort by date and time
        calendar.sort(key=lambda x: (x['date'], x['time']))
        
        return calendar[:7]  # Return max 7 posts for the week
    
    def get_content_suggestions(self, topic: str) -> List[Dict]:
        """Generate content variation suggestions for the week"""
        variations = [
            {'angle': 'Educational', 'focus': 'How-to guide and tutorials'},
            {'angle': 'Inspirational', 'focus': 'Success stories and motivation'},
            {'angle': 'News', 'focus': 'Latest trends and updates'},
            {'angle': 'Behind-the-scenes', 'focus': 'Process and insights'},
            {'angle': 'Tips & Tricks', 'focus': 'Quick actionable advice'},
            {'angle': 'Case Study', 'focus': 'Real-world examples'},
            {'angle': 'Opinion', 'focus': 'Expert perspective and analysis'}
        ]
        
        return variations[:7]
