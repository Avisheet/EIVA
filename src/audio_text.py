import whisper
import pyaudio
import numpy as np
import threading
import time

# Load Whisper model
model = whisper.load_model("small")

# Audio settings
RATE = 16000       # sample rate
CHUNK = 1024       # buffer size (about 64ms of audio)
ROLLING_WINDOW = 5 # seconds of audio to keep in buffer

# Shared buffer
audio_buffer = np.zeros(RATE * ROLLING_WINDOW, dtype=np.float32)
buffer_lock = threading.Lock()

def audio_capture():
    """Capture audio from microphone and fill buffer."""
    global audio_buffer
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening... (press Ctrl+C to stop)")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_np = np.frombuffer(data, np.int16).astype(np.float32) / 32768.0

            with buffer_lock:
                audio_buffer = np.roll(audio_buffer, -len(audio_np))
                audio_buffer[-len(audio_np):] = audio_np
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def transcribe_loop():
    """Continuously transcribe from rolling buffer."""
    global audio_buffer
    while True:
        time.sleep(1)  # every 1 sec update subtitles
        with buffer_lock:
            audio_copy = audio_buffer.copy()

        result = model.transcribe(audio_copy, fp16=False, language="en")
        text = result["text"].strip()
        if text:
            print(f"\r{text}", end="")

if __name__ == "__main__":
    # Start audio thread
    t = threading.Thread(target=audio_capture, daemon=True)
    t.start()

    # Run transcription loop
    try:
        transcribe_loop()
    except KeyboardInterrupt:
        print("\nStopped.")
