import whisper
import pyaudio
import numpy as np
import threading
import queue

model = whisper.load_model("base")

# Audio settings
RATE = 16000       # sample rate
CHUNK = 1024       # buffer size (~64ms of audio)
CHUNK_DURATION = 3 # seconds of audio per transcription chunk

# Derived values
FRAMES_PER_CHUNK = int(RATE * CHUNK_DURATION / CHUNK)

audio_queue = queue.Queue()

def audio_capture():
    """Capture audio and push fixed-size chunks into queue."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(" Listening... (Ctrl+C to stop)")

    frames = []
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(np.frombuffer(data, np.int16))

            if len(frames) >= FRAMES_PER_CHUNK:
                audio_np = np.concatenate(frames).astype(np.float32) / 32768.0
                audio_queue.put(audio_np)
                frames = []
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def transcribe_loop():
    """Continuously take chunks from queue and transcribe."""
    while True:
        audio_chunk = audio_queue.get()
        if audio_chunk is None:
            break

        result = model.transcribe(audio_chunk, fp16=False, language="en")
        text = result["text"].strip()

        if text:
            print(f" {text}", flush=True)

if __name__ == "__main__":
    # Start audio capture thread
    t = threading.Thread(target=audio_capture, daemon=True)
    t.start()

    # Run transcription loop
    try:
        transcribe_loop()
    except KeyboardInterrupt:
        print("\n Stopped.")

