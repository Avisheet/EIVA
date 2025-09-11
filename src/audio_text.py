import whisper
import pyaudio
import numpy as np
import queue

model = whisper.load_model("base")

RATE = 16000
CHUNK = 1024
CHUNK_DURATION = 3
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

    frames = []
    data_text = None
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(np.frombuffer(data, np.int16))

            if len(frames) >= FRAMES_PER_CHUNK:
                audio_np = np.concatenate(frames).astype(np.float32) / 32768.0
                frames = []

                result = model.transcribe(audio_np, fp16=False, language="en")
                text = result["text"].strip()
                if text:
                    return text
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
