# 🤖 HarzAI - Most Advanced AI Assistant

### Speacial thanks to @KaushikShresth07

**HarzAI** is a cutting-edge AI assistant application that combines natural language processing, real-time web search, automation, multimedia generation, and voice interaction capabilities. It's designed to be an intelligent, multi-functional personal assistant that can handle complex tasks seamlessly.

---

## ✨ Features

### 🧠 Core AI & Conversation
- **Advanced Chatbot**: Powered by Groq's Llama 3.3-70B model for intelligent conversations
- **Smart Decision Model**: Cohere-based intelligence for classifying user queries into appropriate action categories
- **Real-Time Information**: Access to current date, time, and live data without training data limitations
- **Task Memory**: Remembers user tasks and incorporates them into responses for context-aware conversations
- **Customizable Persona**: Configure assistant name and user name via environment variables

### 🔍 Web & Search Capabilities
- **Google Search Integration**: Search Google directly from voice commands
- **YouTube Search**: Find and play videos on YouTube
- **Real-Time Web Data**: Fetch current information not available in training data
- **Web Scraping**: Parse and extract information from web pages using BeautifulSoup

### 🎤 Voice Interaction
- **Speech-to-Text (STT)**: Convert voice input to text using WebkitSpeechRecognition
- **Text-to-Speech (TTS)**: Convert text responses to speech using Microsoft Edge's neural voices
- **Voice Control**: Hands-free operation with microphone integration
- **Real-time Speech Recognition**: Async speech processing for smooth user experience

### 🎨 Content & Media Generation
- **Image Generation**: Create images from text prompts using Gemini AI
- **Video Generation**: Generate videos from descriptions using advanced video synthesis
- **Presentation Creation**: Generate slides/presentations on specified topics
- **Content Writing**: Write essays, letters, articles, code, poems, stories, and more

### 🤖 System Automation
- **Application Control**: Open and close applications via voice commands
- **Website Opening**: Launch websites directly from voice commands
- **Music Playback**: Play songs on YouTube with natural language requests
- **System Controls**: Mute/unmute, volume control, and other system operations
- **Timer & Notifications**: Set timers and send system notifications
- **Task Management**: Add, view, and remove tasks with persistent memory

### 📚 Data Management
- **Chat History**: Maintains persistent chat logs in JSON format
- **Task Management**: Store and retrieve user tasks from local files
- **Session Persistence**: Continue conversations across sessions
- **Data Organization**: Structured data storage in Data/ directory

### 🎯 Additional Features
- **Multi-LLM Architecture**: Uses different specialized models for different tasks:
  - Decision Making: Cohere Command-R-Plus
  - General Chat: Groq Llama-3.3-70B
  - Content Writing: Groq Llama-3.1-8B
- **Desktop GUI**: Modern PyQt5-based graphical interface
- **Responsive UI**: Real-time updates and status indicators
- **Error Handling**: Robust error handling with graceful degradation
- **Async Operations**: Non-blocking operations for smooth user experience

---

## 🛠 Technology Stack

### Backend Technologies
- **Python 3.8+**: Core programming language
- **Groq API**: LLM for chatbot and content generation
- **Cohere API**: Decision-making and query classification
- **Gemini API**: Image generation
- **Microsoft Edge TTS**: Neural text-to-speech
- **WebkitSpeechRecognition**: Voice input via Selenium

### Frontend
- **PyQt5**: Desktop GUI framework
- **PyAutoGUI**: GUI automation
- **Pillow**: Image processing

### Utilities & Libraries
- **BeautifulSoup4**: Web scraping
- **Requests**: HTTP requests
- **pywhatkit**: Google search and YouTube functionality
- **AppOpener**: Open/close applications
- **Selenium**: Browser automation for speech recognition
- **keyboard**: Keyboard input handling
- **plyer**: System notifications
- **pygame**: Audio playback
- **python-dotenv**: Environment variable management

---

## 📋 Requirements

```
python-dotenv==1.0.1
groq==0.16.0
AppOpener==1.7
pywhatkit==5.4
beautifulsoup4==4.12.3
rich==13.9.4
requests==2.32.3
keyboard==0.13.5
cohere==5.13.11
googlesearch-python==1.3.0
selenium==4.28.1
webdriver-manager==4.0.2
mtranslate==1.8
pygame==2.6.0
edge-tts==7.2.7
PyQt5==5.15.10
pyautogui==0.9.54
pillow==10.4.0
pytrends==4.9.2
plyer==2.1.0
```

---

## 🚀 Installation & Setup

### 1. **Clone the Repository**
```bash
git clone https://github.com/harz129/HarzAI---Most-Advance-AI-Assistant.gitcd HarzAI
```

### 2. **Install Dependencies**
```bash
pip install -r Requirements.txt
```

