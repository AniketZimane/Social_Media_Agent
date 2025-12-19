import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os
from datetime import datetime


class VoiceAssistant:
    def __init__(self):
        # ------------------ Speech Recognition ------------------
        self.recognizer = sr.Recognizer()

        try:
            self.microphone = sr.Microphone()
        except OSError:
            raise RuntimeError("❌ Microphone not found or PyAudio not installed.")

        # ------------------ Text To Speech ------------------
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        if voices:
            self.tts_engine.setProperty('voice', voices[0].id)
        self.tts_engine.setProperty('rate', 180)

        # ------------------ Gemini AI ------------------
        api_key = os.getenv("GOOGLE_AI_API_KEY")
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY environment variable not set.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        # ------------------ Conversation Flow ------------------
        self.questions = [
            "Hi! I'm your AI blog assistant. What topic would you like to create content about today?",
            "Which platform are you targeting? Instagram, Twitter, LinkedIn, YouTube, or Facebook?",
            "What is your main goal? Educate, entertain, inspire, or promote?",
            "Who is your target audience? Beginners, professionals, or general audience?",
            "How long should the content be? Short, medium, or detailed?"
        ]

        self.responses = {}
        self.current_question = 0

    # ------------------ Speak ------------------
    def speak(self, text):
        print(f"🤖 Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    # ------------------ Listen ------------------
    def listen(self):
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=15)

            print("🔄 Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "unclear"
        except sr.RequestError:
            return "error"

    # ------------------ Process User Response ------------------
    def process_response(self, response, index):
        if index == 0:
            self.responses["topic"] = response

        elif index == 1:
            platforms = ["instagram", "twitter", "linkedin", "youtube", "facebook"]
            self.responses["platform"] = next(
                (p for p in platforms if p in response), "instagram"
            )

        elif index == 2:
            goals = {
                "educate": "educational",
                "entertain": "entertaining",
                "inspire": "inspirational",
                "promote": "promotional"
            }
            self.responses["goal"] = next(
                (goals[g] for g in goals if g in response), "educational"
            )

        elif index == 3:
            audiences = {
                "beginner": "beginners",
                "professional": "professionals",
                "general": "general audience"
            }
            self.responses["audience"] = next(
                (audiences[a] for a in audiences if a in response), "general audience"
            )

        elif index == 4:
            if "short" in response:
                self.responses["length"] = "short"
            elif "detailed" in response or "long" in response:
                self.responses["length"] = "long"
            else:
                self.responses["length"] = "medium"

    # ------------------ Generate Content ------------------
    def generate_content(self):
        prompt = f"""
Create {self.responses['platform']} content on "{self.responses['topic']}"

Requirements:
- Platform: {self.responses['platform']}
- Goal: {self.responses['goal']}
- Audience: {self.responses['audience']}
- Length: {self.responses['length']}

Include:
- Catchy title with emojis
- Bullet points
- Hashtags
- Call to action
- Platform-optimized tone
"""

        try:
            response = self.model.generate_content(prompt)
            if response and hasattr(response, "text"):
                return response.text
            return "No content generated."

        except Exception as e:
            return f"Error generating content: {str(e)}"

    # ------------------ Start Conversation ------------------
    def start_conversation(self):
        self.speak("Welcome to your AI Blog Assistant!")

        retries = 0
        while self.current_question < len(self.questions):
            self.speak(self.questions[self.current_question])
            response = self.listen()

            if response in ["timeout", "unclear", "error"]:
                retries += 1
                self.speak("I didn't catch that. Please try again.")
                if retries >= 3:
                    self.speak("Let's move to the next question.")
                    self.current_question += 1
                    retries = 0
                continue

            self.process_response(response, self.current_question)
            self.current_question += 1
            retries = 0

        self.speak("Generating your content now...")
        content = self.generate_content()

        # ------------------ Save File ------------------
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_generated_content_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        self.speak(f"Your content is ready and saved as {filename}.")
        return content, filename


# ------------------ Run Program ------------------
if __name__ == "__main__":
    assistant = VoiceAssistant()
    content, file = assistant.start_conversation()

    print("\n✅ CONVERSATION COMPLETED")
    print("📄 File:", file)
