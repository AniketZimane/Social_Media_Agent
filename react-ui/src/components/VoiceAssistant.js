import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Volume2, Download, Bot, Zap, Play, Pause, RotateCcw } from 'lucide-react';
import Button from './Button';

const VoiceAssistant = () => {
  const [isListening, setIsListening] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [responses, setResponses] = useState({});
  const [generatedContent, setGeneratedContent] = useState('');
  const [conversationComplete, setConversationComplete] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversationStarted, setConversationStarted] = useState(false);
  const [processingStep, setProcessingStep] = useState('');
  const [estimatedTime, setEstimatedTime] = useState(0);
  const [recognitionActive, setRecognitionActive] = useState(false);

  const recognitionRef = useRef(null);
  const synthRef = useRef(null);

  const questions = [
    "Hi! I'm your AI blog assistant. What topic would you like to create content about today?",
    "Great choice! Which platform are you targeting - Instagram, Twitter, LinkedIn, YouTube, or Facebook?",
    "Perfect! What's your main goal with this content - to educate, entertain, inspire, or promote something?",
    "Excellent! Who is your target audience - beginners, professionals, or general audience?",
    "Almost done! How long should the content be - short and punchy, medium length, or detailed and comprehensive?"
  ];

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';
      
      if (recognitionRef.current.speechTimeout) {
        recognitionRef.current.speechTimeout = 10000;
      }

      recognitionRef.current.onresult = (event) => {
        const capturedTranscript = event.results[0][0].transcript.trim();
        console.log(`🎯 Speech result received:`, capturedTranscript);
        
        if (capturedTranscript.length > 0) {
          setTranscript(capturedTranscript);
          setIsListening(false);
          setRecognitionActive(false);
          
          try {
            recognitionRef.current.stop();
          } catch (e) {}
          
          setTimeout(() => {
            processResponse(capturedTranscript);
          }, 500);
        }
      };

      recognitionRef.current.onerror = (event) => {
        console.error('❌ Speech recognition error:', event.error);
        setIsListening(false);
        setRecognitionActive(false);
      };

      recognitionRef.current.onend = () => {
        console.log('🎤 Speech recognition ended');
        setIsListening(false);
        setRecognitionActive(false);
      };
    }

    synthRef.current = window.speechSynthesis;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, []);

  useEffect(() => {
    if (conversationStarted && currentQuestion < questions.length && !conversationComplete) {
      console.log(`🔊 Speaking question ${currentQuestion + 1}:`, questions[currentQuestion]);
      
      setTranscript('');
      setRecognitionActive(false);
      setIsListening(false);
      
      setTimeout(() => {
        speak(questions[currentQuestion]);
        
        setTimeout(() => {
          console.log('🎤 Auto-starting listening for question', currentQuestion + 1);
          if (!conversationComplete) {
            startListening();
          }
        }, 6000);
      }, 500);
    }
  }, [conversationStarted, currentQuestion, conversationComplete]);

  // Listen for navigation events from parent App component
  useEffect(() => {
    const handleNavigateToOptimizer = (event) => {
      // This will be handled by App.js
      console.log('Navigation to optimizer requested:', event.detail);
    };
    
    window.addEventListener('navigateToOptimizer', handleNavigateToOptimizer);
    
    return () => {
      window.removeEventListener('navigateToOptimizer', handleNavigateToOptimizer);
    };
  }, []);

  const speak = (text) => {
    if (synthRef.current) {
      synthRef.current.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      utterance.volume = 1;
      synthRef.current.speak(utterance);
    }
  };

  const startListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {}
    }
    
    setIsListening(false);
    setRecognitionActive(false);
    
    setTimeout(() => {
      setCurrentQuestion(prevQuestion => {
        if (!conversationComplete && prevQuestion < questions.length) {
          console.log('🎤 Starting fresh speech recognition for question:', prevQuestion + 1);
          setIsListening(true);
          setRecognitionActive(true);
          
          try {
            recognitionRef.current.start();
            
            setTimeout(() => {
              setIsListening(prevListening => {
                setRecognitionActive(prevActive => {
                  if (prevListening && prevActive) {
                    console.log('⏰ Auto-stopping recognition after timeout');
                    stopListening();
                  }
                  return prevActive;
                });
                return prevListening;
              });
            }, 10000);
          } catch (error) {
            console.log('Recognition start error:', error);
            setIsListening(false);
            setRecognitionActive(false);
          }
        }
        return prevQuestion;
      });
    }, 500);
  };

  const stopListening = () => {
    if (recognitionRef.current && (isListening || recognitionActive)) {
      console.log('🔇 Stopping speech recognition...');
      try {
        recognitionRef.current.stop();
      } catch (error) {
        console.log('Stop error:', error);
      }
      setIsListening(false);
      setRecognitionActive(false);
    }
  };

  const processResponse = (response) => {
    setCurrentQuestion(prevQuestion => {
      const questionNum = prevQuestion;
      console.log(`🎤 Processing response for question ${questionNum + 1}: "${response}"`);
      console.log('🔢 Current question state:', questionNum);
      
      setResponses(prevResponses => {
        const newResponses = { ...prevResponses };
        
        if (questionNum === 0) {
          newResponses.topic = response;
          console.log('📝 Topic set:', response);
        } else if (questionNum === 1) {
          const platforms = ['instagram', 'twitter', 'linkedin', 'youtube', 'facebook'];
          const detectedPlatform = platforms.find(p => response.toLowerCase().includes(p)) || 'instagram';
          newResponses.platform = detectedPlatform;
          console.log('📱 Platform detected:', detectedPlatform, 'from response:', response);
        } else if (questionNum === 2) {
          const goals = { educate: 'educational', entertain: 'entertaining', inspire: 'inspirational', promote: 'promotional' };
          const detectedGoal = Object.keys(goals).find(g => response.toLowerCase().includes(g));
          newResponses.goal = detectedGoal ? goals[detectedGoal] : 'educational';
          console.log('🎯 Goal detected:', newResponses.goal, 'from response:', response);
        } else if (questionNum === 3) {
          const audiences = { beginner: 'beginners', professional: 'professionals', general: 'general' };
          const detectedAudience = Object.keys(audiences).find(a => response.toLowerCase().includes(a));
          newResponses.audience = detectedAudience ? audiences[detectedAudience] : 'general';
          console.log('👥 Audience detected:', newResponses.audience, 'from response:', response);
        } else if (questionNum === 4) {
          if (response.toLowerCase().includes('short') || response.toLowerCase().includes('punchy')) {
            newResponses.length = 'short';
          } else if (response.toLowerCase().includes('detailed') || response.toLowerCase().includes('comprehensive')) {
            newResponses.length = 'long';
          } else {
            newResponses.length = 'medium';
          }
          console.log('📏 Length detected:', newResponses.length, 'from response:', response);
        }

        console.log('💾 Updated responses:', JSON.stringify(newResponses, null, 2));
        
        if (questionNum < 4) {
          console.log(`➡️ Moving from question ${questionNum + 1} to ${questionNum + 2}`);
          setTimeout(() => {
            console.log('🔄 Setting question to:', questionNum + 1);
            setCurrentQuestion(questionNum + 1);
          }, 1500);
          return newResponses;
        } else {
          console.log('✅ All responses collected, starting content generation');
          speak('Thank you! Now let me create your personalized content. This will take about 15 seconds.');
          
          setTimeout(() => {
            console.log('⏰ Timeout triggered, calling generateContent');
            generateContent(newResponses);
          }, 2000);
          return newResponses;
        }
      });
      
      return prevQuestion;
    });
  };

  const generateContent = async (finalResponses) => {
    setIsProcessing(true);
    setEstimatedTime(15);
    
    console.log('🚀 STARTING DETAILED BLOG GENERATION');
    console.log('📝 Final Responses:', JSON.stringify(finalResponses, null, 2));
    
    try {
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: finalResponses.topic,
          platform: finalResponses.platform,
          content_focus: finalResponses.goal,
          audience_level: finalResponses.audience,
          content_length: finalResponses.length === 'short' ? 200 : finalResponses.length === 'long' ? 800 : 500
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('✅ API Response:', data);
        
        let content = '';
        if (data.content) {
          content = data.content;
        } else if (data.title && data.content) {
          content = `# ${data.title}\n\n${data.content}`;
        } else if (typeof data === 'string') {
          content = data;
        } else {
          throw new Error('No content in response');
        }
        
        setGeneratedContent(content);
        setConversationComplete(true);
        speak("Perfect! I've generated your detailed blog content. You can view it in the Platform Optimizer or download it.");
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('💥 Content generation error:', error);
      
      const fallbackContent = `## ${finalResponses.topic}\n\n### Introduction\nWelcome to this comprehensive guide about ${finalResponses.topic}. This ${finalResponses.goal} content is designed for ${finalResponses.audience} and optimized for ${finalResponses.platform}.\n\n### Key Insights\n• Essential information about ${finalResponses.topic}\n• Practical tips and strategies\n• Expert recommendations\n• Real-world applications\n\n### Main Content\nDive deep into the world of ${finalResponses.topic}. Whether you're looking to understand the basics or explore advanced concepts, this guide provides valuable insights.\n\n### Best Practices\n✅ Follow industry standards\n✅ Stay updated with latest trends\n✅ Engage with your community\n✅ Measure and optimize results\n\n### Conclusion\nImplement these strategies to maximize your success with ${finalResponses.topic}. Start applying these insights today!\n\n### Call to Action\nReady to take action? Share your thoughts and experiences in the comments below!\n\n#${(finalResponses.topic || 'topic').replace(/\s+/g, '')} #${finalResponses.platform}tips #contentcreation`;
      
      setGeneratedContent(fallbackContent);
      setConversationComplete(true);
      speak("I've created your detailed blog content using our backup system.");
    }
    setIsProcessing(false);
  };

  const viewInOptimizer = () => {
    // Create blog content object in the same format as ContentGenerator
    const blogContentData = {
      title: `${responses.topic} - ${responses.platform} Content`,
      content: generatedContent,
      platform: responses.platform,
      topic: responses.topic,
      goal: responses.goal,
      audience: responses.audience,
      length: responses.length,
      timestamp: Date.now(),
      source: 'voice-assistant'
    };
    
    // Store in localStorage for Platform Optimizer to access
    localStorage.setItem('voiceGeneratedContent', JSON.stringify(blogContentData));
    
    // Trigger a custom event to notify App.js to switch tabs and pass content
    const event = new CustomEvent('navigateToOptimizer', {
      detail: { blogContent: blogContentData }
    });
    window.dispatchEvent(event);
    
    speak('Opening Platform Optimizer with your generated content.');
  };

  const startConversation = () => {
    setCurrentQuestion(0);
    setResponses({});
    setGeneratedContent('');
    setConversationComplete(false);
    setConversationStarted(true);
  };

  const downloadContent = () => {
    const content = `Topic: ${responses.topic}\nPlatform: ${responses.platform}\nGoal: ${responses.goal}\nAudience: ${responses.audience}\nLength: ${responses.length}\n\n${generatedContent}`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `voice_content_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }} 
          animate={{ opacity: 1, y: 0 }} 
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-3 mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <Bot size={32} className="text-white" />
            </div>
            <div>
              <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                Voice Assistant
              </h1>
              <p className="text-gray-400 text-lg mt-2">AI-Powered Content Creation Through Conversation</p>
            </div>
          </div>
        </motion.div>

        {!conversationComplete ? (
          <div className="space-y-8">
            {!conversationStarted ? (
              /* Welcome Screen */
              <motion.div 
                initial={{ opacity: 0, scale: 0.9 }} 
                animate={{ opacity: 1, scale: 1 }}
                className="max-w-2xl mx-auto text-center"
              >
                <div className="bg-gradient-to-br from-slate-800/50 to-purple-900/30 backdrop-blur-xl rounded-3xl p-12 border border-purple-500/20">
                  <div className="mb-8">
                    <div className="w-24 h-24 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
                      <Mic size={40} className="text-white" />
                    </div>
                    <h2 className="text-3xl font-bold text-white mb-4">Ready to Create Amazing Content?</h2>
                    <p className="text-gray-300 text-lg leading-relaxed">
                      I'll ask you 5 simple questions to understand exactly what you need, 
                      then generate professional blog content tailored to your requirements.
                    </p>
                  </div>
                  
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="relative"
                  >
                    <Button
                      onClick={startConversation}
                      variant="primary"
                      size="xl"
                      icon={<Play size={28} />}
                      className="relative overflow-hidden group min-w-[320px] h-16 text-xl font-bold"
                    >
                      <span className="relative z-10">Start Voice Conversation</span>
                      <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                      <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500 animate-pulse" />
                    </Button>
                    
                    {/* Glow effect */}
                    <div className="absolute -inset-1 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full blur opacity-30 group-hover:opacity-60 transition-opacity duration-300 -z-10" />
                  </motion.div>
                  
                  <div className="mt-10 grid grid-cols-2 gap-6 text-sm text-gray-400">
                    <motion.div 
                      className="flex items-center gap-3 p-3 rounded-lg bg-slate-800/30 border border-purple-500/20"
                      whileHover={{ scale: 1.05, backgroundColor: "rgba(168, 85, 247, 0.1)" }}
                    >
                      <Zap size={18} className="text-purple-400" />
                      <span>AI-Powered Generation</span>
                    </motion.div>
                    <motion.div 
                      className="flex items-center gap-3 p-3 rounded-lg bg-slate-800/30 border border-purple-500/20"
                      whileHover={{ scale: 1.05, backgroundColor: "rgba(168, 85, 247, 0.1)" }}
                    >
                      <Bot size={18} className="text-purple-400" />
                      <span>Natural Conversation</span>
                    </motion.div>
                  </div>
                </div>
              </motion.div>
            ) : (
              /* Conversation Interface */
              <div className="max-w-4xl mx-auto">
                {/* Progress Header */}
                <div className="mb-8">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-2xl font-bold text-white">Question {currentQuestion + 1} of 5</h3>
                    <div className="text-purple-400 font-semibold">{Math.round(((currentQuestion + 1) / 5) * 100)}% Complete</div>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-3">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${((currentQuestion + 1) / 5) * 100}%` }}
                      className="bg-gradient-to-r from-purple-500 to-pink-500 h-3 rounded-full"
                      transition={{ duration: 0.8, ease: "easeOut" }}
                    />
                  </div>
                </div>

                {/* Question Card */}
                <motion.div
                  key={currentQuestion}
                  initial={{ opacity: 0, x: 50 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -50 }}
                  className="bg-gradient-to-br from-slate-800/80 to-purple-900/40 backdrop-blur-xl rounded-3xl p-8 border border-purple-500/30 mb-8"
                >
                  <div className="flex items-start gap-6">
                    <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot size={28} className="text-white" />
                    </div>
                    <div className="flex-1">
                      <p className="text-xl text-gray-100 leading-relaxed mb-6">
                        {questions[currentQuestion]}
                      </p>
                      
                      {/* Voice Status */}
                      <div className="flex items-center gap-4 mb-6">
                        <motion.div
                          animate={isListening ? { scale: [1, 1.1, 1] } : { scale: 1 }}
                          transition={{ repeat: isListening ? Infinity : 0, duration: 1.5 }}
                          className={`flex items-center gap-3 px-6 py-3 rounded-full ${
                            isListening 
                              ? 'bg-red-500/20 text-red-300 border border-red-500/30' 
                              : 'bg-slate-700/50 text-gray-400 border border-slate-600/30'
                          }`}
                        >
                          {isListening ? (
                            <>
                              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
                              <Mic size={20} />
                              <span className="font-medium">Listening... Speak now!</span>
                            </>
                          ) : (
                            <>
                              <MicOff size={20} />
                              <span>Preparing to listen...</span>
                            </>
                          )}
                        </motion.div>
                      </div>

                      {/* Transcript */}
                      <AnimatePresence>
                        {transcript && (
                          <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="bg-slate-700/30 rounded-2xl p-4 border border-slate-600/30"
                          >
                            <div className="flex items-start gap-3">
                              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                                <span className="text-white text-sm font-bold">You</span>
                              </div>
                              <p className="text-gray-200 flex-1">"{transcript}"</p>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>
                </motion.div>
              </div>
            )}
          </div>
        ) : (
          /* Results Screen */
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-5xl mx-auto"
          >
            <div className="bg-gradient-to-br from-slate-800/80 to-purple-900/40 backdrop-blur-xl rounded-3xl p-8 border border-purple-500/30">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center">
                  <Zap size={28} className="text-white" />
                </div>
                <div>
                  <h3 className="text-3xl font-bold text-white">Content Generated Successfully!</h3>
                  <p className="text-gray-400">Your personalized blog content is ready</p>
                </div>
              </div>

              {/* Response Summary */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
                {[
                  { label: 'Topic', value: responses.topic, icon: '📝' },
                  { label: 'Platform', value: responses.platform?.toUpperCase(), icon: '📱' },
                  { label: 'Goal', value: responses.goal, icon: '🎯' },
                  { label: 'Audience', value: responses.audience, icon: '👥' },
                  { label: 'Length', value: responses.length, icon: '📏' }
                ].map((item, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-slate-700/30 rounded-xl p-4 border border-slate-600/30"
                  >
                    <div className="text-2xl mb-2">{item.icon}</div>
                    <p className="text-gray-400 text-sm mb-1">{item.label}</p>
                    <p className="text-white font-semibold">{item.value}</p>
                  </motion.div>
                ))}
              </div>

              {/* Generated Content */}
              <div className="bg-slate-900/50 rounded-2xl p-6 mb-8 border border-slate-700/50">
                <h4 className="text-xl font-bold text-white mb-4">Generated Content</h4>
                <div className="max-h-96 overflow-y-auto">
                  <pre className="text-gray-200 whitespace-pre-wrap font-sans leading-relaxed">
                    {generatedContent}
                  </pre>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-4">
                <Button
                  onClick={downloadContent}
                  variant="success"
                  icon={<Download size={20} />}
                >
                  Download Content
                </Button>

                <Button
                  onClick={viewInOptimizer}
                  variant="info"
                  icon={<Bot size={20} />}
                >
                  View in Platform Optimizer
                </Button>

                <Button
                  onClick={() => {
                    setConversationComplete(false);
                    setCurrentQuestion(0);
                    setResponses({});
                    setGeneratedContent('');
                    setConversationStarted(false);
                  }}
                  variant="primary"
                  icon={<RotateCcw size={20} />}
                >
                  Start New Conversation
                </Button>
              </div>
            </div>
          </motion.div>
        )}

        {/* Processing Modal */}
        <AnimatePresence>
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50"
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-gradient-to-br from-slate-800/90 to-purple-900/50 backdrop-blur-xl rounded-3xl p-8 text-center border border-purple-500/30"
              >
                <div className="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
                <h3 className="text-2xl font-bold text-white mb-2">Creating Your Content</h3>
                <p className="text-gray-300 mb-4">AI is generating your personalized blog post...</p>
                <div className="text-purple-400 font-semibold">Estimated: {estimatedTime}s remaining</div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default VoiceAssistant;