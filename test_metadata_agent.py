#!/usr/bin/env python3
"""
Test script for MetadataAgent
"""

from metadata_agent import MetadataAgent
from google_ai_integration import BlogWriterAgent

def test_metadata_agent():
    """Test the metadata agent functionality"""
    
    print("🧪 Testing MetadataAgent...")
    
    # Test data
    topic = "AI Tools for Content Creation"
    platform = "Instagram"
    sample_content = """
    # The Ultimate Guide to AI Tools for Content Creation in 2025

    Are you struggling to keep up with content demands? AI tools are revolutionizing how creators work! 🚀

    ## Top AI Tools You Need

    Here are the game-changing tools:
    - ChatGPT for writing
    - Midjourney for images  
    - Runway for videos
    - Jasper for marketing copy

    ## Why AI Tools Matter

    These tools can boost your productivity by 300%! Content creators are saving 10+ hours per week.

    ## Getting Started

    Start with free tools first, then upgrade as you grow. The key is finding tools that match your workflow.

    Ready to transform your content creation process? The future is here! ✨
    """
    
    try:
        # Initialize agent
        agent = MetadataAgent()
        
        # Generate metadata
        print(f"📝 Topic: {topic}")
        print(f"📱 Platform: {platform}")
        print("🔄 Generating metadata...\n")
        
        metadata = agent.generate_metadata(topic, sample_content, platform)
        
        if metadata['success']:
            print("✅ SUCCESS! Generated metadata:")
            print(f"\n🏷️ Hashtags ({len(metadata['hashtags'])}):")
            for hashtag in metadata['hashtags']:
                print(f"  {hashtag}")
            
            print(f"\n💯 Call to Action:")
            print(f"  {metadata['cta']}")
            
            print(f"\n🔍 SEO Keywords ({len(metadata['keywords'])}):")
            print(f"  {', '.join(metadata['keywords'])}")
            
        else:
            print(f"❌ FAILED: {metadata.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_full_integration():
    """Test full blog generation with metadata agent"""
    
    print("\n" + "="*60)
    print("🧪 Testing Full Integration...")
    print("="*60)
    
    try:
        # Initialize blog writer agent
        agent = BlogWriterAgent()
        
        # Generate complete blog
        topic = "Best Travel Apps for Digital Nomads"
        platform = "LinkedIn"
        
        print(f"📝 Generating blog: {topic}")
        print(f"📱 Platform: {platform}\n")
        
        result = agent.write_blog(topic, platform, 600)
        
        if result['success']:
            print("✅ SUCCESS! Generated complete blog:")
            print(f"\n📰 Title: {result['title']}")
            print(f"\n📊 Stats:")
            print(f"  • Word Count: {result['word_count']}")
            print(f"  • Engagement Score: {result['engagement_score']:.2f}")
            print(f"  • Metadata Generated: {result['metadata']['metadata_generated']}")
            
            print(f"\n🏷️ Hashtags ({len(result['hashtags'])}):")
            print(f"  {' '.join(result['hashtags'][:5])}...")
            
            print(f"\n💯 CTA: {result['cta']}")
            
            print(f"\n🔍 Keywords: {', '.join(result['keywords'][:5])}")
            
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_metadata_agent()
    test_full_integration()