### 3. **Configure Environment Variables**
Create a `.env` file in the root directory:
```
Username=YourName
Assistantname=HarzAI
GroqAPIKey=your_groq_api_key_here
CohereAPIKey=your_cohere_api_key_here
```

### 4. **Run the Application**
```bash
# On Windows
Run.bat

# On Linux/Mac
python Main.py
```

---

## 🎮 How to Use

### Voice Commands
Simply speak to HarzAI using natural language:

**General Queries:**
- "Who was Akbar?"
- "How can I study more effectively?"
- "What is Python?"

**Real-Time Information:**
- "What is today's news?"
- "Who is the current Indian Prime Minister?"
- "Tell me about recent Facebook updates"

**Application Control:**
- "Open Facebook"
- "Close Notepad"
- "Open multiple apps"

**Media & Entertainment:**
- "Play Let Her Go"
- "Search for Python tutorials on YouTube"

**Content Generation:**
- "Generate an image of a lion"
- "Write a professional email"
- "Create slides on global warming"

**System Controls:**
- "Set a timer for 10 minutes"
- "Send me a notification"
- "Mute the system"

**Task Management:**
- "Add task: Buy groceries"
- "Show my tasks"
- "Remove completed tasks"

---

## 📁 Project Structure

```
HarzAI/
├── Main.py                 # Main application entry point
├── Requirements.txt        # Python dependencies
├── Run.bat                # Windows batch file to run the app
├── .env                    # Environment variables (create this)
│
├── Backend/               # Core backend modules
│   ├── Model.py           # AI decision-making model
│   ├── Chatbot.py         # Chat response generation
│   ├── Automation.py      # System automation tasks
│   ├── SpeechToText.py    # Voice input processing
│   ├── TextToSpeech.py    # Voice output generation
│   ├── ImageGeneration.py # AI image creation
│   ├── VideoGeneration.py # AI video creation
│   ├── RealtimeSearchEngine.py # Web search functionality
│   └── Files/             # Backend temporary files
│
├── Frontend/              # GUI and interface
│   ├── GUI.py            # PyQt5 main interface
│   ├── Files/            # Temporary GUI data files
│   └── Graphics/         # UI assets and images
│
└── Data/                  # User data storage
    ├── ChatLog.json       # Chat history
    └── Daily tasks.txt    # Task list
```

---

## 🔐 Security & Privacy

- **Local Data Storage**: All chat history and tasks are stored locally
- **API Key Protection**: Use environment variables for sensitive API keys
- **No Cloud Dependency**: Core data remains on your machine
- **Secure Authentication**: API keys never exposed in code

---

## 🎯 Core Components

### 1. **Main.py**
Entry point that orchestrates all components:
- Initializes GUI and backend services
- Manages chat history and sessions
- Handles user interactions

### 2. **Model.py (FirstLayerDMM)**
Decision-Making Model that classifies user queries:
- Categorizes queries as general, real-time, automation, or content
- Routes queries to appropriate handlers
- Reduces redundant API calls

### 3. **Chatbot.py**
Conversational AI powered by Groq:
- Maintains context across conversations
- Integrates task memory
- Provides real-time information awareness

### 4. **Automation.py**
Handles all automated tasks:
- Opens/closes applications
- Performs web searches
- Plays music
- Generates content
- Manages system controls

### 5. **SpeechToText.py**
Voice input processing:
- WebkitSpeechRecognition via Selenium
- Converts speech to text in real-time
- Supports multiple languages

### 6. **TextToSpeech.py**
Voice output generation:
- Microsoft Edge neural voices
- Multiple voice options
- Natural speech synthesis

### 7. **GUI.py**
Modern desktop interface:
- PyQt5-based UI
- Real-time chat display
- Microphone status indicator
- Responsive design

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Improve documentation
- Submit pull requests

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Harshit Goyal** - [@harz129](https://github.com/harz129)

---

## 🌟 Features Roadmap

- [ ] Multi-language support
- [ ] Cloud backup for chat history
- [ ] Mobile app version
- [ ] Plugin system for custom extensions
- [ ] Advanced emotion recognition
- [ ] Offline mode support
- [ ] Advanced analytics and insights
- [ ] Integration with smart home devices

---

## 📞 Support & Contact

For issues, feature requests, or general inquiries:
- Open an issue on [GitHub](https://github.com/harz129/HarzAI)
- Check existing documentation
- Review the code comments for detailed explanations

---

## 🎉 Acknowledgments

- Groq for powerful LLM capabilities
- Cohere for decision-making intelligence
- Google for search and web services
- Microsoft for Edge TTS neural voices
- Gemini for image generation
- PyQt5 for the GUI framework

---

**HarzAI** - Your Advanced AI Assistant 🚀
