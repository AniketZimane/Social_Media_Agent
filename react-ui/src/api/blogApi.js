import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Flask API server port

class BlogAPI {
  // Generate blog content using your existing Python backend
  async generateBlogContent(topic, platform, contentFocus, maxWords) {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/generate`, {
        topic,
        platform,
        content_focus: contentFocus,
        max_words: maxWords,
        ai_mode: 'Dynamic AI'
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      // Fallback to mock data if API fails
      return this.getMockContent(topic, platform, maxWords);
    }
  }

  // Schedule social media post
  async schedulePost(content, platforms, scheduleDate, scheduleTime) {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/schedule`, {
        content,
        platforms,
        schedule_date: scheduleDate,
        schedule_time: scheduleTime
      });
      return response.data;
    } catch (error) {
      console.error('Schedule Error:', error);
      return { success: false, error: error.message };
    }
  }

  // Get posting history
  async getPostingHistory() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/history`);
      return response.data;
    } catch (error) {
      console.error('History Error:', error);
      return [];
    }
  }

  // Generate hashtags
  async generateHashtags(topic, platform) {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/hashtags`, {
        topic,
        platform
      });
      return response.data.hashtags;
    } catch (error) {
      console.error('Hashtags Error:', error);
      return this.getMockHashtags(topic, platform);
    }
  }

  // Generate blog image
  async generateBlogImage(topic) {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/image`, {
        topic
      });
      return response.data.image_url;
    } catch (error) {
      console.error('Image Error:', error);
      return null;
    }
  }

  // Mock data fallback (same as your Python logic)
  getMockContent(topic, platform, maxWords) {
    const platformHashtags = {
      '📸 Instagram': ['#AI', '#Innovation', '#Technology', '#Future', '#Digital', '#Trending', '#2024', '#Tech', '#Business', '#Growth', '#Instagood', '#PhotoOfTheDay', '#Viral', '#Explore', '#InnovationDaily'],
      '🐦 Twitter': ['#AI', '#Tech', '#Innovation', '#Breaking', '#Thread'],
      '💼 LinkedIn': ['#AI', '#Innovation', '#Technology', '#Professional', '#Business', '#Career', '#Industry', '#Leadership'],
      '📺 YouTube': ['#AI', '#Technology', '#Tutorial', '#HowTo', '#Educational', '#Subscribe', '#Innovation', '#Tech', '#Future', '#Digital', '#Learning', '#Guide', '#Tips', '#Trending', '#2024'],
      '👥 Facebook': ['#AI', '#Innovation', '#Technology', '#Community', '#Share', '#Like', '#Follow', '#Digital', '#Future', '#Tech']
    };

    const hashtagLimits = {
      '📸 Instagram': 30,
      '🐦 Twitter': 5,
      '💼 LinkedIn': 8,
      '📺 YouTube': 15,
      '👥 Facebook': 10
    };

    const baseContent = `Discover the transformative power of ${topic} in today's digital landscape. This comprehensive guide explores cutting-edge developments, practical applications, and future trends that are reshaping industries worldwide. From breakthrough innovations to real-world implementations, learn how ${topic} is driving unprecedented change and creating new opportunities for businesses and individuals alike. Whether you're a professional looking to stay ahead or someone curious about the latest developments, this insight-packed content will provide you with valuable knowledge and actionable strategies.`;
    
    const words = baseContent.split(' ');
    const limitedContent = words.slice(0, maxWords).join(' ') + (words.length > maxWords ? '...' : '');
    
    const selectedHashtags = platformHashtags[platform] || platformHashtags['📸 Instagram'];
    const hashtagLimit = hashtagLimits[platform] || 10;

    return {
      title: `The Future of ${topic}: Revolutionary Insights for 2024`,
      content: limitedContent,
      hashtags: selectedHashtags.slice(0, hashtagLimit),
      cta: `Ready to explore the future of ${topic}? Follow for more insights and join the conversation!`,
      keywords: [topic, 'innovation', 'technology', 'future', '2024'],
      engagement_score: 0.87,
      platform: platform,
      wordCount: limitedContent.split(' ').length
    };
  }

  getMockHashtags(topic, platform) {
    const platformHashtags = {
      '📸 Instagram': ['#instagood', '#photooftheday', '#viral', '#explore'],
      '🐦 Twitter': ['#breaking', '#news', '#thread', '#viral'],
      '💼 LinkedIn': ['#professional', '#business', '#career', '#industry'],
      '📺 YouTube': ['#tutorial', '#howto', '#educational', '#subscribe'],
      '👥 Facebook': ['#community', '#share', '#like', '#follow']
    };

    const baseTags = [`#${topic.replace(' ', '')}`, '#trending', '#2024'];
    const platformSpecific = platformHashtags[platform] || ['#content', '#social', '#digital'];
    
    return [...baseTags, ...platformSpecific, '#AI', '#tech', '#innovation'];
  }
}

export default new BlogAPI();