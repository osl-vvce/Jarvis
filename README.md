# J.A.R.V.I.S — Just A Rather Very Intelligent System

> An AI-powered desktop assistant inspired by Iron Man's Jarvis, built with Python.  
> Voice-controlled, extensible, and capable of managing your PC through natural language.

---

## Features

- **Voice Recognition** — Real-time speech-to-text via custom STT engine
- **AI Brain** — GPT-powered conversational intelligence with memory and personality
- **Smart Intent Classification** — Offline intent classifier for instant command routing
- **App Control** — Open, close, and manage Windows applications by voice
- **Spotify Integration** — Play songs, albums, control playback hands-free
- **Browser Automation** — Search Google/YouTube, manage tabs
- **Camera Control** — Open camera, take photos, record video
- **Screen Control** — Screenshots, screen management
- **Notes Mode** — Dictate text directly into Notepad
- **Weather & Scheduling** — Check weather, manage schedules and alarms
- **System Controls** — Volume, brightness, window management
- **WhatsApp Automation** — Send messages via WhatsApp

---

## Project Structure

```
Jarvis/
├── Automation/         # App launching, browser, music, scrolling, tab control
├── Brain/              # GPT brain, intent classifier, personality engine
├── Data/               # Dialogue data and response templates
├── Features/           # Brightness, volume, IP lookup, jokes, health checks
├── NetHyTechSTT/       # Speech-to-text listener engine
├── New/                # Data fetching utilities
├── Real_Time/          # Real-time Google search modules
├── TextToImage/        # AI image generation
├── TextToSpeech/       # TTS engine (pyttsx3-based)
├── Time_Operations/    # Scheduling, alarms, time-based alerts
├── Tools/              # System tools (apps, browser, camera, clipboard, etc.)
├── Vision/             # Computer vision modules
├── Weather_Check/      # Weather lookup
├── Whatsapp_automation/# WhatsApp messaging
│
├── jarvis.py           # Entry point — boots all threads
├── co_brain.py         # Core command router and voice loop
├── internet_check.py   # Online/offline detection
├── Alert.py            # Desktop notification alerts
├── ui.py               # UI interface
├── setup.py            # Dependency installer
├── requirements.txt    # Python dependencies
├── LICENSE             # GPL-3.0 License
└── .gitignore
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Windows 10/11
- Microphone for voice input

## Installation

```powershell
# Clone the official repository
git clone https://github.com/osl-vvce/Jarvis.git
cd Jarvis

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Run

```bash
python jarvis.py
```

---

## Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Language        | Python 3.11+                        |
| AI Engine       | OpenAI GPT API                      |
| Speech-to-Text  | Custom STT (NetHyTechSTT)          |
| Text-to-Speech  | pyttsx3                             |
| Vision          | OpenCV                              |
| Browser         | Selenium + ChromeDriver             |
| Desktop Control | pyautogui, psutil, pycaw, comtypes  |
| Notifications   | winotify                            |

---

## License

This project is licensed under the **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for details.

---

## Author

**Abhilash G**  
[GitHub](https://github.com/abhilashg-cell)
