
import logging
from voice_of_patient import record_audio_in_memory, transcribe_with_groq_memory, stt_model, GROQ_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    audio_bytes = record_audio_in_memory(timeout=10, phrase_time_limit=5)
    if audio_bytes:
        text = transcribe_with_groq_memory(stt_model, audio_bytes, GROQ_API_KEY)
        print("Transcribed Text:", text)
    else:
        print("Recording failed")

if __name__ == "__main__":
    main()
