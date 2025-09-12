from eiva_brain import ask_eiva
from text_audio import text_to_speech

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        print("EIVA:", end=" ", flush=True)
        for sentence in ask_eiva(user_input):
            text_to_speech(sentence)
