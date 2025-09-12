from gtts import gTTS
import io
import pygame

def text_to_speech(text, lang="en-in"):
    """
    Convert text to human-like speech using Google TTS
    and play directly through speakers (no file saved).
    """

    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    pygame.mixer.init()
    pygame.mixer.music.load(fp, "mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    while True:
        user_input = input("Enter text (or 'exit' to quit): ")
        if user_input.lower() in ["exit", "quit"]:
            break
        text_to_speech(user_input)
