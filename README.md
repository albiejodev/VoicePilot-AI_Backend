# 🎙️ VoicePilot AI Backend

<p align="center">

**A Real-Time AI Voice Receptionist built with FastAPI, Gemini, Deepgram, Redis, ElevenLabs & Google Calendar**

Real-time speech conversations • AI memory • Tool Calling • Appointment Booking

</p>

---

## 🚀 Overview

VoicePilot AI is a real-time conversational AI receptionist capable of understanding spoken language, maintaining conversation memory, booking appointments, and responding with natural AI-generated speech.

The backend receives live audio over WebSockets, converts speech to text using **Deepgram**, processes conversations using **Gemini 2.5 Flash**, stores conversation history in **Redis**, executes external tools such as **Google Calendar**, synthesizes responses using **ElevenLabs**, and streams audio back to the client.

The current demo uses a **React Web Client** as the audio transport layer.

The architecture is intentionally transport-agnostic, making it easy to integrate **Twilio Media Streams** later to support real phone calls.

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.12 |
| Framework | FastAPI |
| Communication | WebSockets |
| AI Model | Gemini 2.5 Flash |
| Speech-to-Text | Deepgram |
| Text-to-Speech | ElevenLabs |
| Memory | Redis |
| Tool Calling | Custom Tool Executor |
| Calendar | Google Calendar API |
| Containerization | Docker |

---

# ✨ Features

- ✅ Real-time voice conversations
- ✅ Live Speech-to-Text
- ✅ Live AI audio responses
- ✅ Conversation memory using Redis
- ✅ Multi-turn conversations
- ✅ Google Calendar appointment booking
- ✅ Tool Calling Architecture
- ✅ WebSocket streaming
- ✅ Browser voice client
- ✅ Modern AI workflow

---

# 🏗 System Architecture

```text
                            VoicePilot AI

                    ┌─────────────────────────┐
                    │     React Frontend      │
                    │ Voice Recorder (Demo)   │
                    └─────────────┬───────────┘
                                  │
                             WebSocket
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    │  WebSocket Controller   │
                    └─────────────┬───────────┘
                                  │
          ┌───────────────────────┼────────────────────────┐
          ▼                       ▼                        ▼
   Deepgram STT             Gemini 2.5 Flash          Redis Memory
 Speech → Text              Conversation AI         Conversation History
          │                       │                        │
          └───────────────────────┼────────────────────────┘
                                  ▼
                         Tool Execution Layer
                                  │
                ┌─────────────────┴─────────────────┐
                ▼                                   ▼
       Google Calendar API                 ElevenLabs TTS
      Appointment Booking               AI Speech Generation
                │                                   │
                └─────────────────┬─────────────────┘
                                  ▼
                          Audio Response
                                  │
                                  ▼
                          Browser Speaker

Future

Browser
     │
     ▼
Twilio Media Streams
     │
     ▼
Phone Calls
```

---

# 🔄 Request Flow

```text
User speaks

        │

        ▼

React Frontend

        │

WebSocket Audio

        │

        ▼

FastAPI

        │

        ▼

Deepgram

        │

Speech → Text

        │

        ▼

Gemini

        │

Conversation Memory (Redis)

        │

Tool Calling (if required)

        │

Google Calendar

        │

AI Response

        │

ElevenLabs

        │

Audio Stream

        │

Browser Speaker
```

---

# 📂 Project Structure

```text
backend/

│

├── app/

│   ├── api/
│   ├── core/
│   ├── graph/
│   ├── models/
│   ├── services/
│   │     ├── ai/
│   │     ├── aggregation/
│   │     ├── calendar/
│   │     ├── conversation/
│   │     ├── memory/
│   │     ├── stt/
│   │     ├── tools/
│   │     └── tts/
│   │
│   ├── utils/
│   └── websocket/

│

├── docker-compose.yml

├── requirements.txt

├── main.py

└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>

cd backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate

```bash
source venv/bin/activate

# Windows

venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file

```env
GEMINI_API_KEY=

DEEPGRAM_API_KEY=

ELEVENLABS_API_KEY=

REDIS_URL=

GOOGLE_CLIENT_SECRET_FILE=
```

---

# ▶️ Running the Project

Start Redis

```bash
docker compose up -d
```

Start Backend

```bash
uvicorn main:app --reload
```

---

# 🚀 Deployment

VoicePilot AI is deployment-ready and can be hosted using:

- Docker
- EC2
- DigitalOcean
- Railway
- Render
- Azure
- Google Cloud

Recommended production stack

```text
Internet

↓

Nginx

↓

FastAPI

↓

Redis

↓

External AI Services
```

---

# 📸 Screenshots

> Add screenshots here

### Home Screen

*(Add Image)*

---

### Live Conversation

*(Add Image)*

---

### Appointment Booking

*(Add Image)*

---

### Google Calendar Event

*(Add Image)*

---

# 🎥 Demo Video

> Add YouTube / Loom link here

---

# 🎯 Why I Built This

Traditional chatbots are limited to text-based interactions.

The goal of VoicePilot AI was to build a real-time voice AI agent capable of understanding spoken language, remembering previous conversations, interacting with external systems, and responding naturally using synthesized speech.

This project combines multiple AI services into one production-style workflow, demonstrating how modern voice assistants are built.

---

# 💡 Challenges & Learnings

During development I explored:

- Real-time audio streaming
- WebSocket communication
- AI tool calling
- Conversation memory
- Streaming speech synthesis
- Redis session management
- Async Python
- Google Calendar integration
- Multi-provider AI orchestration
- Latency optimization for voice conversations

---

# 🛣 Future Roadmap

- 📞 Twilio Media Streams integration
- 📚 RAG Knowledge Base
- 📧 Email confirmations
- 📱 SMS reminders
- 🌍 Multi-language support
- 👨‍💼 Human handoff
- 📊 Call analytics dashboard
- 📝 Conversation summaries
- 🗄 Persistent database
- ☁ Cloud deployment

---

# 🙏 Acknowledgements

- Google Gemini
- Deepgram
- ElevenLabs
- FastAPI
- Redis
- Google Calendar API

---

# 📄 License

MIT License