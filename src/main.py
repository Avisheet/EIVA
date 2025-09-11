import audio_text
import emotion_detection

def main():
    print("Speak something... (Ctrl+C to quit)")

    try:
        while True:
            # Capture a spoken phrase
            text = audio_text.audio_capture()
            if text:
                print(f"\nYou said: {text}")

                # Detect emotions instantly
                emotions = emotion_detection.get_top_emotions(text, top_k=3)
                print("Emotions detected:")
                for emo in emotions:
                    print(f"- {emo['label']}: {emo['score']*100:.2f}%")
                print()
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    main()
