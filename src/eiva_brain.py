import ollama

model_name = "llama3:8b"

def ask_eiva(question):
    """
    Sends a question to the Ollama model and yields text chunks in real time.
    """
    stream = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": question}],
        stream=True,
    )

    buffer = ""
    for chunk in stream:
        if "message" in chunk and "content" in chunk["message"]:
            text = chunk["message"]["content"]
            print(text, end="", flush=True)
            buffer += text

            if any(p in buffer for p in [".", "?", "!"]):
                yield buffer.strip()
                buffer = ""

    if buffer:
        yield buffer.strip()
    print()


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("EIVA: Goodbye!")
            break

        print("EIVA:", end=" ", flush=True)
        for sentence in ask_eiva(user_input):
            print(f"\n[Sentence Detected for TTS]: {sentence}")
