import pvporcupine
import pyaudio
import openai
import requests
import sounddevice as sd
import numpy as np
import io
import soundfile as sf
import tempfile
import datetime
import os

# --- API configurations ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
PICOVOICE_API_KEY = os.getenv("PICOVOICE_API_KEY")
WAKE_WORD = "jarvis"
SAMPLE_RATE = 16000
RECORD_SECONDS = 3

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

def record_audio(seconds=RECORD_SECONDS, fs=SAMPLE_RATE):
    print(f"Listening for {seconds} seconds...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    audio_data = recording.flatten()
    return (audio_data * 32767).astype(np.int16).tobytes()

def detect_wake_word():
    porcupine = pvporcupine.create(access_key=PICOVOICE_API_KEY, keywords=[WAKE_WORD])
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    print(f"Say '{WAKE_WORD}' to activate Jarvis.")
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = np.frombuffer(pcm, dtype=np.int16)
            result = porcupine.process(pcm)
            if result >= 0:
                print(f"Wake word '{WAKE_WORD}' detected!")
                break
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

def transcribe_audio(audio_bytes):
    import whisper
    model = whisper.load_model("base")
    print("Transcribing audio...")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        sf.write(tmp.name, np.frombuffer(audio_bytes, dtype=np.int16), SAMPLE_RATE)
        result = model.transcribe(tmp.name, fp16=False)
    print(f"Transcription: {result['text']}")
    return result['text']

def handle_builtin_queries(text):
    text = text.lower()
    if "what time is it" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."
    elif "what day is it" in text:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}."
    return None

def openai_chat(prompt):
    print("Querying OpenAI...")
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    answer = response.choices[0].message.content.strip()
    print(f"OpenAI response: {answer}")
    return answer

def elevenlabs_tts(text):
    print("Generating speech with ElevenLabs...")
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75}
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
            tmp_path = f.name
        data, fs = sf.read(tmp_path, dtype='int16')
        sd.play(data, fs)
        sd.wait()
        os.remove(tmp_path)
    else:
        print(f"Error from ElevenLabs API: {response.status_code} {response.text}")

def main():
    detect_wake_word()
    audio_bytes = record_audio()
    text = transcribe_audio(audio_bytes)
    if not text.strip():
        print("Did not catch that.")
        return

    # Check for built-in responses first
    builtin_response = handle_builtin_queries(text)
    if builtin_response:
        response = builtin_response
    else:
        response = openai_chat(text)

    elevenlabs_tts(response)

if __name__ == "__main__":
    main()
