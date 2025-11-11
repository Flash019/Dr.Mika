from voice_of_doctor import tts_elevenlabs_bytes  # import your module
from io import BytesIO
import platform
import subprocess

# The text you want to test
sample_text = "Hello! Dr. Mika here — how can I help you today?"

# Get in-memory audio bytes
audio_bytes: BytesIO = tts_elevenlabs_bytes(sample_text)

# Save temporarily to play
temp_file = "drmika_test.mp3"
with open(temp_file, "wb") as f:
    f.write(audio_bytes.getbuffer())

# Play the audio (cross-platform)
os_name = platform.system()
try:
    if os_name == "Darwin":  # macOS
        subprocess.run(['afplay', temp_file])
    elif os_name == "Windows":  # Windows
        subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{temp_file}").PlaySync();'])
    elif os_name == "Linux":  # Linux
        subprocess.run(['mpg123', temp_file])
    else:
        raise OSError("Unsupported OS")
except Exception as e:
    print(f"Error playing audio: {e}")
