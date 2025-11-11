import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
stt_model = "whisper-large-v3"


# Step 1: Record audio (in memory)

def record_audio_in_memory(timeout=20, phrase_time_limit=None) -> BytesIO:
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert WAV to MP3 in memory
            wav_bytes = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_bytes))
            mp3_bytes_io = BytesIO()
            audio_segment.export(mp3_bytes_io, format="mp3", bitrate="128k")
            mp3_bytes_io.seek(0)

            logging.info("Audio ready in memory (no file saved).")
            return mp3_bytes_io

    except Exception as e:
        logging.error(f"An error occurred while recording: {e}")
        return None


# Step 2: Transcribe with Groq API

def transcribe_with_groq_memory(stt_model, audio_bytes_io: BytesIO, GROQ_API_KEY):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        audio_bytes_io.seek(0)

        # Groq requires a filename and MIME type
        file_tuple = ("patient_audio.mp3", audio_bytes_io, "audio/mpeg")

        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=file_tuple,
            language="en"  
        )
        return transcription.text
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return ""
