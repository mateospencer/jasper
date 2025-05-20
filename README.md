# Jarvis Voice Assistant

A simple voice assistant that listens for the wake word **"Jarvis"**, records your speech, transcribes it with Whisper, responds with OpenAI’s GPT-3.5-turbo, and speaks the response using ElevenLabs Text-to-Speech API.

---

## Current Features

- Wake word detection using Picovoice Porcupine
- Audio recording and transcription with Whisper
- Built-in responses for "What time is it?" and "What day is it?"
- OpenAI GPT-3.5-turbo for chat completions
- Speech synthesis via ElevenLabs Text-to-Speech
- Easy setup and run on your local machine

---
## Requirements

### 1. APIs
- OpenAI: Handles natural language understanding and response generation. Sends spoken query after transcription to OpenAI's GPT-3.5-Turbo. 
- ElevenLabs: Handles text-to-speech for the assistants response and making it sound human. 
- PicoVoice (Porcupine): Handles wake word detection. 

### 2. Costs
- Note on GPT-3.5-Turbo: I used GPT-3.5 Turbo because the input compared to GPT-4 Turbo (o4) mainly due to cost reduction. GPT-4 costs 0.01/ 1K tokens for input and 0.03 / 1k tokens for output. Whereas GPT-3.5 costs 0.001 / 1k tokens for input and output is free. GPT-4 is more advanced and gives more natural replies. Cost estimates for this project were to keep the prototype under $10/month. 

- Whisper is used locally for the free voice input. 
- PicoVoice has a free-tier
 
## 3. Setup Instructions

```bash
git clone https://github.com/mateospencer/jasper.git
cd jarvis-assistant
``

2. Create and activate a Python virtual environment

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

Create a .env file in the project root or set environment variables in your shell:

export OPENAI_API_KEY="your_openai_api_key"
export ELEVENLABS_API_KEY="your_elevenlabs_api_key"
export PICOVOICE_API_KEY="your_picovoice_access_key"

Replace the values with your actual API keys:
	•	OPENAI_API_KEY: Your OpenAI API key (https://platform.openai.com/account/api-keys)
	•	ELEVENLABS_API_KEY: Your ElevenLabs API key (https://beta.elevenlabs.io/)
	•	PICOVOICE_API_KEY: Your Picovoice Porcupine access key (https://picovoice.ai/)

5. Run the Jarvis assistant

```bash
python jarvis.py
```
Say the wake word “Jarvis” clearly when prompted. Then speak your query or command.

⸻

How It Works (Code Explanation)
1. Wake Word Detection: Uses the Picovoice Porcupine engine to listen continuously for the wake word "jarvis". When detected, it activates the assistant.
2. Audio Recording: Records ~3 seconds of audio after the wake word using the sounddevice library at 16 kHz sample rate.
3. Transcription: Uses OpenAI’s Whisper model (loaded locally with the whisper package) to transcribe the recorded speech into text.
4. Built-in Queries: Checks if the query is asking for the current time or date and returns the appropriate response without calling OpenAI.
5. OpenAI Chat Completion: If the query is not a built-in one, sends the text prompt to OpenAI’s GPT-3.5-turbo API for a chat completion reply.
6. Text-to-Speech: Sends the response text to ElevenLabs Text-to-Speech API, downloads the audio stream, and plays it back via sounddevice.

⸻

Requirements (requirements.txt)

openai
sounddevice
numpy
pyaudio
pvporcupine
requests
whisper
soundfile
python-dotenv


⸻

Notes
	•	The program listens for the wake word once per run due to being a proof of concept; restart to listen again. This will change in the next version. 
	•	ElevenLabs voice ID is set to a default (EXAVITQu4vr4xnSDxMaL), you can replace it in the code with a voice ID of your choice.
	•	Picovoice Porcupine requires a valid access key and internet connection on first use.
	•	Whisper requires a local model download and will use CPU by default.
⸻

License

MIT License

⸻

## 4. Future Development
- Developing to enable continous listening as well as a sleep command.
- Adding Spotify API integration
- Adding some smart home integration
- Adding some computer controls
